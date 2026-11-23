"""Inter-coder reliability: second coder (blind sheet) vs coder A (standardised scores).

Run from the study folder after the second coder has filled audit/Second_Coder_Sheet_BLIND.xlsx:
    python -I code/09_reliability.py
Writes results/reliability.txt and results/reliability_pairs.csv.
"""
import sys
from collections import Counter

import openpyxl
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
CRIT = ['C1', 'C2', 'C3', 'C4', 'C5', 'C9', 'C12']


def norm(v):
    if v is None or pd.isna(v) or str(v).strip() == '':
        return None
    s = str(v).strip().upper()
    if s in ('NA', 'N/A'):
        return 'NA'
    try:
        return str(int(float(s)))
    except ValueError:
        return s


def kappa(a, b, weighted=False):
    cats = sorted(set(a) | set(b))
    n = len(a)
    if n == 0:
        return float('nan')
    if weighted:  # quadratic weights for ordinal C1 (0-3)
        x = [int(v) for v in a]; y = [int(v) for v in b]
        k = max(x + y) - min(x + y) or 1
        w = lambda i, j: ((i - j) / k) ** 2
        obs = sum(w(i, j) for i, j in zip(x, y)) / n
        ca, cb = Counter(x), Counter(y)
        exp = sum(ca[i] * cb[j] * w(i, j) for i in ca for j in cb) / n ** 2
        return 1 - obs / exp if exp else 1.0
    po = sum(i == j for i, j in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[c] * cb[c] for c in cats) / n ** 2
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


SHEET = sys.argv[1] if len(sys.argv) > 1 else 'audit/Second_Coder_Sheet_BLIND.xlsx'
TAG = sys.argv[2] if len(sys.argv) > 2 else ''  # suffix for output files, e.g. _AI_coderB
wb = openpyxl.load_workbook(SHEET, read_only=True)
rows = list(wb['Second_coder'].iter_rows(values_only=True))
b = pd.DataFrame(rows[1:], columns=rows[0])
a = pd.concat([pd.read_csv(f'audit/coding_std/{c}.csv', dtype=str) for c in b['ISO3'].unique()])
m = b.merge(a, on=['ISO3', 'Service code'], suffixes=('_B', '_A'))
if b['C1'].map(norm).isna().all():
    sys.exit('The second-coder sheet is still empty: fill C1 (and the other columns) first.')

out, pairs = [], []
for c in CRIT:
    pa, pb = [], []
    for _, r in m.iterrows():
        x, y = norm(r[c + '_A']), norm(r[c + '_B'])
        pairs.append({'ISO3': r['ISO3'], 'Service code': r['Service code'], 'Criterion': c, 'Coder A': x, 'Coder B': y,
                      'Agree': (x == y) if x is not None and y is not None else None})
        if x is not None and y is not None:
            pa.append(x); pb.append(y)
    n = len(pa)
    agree = sum(i == j for i, j in zip(pa, pb)) / n if n else float('nan')
    line = f'{c}: n = {n}, agreement = {agree:.0%}, Cohen\'s kappa = {kappa(pa, pb):.2f}'
    if c == 'C1' and n and all(v.isdigit() for v in pa + pb):
        line += f', quadratic weighted kappa = {kappa(pa, pb, weighted=True):.2f}'
    out.append(line)

p = pd.DataFrame(pairs)
done = p.dropna(subset=['Agree'])
out.append(f'All seven criteria pooled: n = {len(done)}, agreement = {done.Agree.mean():.0%}, '
           f"Cohen's kappa = {kappa(list(done['Coder A']), list(done['Coder B'])):.2f}")
out.append('\nDisagreements (resolve by discussion and record the outcome in the workbook Reliability sheet):')
for _, r in done[~done.Agree.astype(bool)].iterrows():
    out.append(f"  {r['ISO3']} {r['Service code']} {r['Criterion']}: A = {r['Coder A']}, B = {r['Coder B']}")
txt = '\n'.join(out)
open(f'results/reliability{TAG}.txt', 'w', encoding='utf8').write(f'Second coder sheet: {SHEET}\n' + txt)
p.to_csv(f'results/reliability_pairs{TAG}.csv', index=False, encoding='utf-8-sig')
print(txt)
