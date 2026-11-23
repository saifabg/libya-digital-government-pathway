"""Test the framework's propositions with the World Bank GovTech Maturity Index (GTMI) and UN data.

Run from the study folder:  python -I code/08_gtmi_tests.py
Inputs : data/raw/WBG_GovTech_Dataset_Dec2025.xlsx (GTMI 2020, 2022, 2025), UN EKAP data, World Bank indicators
Outputs: data/gtmi_stage_indices.csv, results/gtmi_tests.txt, results/gtmi_libya_profile.csv

Design: framework-stage indices are built from GTMI institutional indicators (not from the UN indices that GTMI
also includes, to avoid circularity). Outcome = UN Online Services Index (OSI) in the NEXT UN edition
(GTMI 2020 -> UN 2022, GTMI 2022 -> UN 2024, GTMI 2025 -> UN 2026), so foundations are measured before services.
"""
import json
import math
import os

import numpy as np
import openpyxl
import pandas as pd
import statsmodels.formula.api as smf

STAGES = {
    'stage0_governance': ['I-33', 'I-35', 'I-36'],                       # lead entity, strategy, whole-of-government
    'stage1_foundations': ['I-4', 'I-22', 'I-38', 'I-42'],  # core, available in 2020-2025: service bus, e-payment, data protection, e-signature/PKI
    'stage4_measurement': ['I-31', 'I-32'],                              # citizen feedback platforms, published performance statistics
}
NEXT_UN = {2020: 2022, 2022: 2024, 2025: 2026}

wb = openpyxl.load_workbook(os.path.join('data', 'raw', 'WBG_GovTech_Dataset_Dec2025.xlsx'), read_only=True)
rows = list(wb['GTMI_Data'].iter_rows(values_only=True))
hdr = [str(h).strip() if h is not None else '' for h in rows[0]]
g = pd.DataFrame(rows[1:], columns=hdr)
g = g[g['Year'].notna()].copy()
g['Year'] = g['Year'].astype(int)
g['iso3'] = g['Code'].astype(str).str.strip()
num = lambda s: pd.to_numeric(s, errors='coerce')

# scale each indicator to 0-1 by its maximum observed value (response scales differ: 0/1, 0-2, 0-3)
cols = sorted({c for v in STAGES.values() for c in v})
for c in cols:
    x = num(g[c])
    g[c + '_s'] = x / x.max()
for st, cs in STAGES.items():
    g[st] = g[[c + '_s' for c in cs]].mean(axis=1, skipna=False)
g['fcs'] = g['FCS'].astype(str).str.strip().str.startswith('FCS')
# full foundations index (adds digital ID I-26, new in 2025, and interoperability framework I-3, from 2022)
for extra in ('I-26', 'I-3'):
    x = num(g[extra]); g[extra + '_s'] = x / x.max()
g['stage1_full'] = g[[c + '_s' for c in STAGES['stage1_foundations']] + ['I-26_s', 'I-3_s']].mean(axis=1, skipna=False)
g['gtmi'] = num(g['GTMI'])

# UN data
un = json.load(open(os.path.join('data', 'raw', 'ekap_egdi_all_countries_2003_2026.json'), encoding='utf8'))
u = []
for y in (2020, 2022, 2024, 2026):
    for r in un[str(y)]:
        tii = 3 * r['egdi'] - r['osi'] - r['hci'] if y == 2024 else r['tii']
        u.append(dict(iso3=r['code'], un_year=y, osi=r['osi'], tii=tii, hci=r['hci']))
u = pd.DataFrame(u)
wbi = pd.read_csv(os.path.join('data', 'raw', 'worldbank_indicators.csv'))
gdp = wbi[wbi.indicator == 'gdp_pc_const_usd'].pivot_table(index='iso3', columns='year', values='value')


def log_gdp(iso, year):
    for lag in (0, 1, 2, 3):
        try:
            v = gdp.loc[iso, year - lag]
            if pd.notna(v) and v > 0:
                return math.log(v)
        except KeyError:
            return np.nan
    return np.nan


