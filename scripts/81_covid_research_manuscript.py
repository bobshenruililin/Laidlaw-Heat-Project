#!/usr/bin/env python3
"""Build/audit the COVID exploratory manuscript using only public aggregate outputs.

Run with the bundled document Python. --audit reads no governed health file and
checks scientific tables independently against approved CSVs. PDF rendering uses
the packaged document renderer after this Word build, not a system office app.
The previous builder remains available for historical versions.
"""
from pathlib import Path
import argparse, csv, hashlib, importlib.util, json, re, sys
ROOT=Path(__file__).resolve().parents[1]
M=ROOT/'manuscript/covid_period'
EXPS=['mean_temp','mean_tmax','mean_tmin','hot_nights','very_hot_days','cold_days']
NAMES=['Mean temperature / 1°C','Mean maximum / 1°C','Mean minimum / 1°C','Hot nights / 5 days','Very hot days / 5 days','Cold days / 5 days']
SCENARIOS=['trend_ns3','trend_ns6','trend_ns8','year_fixed_effects','drop_first_12_months','drop_first_24_months','covid_phase_adjusted']
SOURCES=['outputs/tables/cvd_descriptive_annual_totals.csv','outputs/tables/cvd_descriptive_covid_era_means.csv','outputs/tables/cvd_core_robust_estimates.csv','outputs/tables/cvd_trend_depletion_sensitivity.csv','outputs/tables/cvd_core_model_fit.csv']
def read(path):return list(csv.DictReader((ROOT/path).open()))
def ci(row):return f"{float(row['rr']):.3f} ({float(row['rr_low']):.3f}–{float(row['rr_high']):.3f})"
def blocks(text):
 spec=importlib.util.spec_from_file_location('covid_layout',ROOT/'scripts/78_covid_period_manuscript_docx.py'); module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
 return module,module.parse_blocks(text)
def audit():
 main=(M/'Manuscript_covid_period_draft.md').read_text();supp=(M/'Supplement_covid_period.md').read_text()
 b,mb=blocks(main);_,sb=blocks(supp);mt=[b.parse_table(x)[1]for k,x in mb if k=='table'];st=[b.parse_table(x)[1]for k,x in sb if k=='table']
 checks=[]
 def ck(name,condition):
  checks.append({'check':name,'passed':bool(condition)})
  if not condition:raise AssertionError(name)
 annual=read(SOURCES[0]);a={(r['outcome'],int(r['year'])):int(r['total_events'])for r in annual}
 ck('main annual table matches all 22 approved outcome totals',mt[0]==[[str(y),f"{a['chd',y]:,}",f"{a['hf',y]:,}"]for y in range(2013,2024)])
 sens=read(SOURCES[3]);s={(r['outcome'],r['exposure'],r['scenario']):r for r in sens}
 ck('nested and full official panel matches 12 source estimates and intervals',mt[1]==[[o.upper(),dict(zip(EXPS,NAMES))[e],ci(s[o,e,'pre_covid']),ci(s[o,e,'baseline_ns4'])]for o in ['chd','hf']for e in EXPS[3:]])
 era=read(SOURCES[1]);periods=[('pre_covid_2013_2019','2013–2019','84'),('covid_2020_2022','2020–2022','36'),('post_reopening_2023','2023','12')]
 ck('disjoint era means and month counts match approved summaries',st[0]==[[label,n]+[f"{float(next(r['mean_events']for r in era if r['outcome']==o and r['period']==key)):.1f}"for o in ['chd','hf']]for key,label,n in periods])
 core=[r for r in read(SOURCES[2])if r['family']=='negative_binomial' and r['offset_policy']=='days_only' and r['model_structure']=='single_exposure'];d={(r['outcome'],r['exposure']):r for r in core if r['se_method']=='NeweyWest_lag6'}
 ck('complete twelve-fit panel and q family match source',st[1]==[[o.upper(),name,ci(d[o,e]),f"{float(d[o,e]['p_value']):.3f}",f"{float(d[o,e]['q_value_core_bh']):.3f}"]for o in ['chd','hf']for e,name in zip(EXPS,NAMES)])
 for i,o in enumerate(['chd','hf']):
  ck(f'{o} all 21 alternative-calendar estimates match source',[row[1:]for row in st[2+i]]==[[ci(s[o,e,key])for e in EXPS[3:]]for key in SCENARIOS])
  expected=[]
  for e,name in zip(EXPS,NAMES):
   row=[name]
   for method in ['model','HC1','NeweyWest_lag3','NeweyWest_lag6']:
    r=next(r for r in core if (r['outcome'],r['exposure'],r['se_method'])==(o,e,method));row.append(f"{float(r['rr_low']):.4f}–{float(r['rr_high']):.4f}")
   expected.append(row)
  ck(f'{o} all uncertainty bounds match source',st[4+i]==expected)
 for o in ['chd','hf']:
  total=sum(a[o,y]for y in range(2013,2024));ck(f'{o} cumulative total in body',f'{total:,}'in main)
  for y in [2020,2023]:
   pct=100*(1-a[o,y]/a[o,2019]);ck(f'{o} {y} percentage versus 2019',f'{pct:.1f}%'in main)
 ck('multiplicity minimum correctly displayed',round(min(float(r['q_value_core_bh'])for r in d.values()),3)==.192 and '0.192'in main)
 ck('near-null HF minimum interval and p value use unrounded source',f"{float(d['hf','mean_tmin']['rr_high']):.10f}"in supp and f"{float(d['hf','mean_tmin']['p_value']):.4f}"in supp)
 ck('reference numbering complete',sorted(set(int(x)for group in re.findall(r'\[([0-9, ]+)\]',main) for x in group.split(',')))==list(range(1,15)) and len(re.findall(r'^\d+\. ',main,re.M))==14)
 weather=next(x for x in main.split('\n\n')if x.startswith(b.HOGAN_OPEN));live=(ROOT/'manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md').read_text();ck('entire protected weather paragraph unchanged',weather in live)
 ck('all health source rows retain approved aggregate label',all(r['data_status']=='HA_APPROVED_AGGREGATE'for r in annual+era+core+sens))
 ck('no temporary tokens or fabricated declarations',not any(x in main+supp for x in ['ANNUAL_TABLE','OFFICIAL_TABLE','REFERENCES','UW XX-XXX','Author 2','Gate 3','ruling-out exhibit','Positive serial correlation should inflate']))
 ck('later-era limitation remains explicit','No 2020–2023-only model or exposure-by-period interaction was available.'in main)
 ck('weather exclusion is not inferred','The thermal panel also cannot exclude weather as an explanation'in main)
 ck('interpretation is exploratory','not evidence that cold became protective'in main)
 out={'date':'2026-10-02','status':'PASS','scope':'Direct source-to-table/value and interpretation checks; no health models run; no governance approval inferred','checks':checks,'tables':{'annual':mt[0],'official_nested_full':mt[1],'disjoint_periods':st[0],'full_panel':st[1],'calendar_sensitivity':st[2:4],'uncertainty':st[4:6]},'nested_continuous':{o:{e:ci(s[o,e,'pre_covid'])for e in EXPS[:3]}for o in ['chd','hf']},'sources':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()for f in SOURCES},'manuscript_sha256':hashlib.sha256((M/'Manuscript_covid_period_draft.md').read_bytes()).hexdigest(),'figure':{'path':'figures/covid_period/figure_annual_counts_20261002.png','sha256':hashlib.sha256((ROOT/'figures/covid_period/figure_annual_counts_20261002.png').read_bytes()).hexdigest()},'supplement_sha256':hashlib.sha256((M/'Supplement_covid_period.md').read_bytes()).hexdigest()}
 (M/'claim_ledger.yml').write_text('# JSON is a YAML subset. Audit of the current COVID revision; historical ledger is in Git.\n'+json.dumps(out,indent=2,ensure_ascii=False)+'\n')
 print(f"PASS: {len(checks)} source and claim checks")

