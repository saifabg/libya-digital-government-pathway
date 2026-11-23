"""Models of online-service provision (OSI) across countries and editions, and Libya's shortfall.

Run from the study folder:  python -I code/03_models.py
Outputs (results/): models.txt, residuals_six_countries.csv, largest_shortfalls.csv, fig_residuals.png
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

SIX = {'LBY': 'Libya', 'TUN': 'Tunisia', 'EGY': 'Egypt', 'ZAF': 'South Africa', 'SAU': 'Saudi Arabia', 'KOR': 'Republic of Korea'}
df = pd.read_csv(os.path.join('data', 'panel_un_wb.csv'))

# Structural oil dependence: mean oil rents 2010-2021 (World Bank series ends in 2021)
wb = pd.read_csv(os.path.join('data', 'raw', 'worldbank_indicators.csv'))
oil = wb[(wb.indicator == 'oil_rents_pct_gdp') & wb.year.between(2010, 2021)].groupby('iso3').value.mean()
df['oil_rents_mean'] = df.iso3.map(oil)
df['oil_dependent'] = (df.oil_rents_mean > 10).astype(float).where(df.oil_rents_mean.notna())
df['fragile'] = (df.political_stability <= -1.5).astype(float).where(df.political_stability.notna())

base = 'osi ~ tii + hci + C(edition)'
specs = {
    'M1 infrastructure + human capital': base,
    'M2 + income + government effectiveness': base + ' + log_gdp_pc + gov_effectiveness',
    'M3 + stability + voice + oil dependence': base + ' + log_gdp_pc + gov_effectiveness + political_stability + voice_accountability + oil_dependent',
    'M4 = M3 + fragile x oil': base + ' + log_gdp_pc + gov_effectiveness + political_stability + voice_accountability + oil_dependent + fragile + fragile:oil_dependent',
}
needed = ['osi', 'tii', 'hci', 'log_gdp_pc', 'gov_effectiveness', 'political_stability', 'voice_accountability', 'oil_dependent', 'fragile']
d = df.dropna(subset=needed).copy()

lines = [f'Sample: {len(d)} country-editions, {d.iso3.nunique()} countries, editions {sorted(d.edition.unique())}',
         'OLS with edition fixed effects; standard errors clustered by country.', '']
fits = {}
for name, f in specs.items():
    m = smf.ols(f, data=d).fit(cov_type='cluster', cov_kwds={'groups': d.iso3})
    fits[name] = m
    lines.append(f'== {name}   N={int(m.nobs)}  R2={m.rsquared:.3f}')
    for k in m.params.index:
        if not k.startswith('C(edition'):
            lines.append(f'   {k:32} {m.params[k]:+.4f}  (se {m.bse[k]:.4f}, p={m.pvalues[k]:.3f})')
    lines.append('')

# Same-method subsample (2024 and 2026 use the revised TII)
d2 = d[d.edition >= 2024]
m_s = smf.ols(specs['M3 + stability + voice + oil dependence'], data=d2).fit(cov_type='cluster', cov_kwds={'groups': d2.iso3})
lines.append(f'== Robustness: M3 on 2024-2026 only   N={int(m_s.nobs)}  R2={m_s.rsquared:.3f}')
for k in m_s.params.index:
    if not k.startswith('C(edition'):
        lines.append(f'   {k:32} {m_s.params[k]:+.4f}  (se {m_s.bse[k]:.4f}, p={m_s.pvalues[k]:.3f})')
lines.append('')

# Robustness of the fragile x oil interaction (is it driven by a few countries?)
f4 = specs['M4 = M3 + fragile x oil']
lines.append('== Robustness of fragile x oil-dependent interaction (M4)')
both = sorted(d[(d.fragile == 1) & (d.oil_dependent == 1)].country.unique())
lines.append('   Fragile and oil-dependent in at least one edition: ' + ', '.join(both))
variants = [('all countries', d), ('without Libya', d[d.iso3 != 'LBY']),
            ('without Libya, Iraq and Yemen', d[~d.iso3.isin(['LBY', 'IRQ', 'YEM'])]),
            ('fragile = stability <= -1.0', d.assign(fragile=(d.political_stability <= -1.0).astype(float)))]
for lab, dv in variants:
    mv = smf.ols(f4, data=dv).fit(cov_type='cluster', cov_kwds={'groups': dv.iso3})
    k = 'fragile:oil_dependent'
    lines.append(f'   {lab:32} N={int(mv.nobs)}  coef {mv.params[k]:+.3f} (se {mv.bse[k]:.3f}, p={mv.pvalues[k]:.3f})')
lines.append('')

# Residuals: how far each country's OSI is from what the model predicts, and its rank within the edition
for name in ('M1 infrastructure + human capital', 'M3 + stability + voice + oil dependence'):
    tag = name.split()[0]
    d['resid_' + tag] = fits[name].resid
    d['rank_' + tag] = d.groupby('edition')['resid_' + tag].rank(method='min')  # 1 = largest shortfall
d['n_edition'] = d.groupby('edition').iso3.transform('count')

six = d[d.iso3.isin(SIX)][['country', 'iso3', 'edition', 'osi', 'tii', 'hci', 'resid_M1', 'rank_M1', 'resid_M3', 'rank_M3', 'n_edition']]
six.sort_values(['iso3', 'edition']).to_csv(os.path.join('results', 'residuals_six_countries.csv'), index=False)
lines.append('== Libya: residual from M1 (infrastructure + human capital) and M3 (adds income, governance, stability, voice, oil)')
for _, r in six[six.iso3 == 'LBY'].sort_values('edition').iterrows():
    lines.append(f"   {int(r.edition)}  OSI {r.osi:.3f}  resid M1 {r.resid_M1:+.3f} (rank {int(r.rank_M1)}/{int(r.n_edition)})  resid M3 {r.resid_M3:+.3f} (rank {int(r.rank_M3)}/{int(r.n_edition)})")
lines.append('')
lines.append('== Mean residual 2016-2026 by country (M1 vs M3)')
for iso, nm in SIX.items():
    s = six[(six.iso3 == iso) & (six.edition >= 2016)]
    lines.append(f'   {nm:18} M1 {s.resid_M1.mean():+.3f}   M3 {s.resid_M3.mean():+.3f}')
lines.append('')

big = []
for e in (2024, 2026):
    t = d[d.edition == e].nsmallest(10, 'resid_M3')[['edition', 'country', 'iso3', 'osi', 'tii', 'resid_M3', 'oil_dependent', 'fragile']]
    big.append(t)
    lines.append(f'== Largest shortfalls after M3 controls, {e}')
    for _, r in t.iterrows():
        lines.append(f"   {r.country[:24]:24} OSI {r.osi:.3f} TII {r.tii:.3f} resid {r.resid_M3:+.3f} oil {int(r.oil_dependent)} fragile {int(r.fragile)}")
    lines.append('')
pd.concat(big).to_csv(os.path.join('results', 'largest_shortfalls.csv'), index=False)

open(os.path.join('results', 'models.txt'), 'w', encoding='utf8').write('\n'.join(lines))
print('\n'.join(lines))

# Figure: residuals over time for the six countries (M3)
plt.rcParams.update({'font.family': 'Arial', 'font.size': 10})
fig, ax = plt.subplots(figsize=(7.5, 4.3))
styles = {'LBY': ('-D', 'black'), 'TUN': ('--v', '#555555'), 'EGY': (':s', '#555555'), 'ZAF': ('-.o', '#888888'),
          'SAU': ('--^', '#888888'), 'KOR': (':o', '#aaaaaa')}
for iso, nm in SIX.items():
    s = six[six.iso3 == iso].set_index('edition').reindex(sorted(d.edition.unique())).reset_index()  # gaps break the line
    st, col = styles[iso]
    ax.plot(s.edition, s.resid_M3, st, color=col, label=nm, mfc='white' if iso != 'LBY' else 'black', lw=2 if iso == 'LBY' else 1.2)
ax.axhline(0, color='black', lw=0.7)
ax.axvspan(2023, 2025, color='#eeeeee', zorder=0)
ax.text(2023.1, ax.get_ylim()[1] * 0.92, 'TII revised', fontsize=7.5, color='#444444')
ax.set_xticks(sorted(d.edition.unique()))
ax.set_ylabel('OSI above (+) or below (−) prediction')
ax.legend(frameon=False, fontsize=8, ncol=2, loc='lower left')
for sname in ('top', 'right'):
    ax.spines[sname].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join('results', 'fig_residuals.png'), dpi=300)
print('figure saved')
