"""Download World Bank indicators (public API, no key) for all countries, 2002-2025.

Output: data/raw/worldbank_indicators.csv (long format: iso3, indicator, year, value)
Run from the study folder:  python -I code/01_fetch_worldbank.py
"""
import csv
import json
import os
import time
import urllib.request

INDICATORS = {
    'GOV_WGI_GE.EST': 'gov_effectiveness',     # Worldwide Governance Indicators (source 3), estimate approx. -2.5 to 2.5
    'GOV_WGI_PV.EST': 'political_stability',   # Political Stability
    'GOV_WGI_VA.EST': 'voice_accountability',  # Voice and Accountability
    'NY.GDP.PCAP.KD': 'gdp_pc_const_usd',  # GDP per capita, constant US$
    'NY.GDP.PETR.RT.ZS': 'oil_rents_pct_gdp',
    'SP.POP.TOTL': 'population',
}
OUT = os.path.join('data', 'raw', 'worldbank_indicators.csv')


def fetch(ind):
    src = '&source=3' if ind.startswith('GOV_WGI_') else ''
    url = f'https://api.worldbank.org/v2/country/all/indicator/{ind}?format=json&date=2002:2025&per_page=20000{src}'
    req = urllib.request.Request(url, headers={'User-Agent': 'research-data-fetch/1.0'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                payload = json.load(r)
            if len(payload) < 2:
                raise ValueError(str(payload)[:200])
            meta, rows = payload
            return meta, rows or []
        except Exception as e:  # network hiccup: retry
            print('retry', ind, e)
            time.sleep(3 * (attempt + 1))
    raise RuntimeError('failed ' + ind)


def main():
    out = []
    for ind, name in INDICATORS.items():
        meta, rows = fetch(ind)
        n = 0
        for r in rows:
            iso3 = r.get('countryiso3code') or ''
            if len(iso3) == 3 and r.get('value') is not None:
                out.append((iso3, name, int(r['date']), r['value']))
                n += 1
        print(f'{ind:20} {name:22} rows={n} lastupdated={meta.get("lastupdated")}')
        time.sleep(1)
    with open(OUT, 'w', newline='', encoding='utf8') as f:
        w = csv.writer(f)
        w.writerow(['iso3', 'indicator', 'year', 'value'])
        w.writerows(out)
    print('wrote', OUT, len(out))


if __name__ == '__main__':
    main()
