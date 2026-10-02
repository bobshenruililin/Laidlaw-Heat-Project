#!/usr/bin/env python3
"""Plot already-approved annual aggregates; never read monthly health records."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((ROOT/'outputs/tables/cvd_descriptive_annual_totals.csv').open()))
assert all(r['data_status']=='HA_APPROVED_AGGREGATE'for r in rows)
fig,ax=plt.subplots(figsize=(8.2,4.25),layout='constrained')
ax.axvspan(2019.5,2023.5,color='#eeeeee',zorder=0)
for outcome,label,color,marker in [('chd','After CHD diagnosis','#275d8a','o'),('hf','After HF diagnosis','#9a5931','s')]:
 r=sorted((x for x in rows if x['outcome']==outcome),key=lambda x:int(x['year']));base=float(r[0]['total_events'])
 ax.plot([int(x['year'])for x in r],[100*float(x['total_events'])/base for x in r],label=label,color=color,marker=marker,lw=2,ms=5)
ax.set(xlim=(2012.7,2023.4),ylim=(0,110),xticks=range(2013,2024),ylabel='Annual recorded counts  (2013 = 100)',xlabel='Calendar year')
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.legend(frameon=False,loc='upper right');ax.tick_params(labelsize=9)
p=ROOT/'figures/covid_period/figure_annual_counts_20261002.png';fig.savefig(p,dpi=220);plt.close(fig);print(p)