def build():
 from docx import Document
 from docx.shared import Pt,RGBColor
 from docx.oxml import OxmlElement
 from docx.oxml.ns import qn
 for source,target,header in [('Manuscript_covid_period_draft.md','Heat_CVD_Manuscript_covid_period.docx','Pandemic era first hospitalisation counts'),('Supplement_covid_period.md','Supplement_covid_period.docx','Supplementary results')]:
  b,parts=blocks((M/source).read_text());doc=Document();b.configure_document(doc,header,body_size=11.5)
  doc.sections[0].header.paragraphs[0].clear()
  footer=doc.sections[0].footer.paragraphs[0]
  footer.alignment=1
  field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');run=OxmlElement('w:r');text=OxmlElement('w:t');text.text='1';run.append(text);field.append(run);footer._p.append(field)
  for style in ['Title','Heading 1','Heading 2','Heading 3']:
   doc.styles[style].font.name='Times New Roman';doc.styles[style].font.color.rgb=RGBColor(0,0,0)
   for border in list(doc.styles[style]._element.iter(qn('w:pBdr'))):border.getparent().remove(border)
  for kind,lines in parts:
   txt=' '.join(lines)
   if kind=='h0':
    p=doc.add_paragraph(style='Title');p.paragraph_format.keep_with_next=True;p.paragraph_format.space_after=Pt(10);b.add_rich_runs(p,txt,size=16);continue
   if kind in ['h1','h2','h3']:
    p,_=b.add_heading(doc,txt,1 if kind=='h1'else 2,size=11.5);p.style='Heading 1'if kind=='h1'else'Heading 2';continue
   if kind=='equation':
    b.add_body(doc,'log E(Yₜ) = log(dₜ) + α + βXₜ + Σₘ₌₂¹² γₘ I(monthₜ = m) + s(t; 4 df).  (1)',size=11,first_line=False,align='center');continue
   if kind=='table':
    headers,rows=b.parse_table(lines);n=len(headers)
    widths=([.7,2.7,2.7]if n==3 else[.65,1.6,1.925,1.925]if source.startswith('Manuscript')else[1.85]+[4.25/(n-1)]*(n-1))
    if n==5 and source.startswith('Supplement'):widths=[.7,1.6,2.05,.85,.9]if headers[0]=='Outcome'else[1.9,1.05,1.05,1.05,1.05]
    b.add_table(doc,headers,rows,font_size=9.5,widths=widths)
    table=doc.tables[-1];border=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
     node=OxmlElement('w:'+edge);node.set(qn('w:val'),'single');node.set(qn('w:sz'),'4');node.set(qn('w:color'),'D9D9D9');border.append(node)
    table._tbl.tblPr.append(border);continue
   if kind=='image':
    match=re.search(r'\]\(([^)]+)\)',txt);b.add_picture(doc,(M/match.group(1)).resolve(),width=6.1,max_height=3.5);continue
   plain=b.clean_cell(txt)
   if plain.startswith(('Table ','Figure ','Supplementary Table ')):
    b.add_caption(doc,plain,size=10.5);continue
   if re.match(r'^\d+\. ',plain):
    b.add_body(doc,txt,size=10.5,first_line=False,align='left');continue
   b.add_body(doc,txt,size=11.5,first_line=False,align='left')
  doc.core_properties.title=parts[0][1][0];doc.core_properties.author='';doc.core_properties.last_modified_by='';doc.save(M/target);print('Wrote',target)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--audit',action='store_true');a=p.parse_args();audit()if a.audit else build()
