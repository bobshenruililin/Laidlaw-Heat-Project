#!/usr/bin/env python3
"""Evidence-only figures from released tables. No governed inputs or model fitting.

Run from any directory. Source snapshots exclude the obsolete population-rate
columns in the legacy annual table. Conceptual edges are hypotheses, not effects.
"""
from pathlib import Path
import csv, hashlib, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.ticker import FuncFormatter, NullLocator

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'figures/covid_period'
BLUE, ORANGE, INK = '#0072B2', '#D55E00', '#253746'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10,
                     'svg.fonttype':'none', 'pdf.fonttype':42,
                     'axes.spines.top':False, 'axes.spines.right':False})
manifest = {'data_status':'HA_APPROVED_AGGREGATE',
            'operations':'Released summary-table plotting only; no model fits',
            'figures':[]}

def read(rel):
    rows = list(csv.DictReader((ROOT/rel).open()))
    assert rows and all(r['data_status']=='HA_APPROVED_AGGREGATE' for r in rows), rel
    return rows

def write_source(name, rows, fields):
    target = OUT / (name+'_source.csv')
    with target.open('w', newline='') as f:
        w = csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader()
        w.writerows({k:r[k] for k in fields} for r in rows)
    return target

def save(fig,name,sources,description):
    outputs=[]
    for fmt in ['png','pdf','svg']:
        p=OUT/(name+'.'+fmt)
        fig.savefig(p,dpi=240,bbox_inches='tight',facecolor='white')
        if fmt == 'svg':
            p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
        outputs.append({'path':str(p.relative_to(ROOT)), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    manifest['figures'].append({'name':name,'description':description,
        'sources':[{'path':s,'sha256':hashlib.sha256((ROOT/s).read_bytes()).hexdigest()} for s in sources],
        'outputs':outputs})
    plt.close(fig)

def annual():
    source='outputs/tables/cvd_descriptive_annual_totals.csv'; rows=read(source)
    assert len(rows)==22 and all(int(r['n_months'])==12 for r in rows)
    for outcome in ['chd','hf']:
        assert sorted(int(r['year']) for r in rows if r['outcome']==outcome)==list(range(2013,2024))
    name='figure_annual_counts_20261002'
    write_source(name,rows,['outcome','year','total_events','n_months','data_status'])
    fig,axes=plt.subplots(1,2,figsize=(10.3,4.1),layout='constrained')
    for ax,outcome,label,color in zip(axes,['chd','hf'],['After CHD diagnosis','After HF diagnosis'],[BLUE,ORANGE]):
        subset=sorted((r for r in rows if r['outcome']==outcome),key=lambda r:int(r['year']))
        years=[int(r['year']) for r in subset]; counts=[int(r['total_events']) for r in subset]
        ax.axvspan(2019.5,2023.5,color='#F1F1F1',zorder=0)
        ax.plot(years,counts,color=color,marker='o',lw=2,ms=4)
        ax.set(title=label,xlabel='Calendar year',ylabel='Annual recorded first-hospitalisation count',
               xlim=(2012.7,2023.4),ylim=(0,max(counts)*1.12),xticks=[2013,2015,2017,2019,2021,2023])
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x:,.0f}'))
        ax.grid(axis='y',alpha=.18); ax.tick_params(axis='both',labelsize=9)
        for y in [2013,2019,2020,2023]:
            n=counts[years.index(y)]
            ax.annotate(f'{n:,}',(y,n),xytext=(0,9),textcoords='offset points',ha='center',fontsize=8,color=INK)
    fig.suptitle('Recorded counts declined before 2020 and approached 2019 levels by 2023',fontsize=12)
    save(fig,name,[source], 'Annual raw counts. Shading marks calendar years 2020-2023, not an identified intervention. Panel y-axis ranges differ. No person-time or incidence shown.')

def nested():
    source='outputs/tables/cvd_trend_depletion_sensitivity.csv'; allrows=read(source)
    exposures=[('cold_days','Cold days'),('very_hot_days','Very hot days'),('hot_nights','Hot nights')]
    rows=[r for r in allrows if r['exposure'] in dict(exposures) and r['scenario'] in ['pre_covid','baseline_ns4']]
    assert len(rows)==12
    assert all(float(r['scale'])==5 for r in rows)
    name='figure_nested_window_associations_20261002'
    write_source(name,rows,['outcome','exposure','scenario','n_months','rr','rr_low','rr_high','scale','data_status'])
    fig,axes=plt.subplots(1,2,figsize=(10.3,4.7),sharey=True,layout='constrained')
    for ax,outcome,label in zip(axes,['chd','hf'],['After CHD diagnosis','After HF diagnosis']):
        ax.axvline(1,color='#79858B',lw=1)
        for i,(exposure,_) in enumerate(exposures):
            for scenario,offset,color,marker,legend in [('pre_covid',.15,BLUE,'o','2013-2019 (84 months)'),('baseline_ns4',-.15,ORANGE,'s','2013-2023 (132 months)')]:
                r=next(r for r in rows if r['outcome']==outcome and r['exposure']==exposure and r['scenario']==scenario)
                val,lo,hi=map(float,[r['rr'],r['rr_low'],r['rr_high']]); assert lo<=val<=hi
                ax.errorbar(val,2-i+offset,xerr=[[val-lo],[hi-val]],fmt=marker,color=color,capsize=3,ms=5,lw=1.5,label=legend if i==0 else None)
        ax.set(xscale='log',xlim=(.90,1.20),ylim=(-.95,2.55),title=label,
               yticks=[2,1,0],yticklabels=[l for _,l in exposures],xlabel='Count ratio per five official days')
        ax.set_xticks([.90,.95,1,1.05,1.10,1.15,1.20]);ax.set_xticklabels(['0.90','0.95','1.00','1.05','1.10','1.15','1.20'],fontsize=8)
        ax.xaxis.set_minor_locator(NullLocator())
        ax.grid(axis='x',alpha=.15)
    axes[0].legend(frameon=False,fontsize=9,loc='lower left')
    fig.suptitle('Nested analysis windows: estimates with Newey-West lag-6 95% intervals',fontsize=12)
    fig.supxlabel('The 84 months are part of the 132 months. No independent post-period estimate or difference test.',fontsize=9)
    save(fig,name,[source], 'Six official-count exposure/outcome pairs, two overlapping fits. Recomputed spline bases differ. Full 12-contrast family has BH q>0.19. No significance symbols or post-period contrast.')

def sensitivity():
    source='outputs/tables/cvd_trend_depletion_sensitivity.csv'; allrows=read(source)
    scenarios=['baseline_ns4','trend_ns3','trend_ns6','trend_ns8','year_fixed_effects','drop_first_12_months','drop_first_24_months']
    labels=['4-df trend (baseline)','3-df trend','6-df trend','8-df trend','Year fixed effects','Omit first 12 months','Omit first 24 months']
    pairs=[('hf','cold_days','HF cold days'),('chd','hot_nights','CHD hot nights')]
    rows=[r for r in allrows if (r['outcome'],r['exposure']) in [(a,b) for a,b,_ in pairs] and r['scenario'] in scenarios]
    assert len(rows)==14
    assert all(float(r['scale'])==5 for r in rows)
    name='figure_calendar_sensitivity_20261002'
    write_source(name,rows,['outcome','exposure','scenario','n_months','rr','rr_low','rr_high','residual_acf1','data_status'])
    fig,axes=plt.subplots(1,2,figsize=(10.6,4.8),sharey=True,layout='constrained')
    for ax,(outcome,exposure,title),color in zip(axes,pairs,[ORANGE,BLUE]):
        ax.axvline(1,color='#79858B',lw=1)
        for i,scenario in enumerate(scenarios):
            r=next(r for r in rows if r['outcome']==outcome and r['exposure']==exposure and r['scenario']==scenario)
            val,lo,hi=map(float,[r['rr'],r['rr_low'],r['rr_high']]);assert lo<=val<=hi
            ax.errorbar(val,6-i,xerr=[[val-lo],[hi-val]],fmt='o',color=color,capsize=3,ms=5,lw=1.5)
        ax.set(title=title,xscale='log',ylim=(-.6,6.6),yticks=range(7),yticklabels=labels[::-1],xlabel='Count ratio per five official days')
        ticks=[.95,1,1.05,1.10,1.15] if outcome=='hf' else [.98,1,1.02,1.04,1.06]
        ax.set_xticks(ticks);ax.set_xticklabels([f'{x:.2f}' for x in ticks],fontsize=9)
        ax.xaxis.set_minor_locator(NullLocator())
        ax.set_xlim((.95,1.16) if outcome=='hf' else (.978,1.07));ax.grid(axis='x',alpha=.15)
    fig.suptitle('Calendar and start-window sensitivity of two discussed associations',fontsize=12)
    fig.supxlabel('Newey-West lag-6 95% intervals. These are selected diagnostics, not a new discovery family.',fontsize=9)
    save(fig,name,[source], 'Seven fixed displays: baseline plus six calendar/start-window checks for the two historically discussed contrasts. The phase-adjusted intercept fit remains in Supplement Table S3. Other exposures remain in the complete source panel. No refitting or preferred-fit selection.')

def observation():
    name='figure_observation_process_20261002'
    fig,ax=plt.subplots(figsize=(10.6,5.2));ax.set(xlim=(0,12),ylim=(0,6));ax.axis('off')
    nodes={
        'context':(1.8,3.05,2.6,.85,'Pandemic-era context\npolicy, infection, weather'),
        'disease':(5.8,4.95,2.5,.85,'Underlying clinical state\n(unobserved here)'),
        'care':(5.8,3.05,2.5,.85,'Hospital contact\n(any admission cause)'),
        'record':(10.05,3.05,2.65,.85,'Recorded first\nhospitalisation count'),
        'coding':(10.05,4.95,2.65,.85,'CHD/HF diagnosis record /\ncoding / extraction'),
        'risk':(5.8,1.0,2.5,.9,'Entry / eligibility /\nprior events / exit'),
        'death':(1.8,1.0,2.6,.9,'Competing death /\nloss of observation')}
    for key,(x,y,w,h,text) in nodes.items():
        ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.05,rounding_size=0.08',fc='#E7F1F7' if key=='record' else '#F3F5F6',ec=BLUE if key=='record' else '#88969E',lw=1))
        ax.text(x,y,text,ha='center',va='center',fontsize=10,color=INK)
    # Each edge is a candidate dependence for design, not an identified effect.
    edges=[('context','disease'),('context','care'),('context','death'),('context','risk'),('disease','care'),('disease','coding'),('care','record'),('coding','record'),('risk','record'),('death','risk')]
    for a,b in edges:
        x,y,w,h,_=nodes[a];xx,yy,ww,hh,_=nodes[b]
        dx,dy=xx-x,yy-y
        if abs(dx)>abs(dy): start=(x+(w/2+.06)*(1 if dx>0 else -1),y); end=(xx-(ww/2+.06)*(1 if dx>0 else -1),yy)
        else:start=(x,y+(h/2+.06)*(1 if dy>0 else -1));end=(xx,yy-(hh/2+.06)*(1 if dy>0 else -1))
        bend=0
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=12,color='#61747F',lw=1.2,connectionstyle=f'arc3,rad={bend}'))
    ax.text(6,5.95,'Conceptual observation process',ha='center',fontsize=13,color=INK,weight='bold')
    ax.text(6,.05,'Candidate pathways only. Counted stays follow a diagnosis record; their admission cause is unavailable.',ha='center',fontsize=9,color=INK)
    edgepath=OUT/(name+'_source.csv')
    with edgepath.open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['from','to','status']);w.writerows((a,b,'CONCEPTUAL_HYPOTHESIS') for a,b in edges)
    save(fig,name,['reports/data_receipt_2026-08-07.md'], 'Conceptual design schematic, not a validated cohort flow or identified causal DAG. Candidate pathways coexist, signs unspecified; no clinical quantities or cohort row counts invented.')
    manifest['figures'][-1]['data_status']='CONCEPTUAL_HYPOTHESIS'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    observation();annual();nested();sensitivity()
    (OUT/'evidence_figures_manifest_20261002.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'figures':len(manifest['figures']),'output_directory':str(OUT)}))

if __name__=='__main__':main()
