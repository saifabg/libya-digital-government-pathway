"""Validate the coder-A audit files, merge them into the workbook, and compute audit indices.

Run from the study folder:  python -I code/05_merge_audit.py
Inputs : audit/coding_std/<ISO3>.csv and _portal.csv (output of 06_standardise.py), audit/evidence/<ISO3>/*.txt
Outputs: audit/Portal_Audit_Workbook.xlsx (Scoring and Portal_level filled), results/audit_scores.csv,
         results/audit_indices.csv, results/audit_validation.txt, results/fig_audit_heatmap.png
"""
import csv
import os
import subprocess
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook

ORDER = ['LBY', 'TUN', 'EGY', 'ZAF', 'SAU', 'KOR']
NAMES = {'LBY': 'Libya', 'TUN': 'Tunisia', 'EGY': 'Egypt', 'ZAF': 'South Africa', 'SAU': 'Saudi Arabia', 'KOR': 'Korea'}
ALLOWED = {'C1': {'0', '1', '2', '3'}, 'C2': {'0', '1', '2', 'NA'}, 'C3': {'0', '1', 'NA'}, 'C4': {'0', '1', '2', 'NA'},
           'C5': {'0', '1', '2'}, 'C6': {'0', '1'}, 'C7': {'0', '1'}, 'C8': {'0', '1'}, 'C9': {'0', '1', 'NA'},
           'C10': {'0', '1'}, 'C11': {'0', '1', 'NA'}, 'C12': {'0', '1'}}
ACCESS = {'OK', 'Certificate error', 'Blocked (bot check / geo)', 'Not found (404)', 'Login required'}