g['un_year'] = g['Year'].map(NEXT_UN)
d = g.merge(u, on=['iso3', 'un_year'], how='left')
# baseline OSI in the UN edition at (or just before) the GTMI year, for change models
base = u.rename(columns={'un_year': 'base_year', 'osi': 'osi_base', 'tii': 'tii_base', 'hci': 'hci_base'})
d['base_year'] = d['Year'].map({2020: 2020, 2022: 2022, 2025: 2024})
d = d.merge(base, on=['iso3', 'base_year'], how='left')
d['log_gdp_pc'] = [log_gdp(i, y) for i, y in zip(d.iso3, d.Year)]
d['osi_change'] = d['osi'] - d['osi_base']
keep = ['Year', 'iso3', 'Economy', 'fcs', 'gtmi', 'stage1_full', 'I-26_s', 'I-3_s'] + list(STAGES) + [c + '_s' for c in cols] + ['un_year', 'osi', 'tii', 'hci', 'osi_base', 'osi_change', 'log_gdp_pc']
d[keep].to_csv(os.path.join('data', 'gtmi_stage_indices.csv'), index=False)

out = []
P = lambda m, k: f'{m.params[k]:+.3f} (se {m.bse[k]:.3f}, p={m.pvalues[k]:.3f})'
ctrl = 'tii + hci + log_gdp_pc + C(Year)'
s = d.dropna(subset=['osi', 'tii', 'hci', 'log_gdp_pc', 'stage0_governance', 'stage1_foundations', 'stage4_measurement'])
out.append(f'Sample: {len(s)} country-editions, {s.iso3.nunique()} economies; GTMI editions {sorted(s.Year.unique())} -> next UN edition. '
           f'OLS, edition fixed effects, SE clustered by economy.')
out.append(f'Stage index means: ' + ', '.join(f'{k} {s[k].mean():.2f}' for k in STAGES))
fit = lambda f, data: smf.ols(f, data=data).fit(cov_type='cluster', cov_kwds={'groups': data.iso3})

m0 = fit(f'osi ~ {ctrl}', s)
m1 = fit(f'osi ~ stage0_governance + {ctrl}', s)
m2 = fit(f'osi ~ stage1_foundations + {ctrl}', s)
m3 = fit(f'osi ~ stage0_governance + stage1_foundations + stage4_measurement + {ctrl}', s)
m4 = fit(f'osi ~ stage0_governance * stage1_foundations + stage4_measurement + {ctrl}', s)
out.append('')
out.append(f'Baseline (TII, HCI, income, edition): R2 = {m0.rsquared:.3f}')
out.append(f'P1 governance (Stage 0) -> later OSI: {P(m1, "stage0_governance")}, R2 = {m1.rsquared:.3f}')
out.append(f'P2 foundations (Stage 1) -> later OSI: {P(m2, "stage1_foundations")}, R2 = {m2.rsquared:.3f}')
out.append(f'P1-P2 joint: governance {P(m3, "stage0_governance")}; foundations {P(m3, "stage1_foundations")}; '
           f'measurement {P(m3, "stage4_measurement")}; R2 = {m3.rsquared:.3f}')
out.append(f'P3 complementarity (governance x foundations): {P(m4, "stage0_governance:stage1_foundations")}')

# P4 sequencing: foundations measured in GTMI 2022 -> change in OSI from UN 2022 to UN 2026 (four years later)
lag = g[g.Year == 2022][['iso3', 'stage0_governance', 'stage1_foundations', 'I-3_s', 'fcs']].copy()
lag = lag.merge(u[u.un_year == 2022][['iso3', 'osi', 'tii', 'hci']].rename(columns={'osi': 'osi22', 'tii': 'tii22', 'hci': 'hci22'}), on='iso3')
lag = lag.merge(u[u.un_year == 2026][['iso3', 'osi']].rename(columns={'osi': 'osi26'}), on='iso3')
lag['log_gdp_pc'] = [log_gdp(i, 2021) for i in lag.iso3]
lag = lag.dropna(subset=['osi22', 'osi26', 'tii22', 'hci22', 'log_gdp_pc', 'stage0_governance', 'stage1_foundations'])
lag['d_osi'] = lag.osi26 - lag.osi22
fitl = lambda f: smf.ols(f, data=lag).fit(cov_type='HC1')
m5 = fitl('osi26 ~ osi22 + stage0_governance + stage1_foundations + tii22 + hci22 + log_gdp_pc')
out.append(f'P4 sequencing (GTMI 2022 -> UN 2026 OSI, controlling UN 2022 OSI; N = {int(m5.nobs)}, robust SE): '
           f'governance {P(m5, "stage0_governance")}; foundations {P(m5, "stage1_foundations")}')
