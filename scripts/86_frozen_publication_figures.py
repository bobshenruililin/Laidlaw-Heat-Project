#!/usr/bin/env python3
"""Plot immutable, approved summary tables without fitting or reading health rows.

All new outputs go to figures/covid_period/frozen_publication. Fixed metadata,
SVG ids and LF source snapshots support byte reproducibility in one runtime.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import platform
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, NullLocator

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'figures/covid_period/frozen_publication'
ANCHOR='7060606fbe44b14b6b2893929781ac477cea1d46'
TABLES={
 'annual':'outputs/tables/cvd_descriptive_annual_totals.csv',
 'core':'outputs/tables/cvd_core_robust_estimates.csv',
 'calendar':'outputs/tables/cvd_trend_depletion_sensitivity.csv'}
FROZEN_HASHES={
 'annual':'2d4997276d77e28761083117e292f438506d07db639deba5bc17c1843e4862e8',
 'core':'6acfc6f5082780c681c05c48b5953579ad7095d379429dc6125230c8c0824dd4',
 'calendar':'061158111bbc79478b8cb54f27687447c213fd1bfc13efe9cf3309996f348e5e'}
BLUE,ORANGE,INK='#0072B2','#D55E00','#243746'
WIDTH=180/25.4
DATE=datetime(2026,10,2,tzinfo=timezone.utc)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,
 'axes.titlesize':10,'axes.labelsize':9,'xtick.labelsize':9,'ytick.labelsize':9,
 'legend.fontsize':9,'pdf.fonttype':42,'svg.fonttype':'none',
 'svg.hashsalt':'laidlaw-frozen-publication-20261002',
 'axes.spines.top':False,'axes.spines.right':False,
 'figure.constrained_layout.w_pad':.04,'figure.constrained_layout.h_pad':.04})

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(key):
 rows=list(csv.DictReader((ROOT/TABLES[key]).open()))
 assert rows and all(r['data_status']=='HA_APPROVED_AGGREGATE' for r in rows)
 return rows
def source(name,rows,fields):
 p=OUT/(name+'_source.csv')
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
  w.writerows({k:r.get(k,'') for k in fields} for r in rows)
 return p
def save(fig,name,inputkeys,sourcepath,description):
 paths=[]
 for fmt in ['png','svg','pdf']:
  p=OUT/(name+'.'+fmt)
  metadata=({'Title':name,'Author':'Laidlaw Heat Project',
             'Creator':'Frozen approved-table plotting; no model fitting',
             'CreationDate':DATE,'ModDate':DATE} if fmt=='pdf' else
            {'Title':name,'Date':'2026-10-02','Creator':'Laidlaw frozen-table plotting'} if fmt=='svg' else
            {'Title':name,'Software':'Laidlaw frozen-table plotting'})
  fig.savefig(p,dpi=300,facecolor='white',metadata=metadata)
  if fmt=='svg':
   p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
  paths.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
 plt.close(fig)
 return {'name':name,'description':description,'data_status':'HA_APPROVED_AGGREGATE',
  'width_mm':180,'minimum_font_pt':9,
  'inputs':[{'path':TABLES[k],'sha256':sha(ROOT/TABLES[k])} for k in inputkeys],
  'source_snapshot':{'path':str(sourcepath.relative_to(ROOT)),'sha256':sha(sourcepath)},
  'outputs':paths}

def setup_forest(ax,ticks,limits):
 ax.axvline(1,color='#89969C',lw=.8,zorder=0)
 ax.set_xscale('log');ax.set_xlim(*limits)
 ax.set_xticks(ticks);ax.set_xticklabels([f'{x:.2f}' for x in ticks])
 ax.xaxis.set_minor_locator(NullLocator());ax.grid(axis='x',alpha=.15)
 ax.tick_params(axis='y',length=0)
def interval(ax,row,y,color,marker):
 val,lo,hi=map(float,[row['rr'],row['rr_low'],row['rr_high']])
 assert 0<lo<=val<=hi
 ax.errorbar(val,y,xerr=[[val-lo],[hi-val]],fmt=marker,color=color,
             capsize=2.2,ms=4,lw=1.15,zorder=2)
def unique(rows,**selection):
 matches=[r for r in rows if all(r[k]==v for k,v in selection.items())]
 assert len(matches)==1,selection
 return matches[0]

def annual(rows):
 assert len(rows)==22
 name='annual_counts'
 snapshot=source(name,rows,['outcome','year','total_events','n_months','data_status'])
 fig,axes=plt.subplots(1,2,figsize=(WIDTH,3.25),layout='constrained')
 for ax,o,title,col,marker,lim in zip(axes,['chd','hf'],
      ['A  After CHD diagnosis','B  After HF diagnosis'],
      [BLUE,ORANGE],['o','s'],[(0,26500),(0,4800)]):
  rs=sorted((r for r in rows if r['outcome']==o),key=lambda r:int(r['year']))
  years=[int(r['year']) for r in rs];vals=[int(r['total_events']) for r in rs]
  assert years==list(range(2013,2024)) and all(int(r['n_months'])==12 for r in rs)
  ax.axvspan(2019.5,2023.5,color='#F0F0F0',zorder=0)
  ax.plot(years,vals,color=col,marker=marker,lw=1.5,ms=3.5)
  ax.set(title=title,xlabel='Calendar year',ylabel='Recorded hospitalisations (annual)',
         xlim=(2012.7,2023.4),ylim=lim,xticks=[2013,2015,2017,2019,2021,2023])
  ax.yaxis.set_major_formatter(FuncFormatter(lambda v,pos:f'{v:,.0f}'))
  ax.grid(axis='y',alpha=.15)
  for year in [2013,2019,2020,2023]:
   val=vals[years.index(year)]
   offset=(3,6) if year==2013 else (0,-14) if year==2020 else (0,6)
   ax.annotate(f'{val:,}',(year,val),xytext=offset,textcoords='offset points',
               ha='left' if year==2013 else 'right' if year==2023 else 'center',
               fontsize=9,color=INK)
 fig.get_layout_engine().set(rect=(0,.04,1,.96))
 fig.text(.5,.012,'Annual counts; vertical ranges differ. Shading: 2020-2023.',ha='center',fontsize=9)
 return save(fig,name,['annual'],snapshot,'Two zero-origin annual count panels, no territory population rates or inferred monthly records.')

def complete(core):
 rows=[r for r in core if r['manuscript_role']=='amended_core_candidate']
 assert len(rows)==12
 assert all(r['family']=='negative_binomial' and r['offset_policy']=='days_only'
            and r['se_method']=='NeweyWest_lag6' and int(r['n_months'])==132 for r in rows)
 assert all(float(r['q_value_core_bh'])>.19 for r in rows)
 name='complete_weather'
 snapshot=source(name,rows,['outcome','pathway_id','exposure','scale','family','offset_policy',
  'se_method','n_months','rr','rr_low','rr_high','p_value','q_value_core_bh','manuscript_role','data_status'])
 fig,axes=plt.subplots(2,2,figsize=(WIDTH,4.75),layout='constrained')
 groups=[('mean_temp','Mean temperature'),('mean_tmax','Mean maximum'),('mean_tmin','Mean minimum')], [('cold_days','Cold days'),('very_hot_days','Very hot days'),('hot_nights','Hot nights')]
 for ir,group in enumerate(groups):
  for ic,(o,col,marker) in enumerate([('chd',BLUE,'o'),('hf',ORANGE,'s')]):
   ax=axes[ir,ic]
   limits=(.94,1.025) if ir==0 else (.94,1.16)
   ticks=[.95,1,1.02] if ir==0 else [.95,1,1.10,1.15]
   setup_forest(ax,ticks,limits)
   ticklabels=[]
   for i,(exposure,label) in enumerate(group):
    r=unique(rows,outcome=o,exposure=exposure)
    assert float(r['scale'])==(1 if ir==0 else 5)
    interval(ax,r,2-i,col,marker)
    ticklabels.append(f"{label}\nq = {float(r['q_value_core_bh']):.3f}")
   ax.set(yticks=[2,1,0],yticklabels=ticklabels,ylim=(-.6,2.6),
          title=f"{'ABCD'[ir*2+ic]}  After {o.upper()} diagnosis\n"+('Continuous temperature' if ir==0 else 'Official day counts'),
          xlabel='Count ratio per 1°C' if ir==0 else 'Count ratio per five official days')
 fig.get_layout_engine().set(rect=(0,.075,1,.925))
 fig.text(.5,.036,'Full 132 months. Newey-West lag-6 95% intervals.',ha='center',fontsize=9)
 fig.text(.5,.010,'BH q-values cover all 12 contrasts; horizontal ranges differ by row.',ha='center',fontsize=9)
 return save(fig,name,['core'],snapshot,'Complete twelve baseline NW6 count ratios. Units separated into four panels, exact q-values shown to three decimals, no significance stars.')

def criticism(calendar,core):
 scenarios=['baseline_ns4','trend_ns3','trend_ns6','trend_ns8','year_fixed_effects','drop_first_12_months','drop_first_24_months']
 labels=['4 df (baseline)','3 df','6 df','8 df','Year fixed effects','Omit first 12 months','Omit first 24 months']
 pairs=[('hf','cold_days','HF cold days',ORANGE,'s'),('chd','hot_nights','CHD hot nights',BLUE,'o')]
 fullcore=[r for r in core if r['family']=='negative_binomial' and r['offset_policy']=='days_only'
           and r['model_structure']=='single_exposure' and int(r['n_months'])==132]
 assert len(fullcore)==48
 methods=['model','HC1','NeweyWest_lag3','NeweyWest_lag6']
 methodlabels=['Model-based','HC1','Newey-West lag 3','Newey-West lag 6']
 selected=[]
 fig,axes=plt.subplots(2,2,figsize=(WIDTH,5.3),layout='constrained')
 for ic,(o,exposure,label,col,marker) in enumerate(pairs):
  limits=(.95,1.16) if o=='hf' else (.98,1.06)
  ticks=[.95,1,1.05,1.10,1.15] if o=='hf' else [.98,1,1.02,1.04,1.06]
  ax=axes[0,ic];setup_forest(ax,ticks,limits)
  for i,scenario in enumerate(scenarios):
   r=unique(calendar,outcome=o,exposure=exposure,scenario=scenario)
   interval(ax,r,6-i,col,marker)
   selected.append({**r,'display_type':'calendar','se_method':'NeweyWest_lag6'})
  ax.set(title=f"{'AB'[ic]}  {label}\nCalendar and window checks",yticks=list(range(7)),
         yticklabels=labels[::-1],ylim=(-.6,6.6),xlabel='Count ratio per five official days')
  ax=axes[1,ic];setup_forest(ax,ticks,limits)
  coefficients=[]
  for i,method in enumerate(methods):
   r=unique(fullcore,outcome=o,exposure=exposure,se_method=method)
   interval(ax,r,3-i,col,marker);coefficients.append(float(r['estimate']))
   selected.append({**r,'display_type':'uncertainty','scenario':'baseline_ns4'})
  assert max(coefficients)-min(coefficients)<1e-14
  ax.set(title=f"{'CD'[ic]}  {label}\nBaseline uncertainty ladder",yticks=list(range(4)),
         yticklabels=methodlabels[::-1],ylim=(-.6,3.6),xlabel='Count ratio per five official days')
 assert len(selected)==22
 name='model_criticism'
 snapshot=source(name,selected,['display_type','outcome','exposure','scenario','se_method',
  'family','offset_policy','n_months','scale','rr','rr_low','rr_high','data_status'])
 fig.get_layout_engine().set(rect=(0,.05,1,.95))
 fig.text(.5,.010,'95% intervals. Horizontal ranges differ by outcome; no new fits.',ha='center',fontsize=9)
 return save(fig,name,['calendar','core'],snapshot,'Four panels: two seven-scenario calendar displays and two four-method baseline uncertainty ladders. Phase-adjustment and complete 48-interval ladder remain in supplement.')

def main():
 before={k:sha(ROOT/v) for k,v in TABLES.items()}
 assert before==FROZEN_HASHES,'Approved tables differ from the scientific anchor; refusing to redraw.'
 OUT.mkdir(parents=True,exist_ok=True)
 figs=[annual(read('annual')),complete(read('core')),criticism(read('calendar'),read('core'))]
 assert before=={k:sha(ROOT/v) for k,v in TABLES.items()}
 manifest={'scientific_anchor_commit':ANCHOR,'data_status':'HA_APPROVED_AGGREGATE',
  'operations':'Selection, display and immutable approved-table plotting only. No model fits or secure inputs.',
  'runtime':{'python':platform.python_version(),'matplotlib':matplotlib.__version__},
  'metadata_date':'2026-10-02 (fixed for reproducible rendering)',
  'generator':{'path':str(Path(__file__).resolve().relative_to(ROOT)),'sha256':sha(Path(__file__))},
  'source_files_unchanged':True,'figures':figs}
 (OUT/'publication_figures_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({'figures':len(figs),'out':str(OUT)}))

if __name__=='__main__':main()
