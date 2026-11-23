"""Build a country-edition panel: UN E-Government Survey (2008-2026 editions) + World Bank covariates.

Covariates are taken from the year before each survey edition (survey data are collected in the
preceding year); if missing, the nearest earlier year within three years is used.
2024 TII is recomputed as 3*EGDI - OSI - HCI because the data-center file's 2024 TII field is
inconsistent for some countries (the recomputed values equal the published ones).

Run from the study folder:  python -I code/02_build_panel.py
Output: data/panel_un_wb.csv
"""
import json
import math
import os

import pandas as pd

EDITIONS = [2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024, 2026]
ARAB = {'DZA', 'BHR', 'COM', 'DJI', 'EGY', 'IRQ', 'JOR', 'KWT', 'LBN', 'LBY', 'MRT', 'MAR', 'OMN', 'PSE',
        'QAT', 'SAU', 'SOM', 'SDN', 'SYR', 'TUN', 'ARE', 'YEM'}

un = json.load(open(os.path.join('data', 'raw', 'ekap_egdi_all_countries_2003_2026.json'), encoding='utf8'))
rows = []
for y in EDITIONS:
    for r in un[str(y)]:
        if r['egdi'] <= 0:          # country not assessed in that edition
            continue
        tii = 3 * r['egdi'] - r['osi'] - r['hci'] if y == 2024 else r['tii']
        rows.append(dict(iso3=r['code'], country=r['name'], region=r.get('region'), income=r.get('income'),
                         ldc=r.get('isLdc'), arab=r['code'] in ARAB, edition=y, egdi=r['egdi'], osi=r['osi'],
                         tii=round(tii, 4), hci=r['hci'], epi=r.get('epi')))
panel = pd.DataFrame(rows)

wb = pd.read_csv(os.path.join('data', 'raw', 'worldbank_indicators.csv'))
wide = wb.pivot_table(index=['iso3', 'year'], columns='indicator', values='value').reset_index()


def lagged(iso3, edition, col):
    sub = wide[(wide.iso3 == iso3) & wide[col].notna()]
    for lag in (1, 2, 3, 4):
        v = sub.loc[sub.year == edition - lag, col]
        if len(v):
            return float(v.iloc[0]), edition - lag
    return math.nan, None


covs = ['gov_effectiveness', 'political_stability', 'voice_accountability', 'gdp_pc_const_usd',
        'oil_rents_pct_gdp', 'population']
for c in covs:
    vals = [lagged(i, e, c) for i, e in zip(panel.iso3, panel.edition)]
    panel[c] = [v for v, _ in vals]
    panel[c + '_year'] = [yy for _, yy in vals]
panel['log_gdp_pc'] = panel.gdp_pc_const_usd.apply(lambda v: math.log(v) if v and v > 0 else math.nan)
panel['log_pop'] = panel.population.apply(lambda v: math.log(v) if v and v > 0 else math.nan)
panel['gap_tii_osi'] = panel.tii - panel.osi
panel.to_csv(os.path.join('data', 'panel_un_wb.csv'), index=False)

print('rows', len(panel), 'countries', panel.iso3.nunique())
print(panel.groupby('edition')[covs].apply(lambda d: d.notna().mean().round(2)).to_string())
cols = ['edition', 'osi', 'tii', 'hci', 'gov_effectiveness', 'political_stability', 'voice_accountability',
        'gdp_pc_const_usd', 'gdp_pc_const_usd_year', 'oil_rents_pct_gdp', 'oil_rents_pct_gdp_year']
print(panel[panel.iso3 == 'LBY'][cols].to_string(index=False))