problems, rows, portals = [], [], []
for iso in ORDER:
    p = os.path.join('audit', 'coding_std', f'{iso}.csv')
    if not os.path.exists(p):
        problems.append(f'{iso}: coding file missing'); continue
    with open(p, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            r = {k.strip(): (v or '').strip() for k, v in r.items() if k}
            rows.append(r)
            sc = r.get('Service code', '?')
            for c, allowed in ALLOWED.items():
                v = r.get(c, '')
                if v and v not in allowed:
                    problems.append(f'{iso} {sc}: {c}={v!r} not allowed')
            if r.get('C1') in {'0', '1'}:
                for c in ('C2', 'C3', 'C11'):
                    if r.get(c) not in ('', 'NA'):
                        problems.append(f'{iso} {sc}: {c}={r.get(c)} but C1<2 (should be NA)')
            if r.get('Access status') and r['Access status'] not in ACCESS:
                problems.append(f"{iso} {sc}: access status {r['Access status']!r} not in list")
            if not os.path.exists(os.path.join('audit', 'evidence', iso, f'{sc}.txt')):
                problems.append(f'{iso} {sc}: evidence file missing')
            if not r.get('C1'):
                problems.append(f'{iso} {sc}: C1 blank')
    pp = os.path.join('audit', 'coding_std', f'{iso}_portal.csv')
    if os.path.exists(pp):
        with open(pp, encoding='utf-8-sig') as f:
            portals.extend({k.strip(): (v or '').strip() for k, v in r.items() if k} for r in csv.DictReader(f))
    else:
        problems.append(f'{iso}: portal file missing')

df = pd.DataFrame(rows)
counts = df.groupby('ISO3').size().to_dict() if len(df) else {}
for iso in ORDER:
    if counts.get(iso, 0) != 12:
        problems.append(f'{iso}: {counts.get(iso, 0)} rows (expected 12)')
open(os.path.join('results', 'audit_validation.txt'), 'w', encoding='utf8').write(
    'Validation of coder-A audit files\n' + ('\n'.join(problems) if problems else 'No problems found.') + '\n')
print('validation problems:', len(problems))
for x in problems[:60]:
    print('  ', x)

# Rebuild a clean workbook, then fill Scoring and Portal_level
subprocess.run([sys.executable, '-I', os.path.join('code', '04_make_audit_workbook.py')], check=True)
wb = load_workbook(os.path.join('audit', 'Portal_Audit_Workbook.xlsx'))
ws = wb['Scoring']
hdr = [c.value for c in ws[1]]
key = {(r.get('ISO3'), r.get('Service code')): r for r in rows}
src_for = {'Responsible agency': 'Responsible agency', 'Service page URL': 'Service page URL', 'Access date (YYYY-MM-DD)': 'Access date',
           'Coder': 'Coder', 'Access status': 'Access status', 'Evidence IDs': 'Evidence IDs', 'Notes': 'Notes'}
for row in ws.iter_rows(min_row=2):
    r = key.get((row[0].value, row[2].value))
    if not r:
        continue
    for j, h in enumerate(hdr):
        if h in src_for:
            row[j].value = r.get(src_for[h], '')
        elif h and h.split(' ')[0] in ALLOWED:
            row[j].value = r.get(h.split(' ')[0], '')
wp = wb['Portal_level']
phdr = [c.value for c in wp[1]]
pkey = {p.get('ISO3'): p for p in portals}
for row in wp.iter_rows(min_row=2):
    p = pkey.get(row[0].value)
    if not p:
        continue
    for j, h in enumerate(phdr):
        if h in ('Access date', 'Coder', 'Evidence IDs', 'Notes', 'Portal URL'):
            row[j].value = p.get(h, row[j].value)
        elif h and h.split(' ')[0] in {f'P{i}' for i in range(1, 11)}:
            row[j].value = p.get(h.split(' ')[0], '')
# Second-coder sample (results/second_coder_sample.csv, 15 rows drawn with a fixed seed): pre-fill coder A
samp = os.path.join('results', 'second_coder_sample.csv')
if os.path.exists(samp):
    wr = wb['Reliability']
    with open(samp, encoding='utf-8') as f:
        for s in csv.DictReader(f):
            a = key.get((s['ISO3'], s['Service code']), {})
            for c in ('C1', 'C2', 'C3', 'C4', 'C5', 'C9', 'C12'):
                wr.append([f"{s['ISO3']}-{s['Service code']}", c, a.get(c, ''), '', '', ''])
wb.save(os.path.join('audit', 'Portal_Audit_Workbook.xlsx'))

# Indices
if len(df):
    num = lambda s: pd.to_numeric(s.replace({'NA': np.nan, '': np.nan}), errors='coerce')
    for c in ALLOWED:
        df[c + '_n'] = num(df[c]) if c in df else np.nan
    df.to_csv(os.path.join('results', 'audit_scores.csv'), index=False)
    share = lambda cond: (lambda s: cond(s.dropna()).mean() if s.notna().any() else np.nan)
    mean_over = lambda k: (lambda s: s.dropna().mean() / k if s.notna().any() else np.nan)
    ind = df.groupby('ISO3').agg(
        services_coded=('C1_n', 'count'),
        maturity_index=('C1_n', mean_over(3)),
        fully_online_share=('C1_n', share(lambda s: s == 3)),
        transactional_share=('C1_n', share(lambda s: s >= 2)),
        national_eid_share=('C2_n', share(lambda s: s == 2)),
        online_payment_share=('C3_n', share(lambda s: s == 1)),
        once_only_index=('C4_n', mean_over(2)),
        integrated_share=('C5_n', share(lambda s: s == 2)),
        assisted_digital_share=('C12_n', share(lambda s: s == 1)),
    ).reindex(ORDER)
    ind.insert(0, 'country', [NAMES[i] for i in ind.index])
    ind.round(3).to_csv(os.path.join('results', 'audit_indices.csv'))
    print(ind.round(2).to_string())

    # Heatmap of C1 (country x service)
    mat = df.pivot_table(index='ISO3', columns='Service code', values='C1_n').reindex(ORDER)
    svc = sorted(mat.columns)
    mat = mat[svc]
    fig, ax = plt.subplots(figsize=(9, 3.6))
    im = ax.imshow(mat.values, cmap='Greys', vmin=0, vmax=3, aspect='auto')
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat.values[i, j]
            if np.isnan(v):
                ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=False, hatch='///', edgecolor='#999999', lw=0))
            ax.text(j, i, 'n/o' if np.isnan(v) else int(v), ha='center', va='center', fontsize=9,
                    color='white' if (not np.isnan(v) and v >= 2) else 'black')
    ax.set_xticks(range(len(svc))); ax.set_xticklabels(svc, fontsize=8)
    ax.set_yticks(range(len(ORDER))); ax.set_yticklabels([NAMES[i] for i in ORDER], fontsize=9)
    cb = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3], fraction=0.03)
    cb.ax.set_yticklabels(['0 none', '1 information', '2 partly online', '3 fully online'], fontsize=7.5)
    ax.set_xlabel('S01 birth, S02 ID, S03 passport, S04 civil-status extract, S05 company, S06 licence, S07 tax, S08 electricity,' + chr(10) + 'S09 vehicle, S10 university, S11 social benefit, S12 building permit.  n/o = official site not reachable', fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join('results', 'fig_audit_heatmap.png'), dpi=300)
    print('heatmap saved')
