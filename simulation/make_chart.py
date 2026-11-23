#!/usr/bin/env python3
"""Generate en project figures independently."""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path
import zipfile
from copy import deepcopy
import platform
import numpy as np
from run_numpy_validation import pert_standard, run_regime, plt
import matplotlib
from run_validation import PARAMETERS, SEED, N, pert_mean, analytic_expected_mean, make_sensitivity_cases
from turnover_sensitivity import generate as generate_turnover_sensitivity
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import TwoSlopeNorm
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter

def generate(language, labels, fonts, readme):
    OUT = Path(__file__).resolve().parent / 'output' / 'project_charts' / language
    OUT.mkdir(parents=True, exist_ok=True)
    COL = {'A': '#BD5248', 'B': '#3674B5', 'C': '#218574'}
    REG = ('A', 'B', 'C')
    SCEN = ('S1', 'S2', 'S3')
    plt.rcParams.update({'font.size': 12, 'axes.spines.top': False, 'axes.spines.right': False,
                        'axes.labelcolor': '#273747', 'text.color': '#273747', 'axes.edgecolor': '#B8C4CC',
                        'svg.fonttype': 'path', 'pdf.fonttype': 42})

    def csvout(name, rows):
        with (OUT / name).open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    def components(p):
        v = {s: pert_mean(p[s][0])*pert_mean(p[s][1])*pert_mean(p[s][2])/1e6 for s in SCEN}
        v.update(people=pert_mean(p['people'])/1e6, program=pert_mean(p['program'])/1e6,
                 fines=pert_mean(p['oc'])*pert_mean((1e7,4e7,1e8))/1e6)
        assert np.isclose(sum(v.values())*1e6, analytic_expected_mean(p))
        return v

    COMP = {r: components(PARAMETERS[r]) for r in REG}
    csvout('cost_components.csv', [{'regime': r, 'component': k, 'expected_annual_cost_usd': v*1e6}
                                  for r in REG for k,v in COMP[r].items()])
    EVENTS = [{'regime': r, 'scenario': s,
               'expected_successful_events_per_year': pert_mean(PARAMETERS[r][s][0])*pert_mean(PARAMETERS[r][s][1]),
               'mean_loss_per_event_usd': pert_mean(PARAMETERS[r][s][2]),
               'expected_annual_event_loss_usd': COMP[r][s]*1e6} for r in REG for s in SCEN]
    csvout('events_and_severity.csv', EVENTS)

    SAMPLES = {}
    SUMMARY = []
    for case, params in make_sensitivity_cases().items():
        row = {'case': case}
        for r in REG:
            np.random.seed(SEED+ord(r))
            vals = run_regime(r, params[r], pert_standard)
            row[r+'_mean_usd'] = float(vals.mean())
            row[r+'_p95_usd'] = float(np.percentile(vals,95))
            row[r+'_analytic_mean_usd'] = analytic_expected_mean(params[r])
            assert abs(vals.mean()/row[r+'_analytic_mean_usd']-1) < .03
            if case == 'Base': SAMPLES[r] = vals
        SUMMARY.append(row)
    csvout('sensitivity_results.csv', SUMMARY)
    csvout('base_annual_samples.csv', [{'draw': i+1, **{r+'_cost_usd':float(SAMPLES[r][i]) for r in REG}} for i in range(N)])

    xgrid=np.linspace(.2,1.2,101); ygrid=np.linspace(0,1.2,121)
    X,Y=np.meshgrid(xgrid,ygrid)
    fixed_b=sum(v for k,v in COMP['B'].items() if k not in ('S2','people'))
    cmean=sum(COMP['C'].values())
    Z=fixed_b+COMP['B']['S2']*X+COMP['B']['people']*Y-cmean
    csvout('bc_heatmap_grid.csv', [{'b_s2_success_multiplier':float(x), 'b_people_cost_multiplier':float(y),
                                   'b_mean_usd':float((z+cmean)*1e6), 'c_mean_usd':cmean*1e6,
                                   'b_minus_c_mean_usd':float(z*1e6)}
                                  for x,y,z in zip(X.ravel(),Y.ravel(),Z.ravel())])
    assert np.isclose(fixed_b+COMP['B']['S2']+COMP['B']['people'],sum(COMP['B'].values()))
    assert PARAMETERS['B']['S2'][1][2]*max(xgrid)<=1
    threshold_x=(cmean-fixed_b-COMP['B']['people'])/COMP['B']['S2']
    threshold_y=(cmean-fixed_b-.5*COMP['B']['S2'])/COMP['B']['people']
    joint=fixed_b+.5*COMP['B']['S2']+.5*COMP['B']['people']
    # Verify the heatmap against the original model evaluator, including its boundary.
    for xs, ys in [(1,1),(.5,.5),(.2,0),(1.2,1.2),(threshold_x,1),(.5,threshold_y)]:
        p=deepcopy(PARAMETERS['B'])
        a,s,l=p['S2']; p['S2']=(a,tuple(v*xs for v in s),l)
        p['people']=tuple(v*ys for v in p['people'])
        assert np.isclose(analytic_expected_mean(p)/1e6,fixed_b+COMP['B']['S2']*xs+COMP['B']['people']*ys)
    assert np.isclose(fixed_b+COMP['B']['S2']*threshold_x+COMP['B']['people'],cmean)

    TEXT = {language: labels}
    STEMS=['01_cost_composition','02_cost_exceedance','03_sensitivity_comparison','04_bc_break_even','05_events_vs_severity']

    def start(lang, idx, note):
        t=TEXT[lang]
        fig=plt.figure(figsize=(13.33,7.5),facecolor='white')
        fig.text(.075,.94,f'{idx+1:02d}  {t["titles"][idx]}',fontsize=23,weight='bold')
        fig.text(.075,.893,t['subs'][idx],fontsize=11.5,color='#596C7B')
        fig.text(.075,.075,note,fontsize=10,color='#596C7B')
        fig.text(.075,.035,t['foot'],fontsize=9,color='#71818E')
        return fig

    def style(ax):
        ax.set_axisbelow(True); ax.grid(axis='y',color='#E5EBEF',lw=.8)

    def save(fig, idx, lang, pdf):
        stem=OUT/(STEMS[idx]+'_'+lang)
        fig.savefig(str(stem)+'.png',dpi=180)
        fig.savefig(str(stem)+'.svg')
        pdf.savefig(fig)
        plt.close(fig)

    def draw(lang):
        plt.rcParams['font.family']=fonts
        t=TEXT[lang]
        with PdfPages(OUT/f'project_figures_{lang}.pdf') as pdf:
            fig=start(lang,0,t['stacknote']); ax=fig.add_axes([.09,.20,.63,.62]); style(ax)
            bottom=np.zeros(3)
            shades=['#9EBACD','#3B708D','#203E55','#D69958','#8F79AD','#C3C8CD']
            for k,label,color in zip(COMP['A'],t['parts'],shades):
                h=np.array([COMP[r][k] for r in REG]); ax.bar(range(3),h,bottom=bottom,width=.55,label=label,color=color,edgecolor='white',lw=.6)
                for i,v in enumerate(h):
                    if v>=3: ax.text(i,bottom[i]+v/2,f'{v:.1f}',ha='center',va='center',fontsize=10,color='white' if k in ('S2','S3') else '#182C3D')
                bottom+=h
            for i,v in enumerate(bottom): ax.text(i,v+2,f'${v:.2f}M',ha='center',weight='bold',fontsize=14)
            ax.set(xticks=range(3),xticklabels=t['names'],ylabel=t['cost'],ylim=(0,112))
            ax.legend(loc='upper left',bbox_to_anchor=(1.02,1),frameon=False,labelspacing=1.5)
            save(fig,0,lang,pdf)

            fig=start(lang,1,t['risknote']); ax=fig.add_axes([.09,.19,.65,.63]); style(ax)
            for r in REG:
                vals=np.sort(SAMPLES[r])/1e6
                ax.step(vals,np.arange(N,0,-1)/N,where='pre',color=COL[r],lw=2,label=t['names'][REG.index(r)])
                p95=np.percentile(vals,95); ax.plot(p95,.05,'o',color=COL[r],ms=6)
            ax.axhline(.05,color='#87929A',ls='--',lw=1)
            ax.text(3,.065,'5%',fontsize=10,color='#596C7B')
            ax.set(xlabel=t['cost'],ylabel=t['prob'],ylim=(0,1.01),xlim=(0,max(v.max() for v in SAMPLES.values())/1e6*1.02))
            ax.yaxis.set_major_formatter(PercentFormatter(1))
            ax.legend(loc='upper left',bbox_to_anchor=(1.01,1),frameon=False)
            for i,r in enumerate(REG):
                fig.text(.77,.56-i*.065,f'{r}  P95  ${SUMMARY[0][r+"_p95_usd"]/1e6:.2f}M',color=COL[r],fontsize=12,weight='bold')
            save(fig,1,lang,pdf)

            fig=start(lang,2,t['sensnote'])
            for j,stat in enumerate(('mean','p95')):
                ax=fig.add_axes([.265+j*.365,.22,.305,.57]); style(ax)
                yy=np.arange(4)
                for i,r in enumerate(REG):
                    vals=[v[r+'_'+stat+'_usd']/1e6 for v in SUMMARY]
                    bars=ax.barh(yy+(i-1)*.23,vals,height=.21,color=COL[r],label=r)
                    ax.bar_label(bars,fmt='%.1f',padding=3,fontsize=10)
                ax.set(yticks=yy,yticklabels=t['cases'] if j==0 else ['']*4,xlabel=t['cost'],xlim=(0,175 if j else 116),title=t[stat])
                ax.invert_yaxis(); ax.grid(False); ax.grid(axis='x',color='#E5EBEF'); ax.tick_params(axis='y',length=0)
            fig.legend(handles=[Line2D([0],[0],color=COL[r],lw=8,label=t['names'][i]) for i,r in enumerate(REG)],loc='lower center',bbox_to_anchor=(.53,.115),ncol=3,frameon=False)
            save(fig,2,lang,pdf)

            fig=start(lang,3,t['heatnote']); ax=fig.add_axes([.09,.21,.67,.61])
            im=ax.pcolormesh(X,Y,Z,shading='auto',cmap='RdBu_r',norm=TwoSlopeNorm(vmin=-60,vcenter=0,vmax=60),rasterized=True)
            contour=ax.contour(X,Y,Z,levels=[0],colors='#152D40',linewidths=2)
            ax.clabel(contour,fmt={0:t['tie']},inline=True,fontsize=11)
            for x,y,label,offset in [(1,1,t['base'],(-55,18)),(.5,.5,t['joint'],(16,-30))]:
                ax.scatter(x,y,s=150,marker='*',color='#152D40',edgecolor='white',zorder=5)
                ax.annotate(label,(x,y),xytext=offset,textcoords='offset points',fontsize=12,weight='bold',bbox=dict(boxstyle='round,pad=.3',fc='white',ec='none',alpha=.92))
            ax.text(.25,.10,t['bwin'],fontsize=17,weight='bold',color='#123D68')
            ax.text(.91,.13,t['cwin'],fontsize=17,weight='bold',color='#8C3432')
            ax.set(xlabel=t['xheat'],ylabel=t['yheat'],xlim=(.2,1.2),ylim=(0,1.2))
            cb=fig.colorbar(im,cax=fig.add_axes([.80,.24,.025,.54])); cb.set_label(t['delta'])
            save(fig,3,lang,pdf)

            fig=start(lang,4,t['evnote']); ax=fig.add_axes([.09,.20,.85,.62]); style(ax)
            positions={('A','S1'):(12.0,1.65),('B','S1'):(2.1,1.75),('A','S2'):(22.2,3.65),
                       ('B','S2'):(18.2,2.3),('C','S2'):(14.7,3.65),
                       ('A','S3'):(8.0,6.25),('B','S3'):(5.1,7.0),('C','S3'):(3.7,5.1)}
            for e in EVENTS:
                r,s=e['regime'],e['scenario']; x=e['expected_successful_events_per_year']; y=e['mean_loss_per_event_usd']/1e6
                if (r,s)==('C','S1'): continue
                if (r,s)==('B','S1'):
                    ax.plot(x,y,marker='o',ms=12,fillstyle='left',markerfacecolor=COL['B'],markerfacecoloralt=COL['C'],markeredgecolor='white')
                    label=f'B = C · S1\n{x:.2f} / ${y:.2f}M'
                else:
                    ax.scatter(x,y,s=110,marker={'S1':'o','S2':'s','S3':'^'}[s],color=COL[r],edgecolor='white',zorder=3)
                    label=f'{r} · {s}\n{x:.2f} / ${y:.2f}M'
                ax.annotate(label,(x,y),xytext=positions[r,s],ha='center',va='center',fontsize=10.5,color=COL[r],
                            arrowprops={'arrowstyle':'-','color':'#84939E','lw':.8})
            ax.set(xlabel=t['freq'],ylabel=t['sev'],xlim=(0,27),ylim=(0,7.7))
            ax.legend(handles=[Line2D([0],[0],marker='o',linestyle='',color=COL[r],label=t['names'][i]) for i,r in enumerate(REG)],loc='upper right',frameon=False)
            save(fig,4,lang,pdf)
            generate_turnover_sensitivity(OUT, pdf)

    draw(language)
    manifest={'n':N,'seed_per_regime':{r:SEED+ord(r) for r in REG},'input_parameters':PARAMETERS,
              'environment':{'python':platform.python_version(),'numpy':np.__version__,'matplotlib':matplotlib.__version__},
              'methods':{'figures_1_4_5':'Analytical expectation, independent standard Beta-PERT inputs',
                         'figures_2_3':'Monte Carlo, existing corrected NumPy simulator',
                         'turnover_sensitivity':'Illustrative analytical first-year scenario; replaces B turnover cost while C stays at baseline'},
              'heatmap':{'scope':'Only B S2 success triples and people triples are multiplied; all other inputs fixed',
                         'comparison':'Expected annual total cost only; not P95 or probability B beats C',
                         'b_s2_multiplier_at_equal_cost_with_people_unchanged':threshold_x,
                         'b_people_multiplier_at_equal_cost_with_s2_halved':threshold_y,
                         'joint_half_b_mean_usd':joint*1e6,'c_baseline_mean_usd':cmean*1e6},
              'source_sha256':{name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                               for name in ['run_validation.py', 'run_numpy_validation.py', 'make_chart.py', 'turnover_sensitivity.py', 'pyproject.toml', 'uv.lock', 'README.md']}}
    (OUT/'methods_and_inputs.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    (OUT/'README.txt').write_text(readme, encoding='utf-8')
    print(json.dumps(manifest['heatmap'],indent=2))
    with zipfile.ZipFile(OUT/'project_charts_bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.iterdir()):
            if p.is_file() and p.suffix!='.zip': z.write(p,p.name)
        for name in ['run_validation.py', 'run_numpy_validation.py', 'make_chart.py', 'turnover_sensitivity.py', 'pyproject.toml', 'uv.lock', 'README.md']:
            z.write(Path(__file__).parent/name,'scripts/'+name)
    print('Saved single-language PNG/SVG figures, PDFs, review CSVs, manifest, and ZIP to',OUT)


TEXT = {'names': ['A  No additional program', 'B  Maximum surveillance', 'C  Privacy-preserving'],
 'foot': 'Scenario model with elicited inputs | USD | Not observed BNY losses',
 'titles': ['Where annual costs come from',
            'How often costs exceed a threshold',
            'What changes when assumptions change',
            'When does B become cheaper than C?',
            'Frequency and severity of successful events'],
 'subs': ['Expected annual costs, calculated analytically from corrected Beta-PERT inputs',
          '20,000 simulated years per regime | Corrected Beta-PERT | Fixed seeds',
          'Each sensitivity changes one factor; all other inputs retain their baseline settings',
          'Joint sensitivity of expected annual total cost | C stays at baseline',
          'Expected successful events per year versus mean loss per event | Analytical values'],
 'cost': 'Annual cost (USD millions)',
 'mean': 'Mean annual cost',
 'p95': '95th-percentile annual cost',
 'parts': ['S1  USB theft',
           'S2  Email/cloud theft',
           'S3  Admin sabotage',
           'Turnover cost',
           'Program',
           'Expected fines'],
 'cases': ['Baseline',
           'B: remove attempt uplift',
           'B: halve S2 success share',
           'B: halve employee cost'],
 'xheat': 'B S2 success-share multiplier (1.0 = baseline)',
 'yheat': 'B employee-cost multiplier (1.0 = baseline)',
 'delta': 'Expected annual cost B minus C (USD millions)',
 'base': 'Baseline',
 'joint': 'Both halved',
 'tie': 'Equal expected cost',
 'bwin': 'B cheaper',
 'cwin': 'C cheaper',
 'heatnote': 'Only B S2 success shares and employee costs vary. Attempts retain uplift. This chart '
             'compares means, not P95.',
 'freq': 'Expected successful events per year',
 'sev': 'Mean loss per successful event (USD millions)',
 'evnote': 'S1 = USB theft | S2 = email/cloud theft | S3 = admin sabotage. Severity means are '
           'shared across A/B/C.',
 'prob': 'Probability annual cost exceeds threshold',
 'stacknote': 'Segments show expected annual contributions; expected fines are probability × mean '
              'fine.',
 'risknote': 'P95 marks the cost exceeded in about 5% of modeled years; it is not a confidence '
             'interval.',
 'sensnote': 'Individual changes to B; combined changes are shown in Figure 4.'}


def main():
    generate('en', TEXT, ['DejaVu Sans'], 'CRM project charts (en)\nSix figures: composition, exceedance, individual sensitivities, B/C break-even,\nevent frequency and severity, and illustrative turnover sensitivity. Currency: USD millions.\nFigures 1, 4, 5 and turnover sensitivity use analytical means; 2, 3 use 20,000 simulated years.\nEmployee costs represent illustrative turnover only; triage and morale costs are excluded.\nThe turnover scenario varies B while C stays at baseline.\nIntention gaps are assumptions, not proven effects; conversion and hiring costs are assumptions.\nFigure 4 and turnover sensitivity compare means only, not P95.\nRun from the project root: cd simulation && uv run --frozen python make_chart.py\nRun from the extracted bundle: cd scripts && uv run --frozen python make_chart.py\nRequires NumPy and Matplotlib. Font: DejaVu Sans.\n')


if __name__ == "__main__":
    main()