lag['low_start'] = lag.osi22 < lag.osi22.median()
m5b = smf.ols('osi26 ~ osi22 + stage0_governance + stage1_foundations + tii22 + hci22 + log_gdp_pc', data=lag[lag.low_start]).fit(cov_type='HC1')
out.append(f'   Countries starting below the median OSI in 2022 (N = {int(m5b.nobs)}): foundations {P(m5b, "stage1_foundations")}; governance {P(m5b, "stage0_governance")}')

# P5 fragile and conflict-affected states
fc = s[s.fcs]
out.append(f'FCS country-editions in the pooled sample: {len(fc)} ({fc.iso3.nunique()} economies)')
m6 = fit(f'osi ~ stage1_foundations * fcs + stage0_governance + {ctrl}', s)
out.append(f'P5 foundations x FCS: foundations {P(m6, "stage1_foundations")}; FCS {P(m6, "fcs[T.True]")}; interaction {P(m6, "stage1_foundations:fcs[T.True]")}')
m6b = fit(f'osi ~ stage1_foundations + stage0_governance + {ctrl}', fc)
out.append(f'   Within FCS only (N = {int(m6b.nobs)}): foundations {P(m6b, "stage1_foundations")}; governance {P(m6b, "stage0_governance")}')

# Full foundations index (six components incl. digital ID), GTMI 2025 only
f25 = s[(s.Year == 2025)].dropna(subset=['stage1_full'])
m7 = smf.ols('osi ~ stage0_governance + stage1_full + stage4_measurement + tii + hci + log_gdp_pc', data=f25).fit(cov_type='HC1')
out.append(f'Full six-component foundations, GTMI 2025 -> UN 2026 (N = {int(m7.nobs)}): foundations {P(m7, "stage1_full")}; '
           f'governance {P(m7, "stage0_governance")}; measurement {P(m7, "stage4_measurement")}; R2 = {m7.rsquared:.3f}')
out.append('Foundation components one at a time (pooled, controls as above):')
for cmp in STAGES['stage1_foundations']:
    mm = fit(f'osi ~ Q("{cmp}_s") + {ctrl}', s.dropna(subset=[cmp + '_s']))
    out.append(f'   {cmp}: {P(mm, f"Q(\"{cmp}_s\")")}')
mm = smf.ols('osi ~ Q("I-26_s") + tii + hci + log_gdp_pc', data=f25.dropna(subset=['I-26_s'])).fit(cov_type='HC1')
out.append(f'   I-26 digital ID (2025 only): {P(mm, "Q(\"I-26_s\")")}')

# Libya profile
lby = d[d.iso3 == 'LBY'][['Year'] + list(STAGES) + ['stage1_full'] + [c + '_s' for c in cols] + ['I-26_s', 'I-3_s', 'un_year', 'osi']]
lby.to_csv(os.path.join('results', 'gtmi_libya_profile.csv'), index=False)
peers = d[(d.Year == 2025) & d.iso3.isin(['LBY', 'TUN', 'EGY', 'ZAF', 'SAU', 'KOR'])][['iso3'] + list(STAGES) + ['stage1_full', 'osi']]
out.append('')
out.append('GTMI 2025 stage indices, six countries (OSI = UN 2026):')
out.append(peers.round(2).to_string(index=False))
out.append('')
out.append('Libya, all GTMI editions:')
out.append(lby.round(2).to_string(index=False))
# what Libya would be predicted to reach with the six-country median foundations and governance (2025, M3)
s25 = d[(d.Year == 2025) & (d.iso3 == 'LBY')].copy()
if len(s25):
    med = peers[peers.iso3 != 'LBY'][['stage0_governance', 'stage1_foundations', 'stage4_measurement']].median()
    base_pred = m3.predict(s25)[s25.index[0]]
    s26 = s25.copy()
    for k in med.index:
        s26[k] = med[k]
    alt = m3.predict(s26)[s26.index[0]]
    out.append(f'Libya predicted OSI 2026 with its own 2025 stage indices: {base_pred:.3f} (actual {s25.osi.iloc[0]:.3f}); '
               f'with the comparison countries\' median stage indices: {alt:.3f}')
open(os.path.join('results', 'gtmi_tests.txt'), 'w', encoding='utf8').write('\n'.join(out))
print('\n'.join(out))
