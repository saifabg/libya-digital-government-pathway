"""Apply cross-country decision rules to the coder-A files and log every change.

Run from the study folder:  python -I code/06_standardise.py
Input : audit/coding/<ISO3>.csv and <ISO3>_portal.csv (raw coder-A files, never modified)
Output: audit/coding_std/<ISO3>.csv and <ISO3>_portal.csv, results/standardisation_log.csv

Decision rules (also recorded in the protocol, section 4):
R1 C2 = 2 only for a state-issued digital-identity credential (national eID or mobile ID app, state-recognised
   certificate, national single sign-on such as Nafath/Absher). A portal account using the national ID number plus
   an SMS code is C2 = 1.
R2 C12 = 1 only for an official, optional channel in which an intermediary completes the digital application for
   the applicant (bank branch, post office, service house, licensed agent). Self-service kiosks, cash-payment
   counters and mandatory or private professionals (tax agents, architects, engineering offices) are C12 = 0.
R3 C9 is NA when C1 <= 1 (no online service for an alternative channel to complement).
R4 Values that the coder states were inferred rather than observed are blanked.
R5 C11 is NA for transactions completed immediately (bill payment; immediately issued certificates and returns).
R6 P1 = 1 where a national portal lists services, even if information-only (Libya, ejraat.gov.ly); noted.
"""
import csv
import os
import re

ORDER = ['LBY', 'TUN', 'EGY', 'ZAF', 'SAU', 'KOR']
IN, OUT = os.path.join('audit', 'coding'), os.path.join('audit', 'coding_std')
os.makedirs(OUT, exist_ok=True)
log = []


def setv(iso, r, col, new, rule, why):
    old = r.get(col, '')
    if old != new:
        log.append(dict(ISO3=iso, item=r.get('Service code', 'portal'), criterion=col, old=old, new=new, rule=rule, reason=why))
        r[col] = new


for iso in ORDER:
    with open(os.path.join(IN, f'{iso}.csv'), encoding='utf-8-sig') as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)
    for r in rows:
        sc, notes = r['Service code'], r.get('Notes', '')
        # R1: Egypt portal login is national ID number + registered mobile
        if iso == 'EGY' and r.get('C2') == '2' and re.search(r'national ID number \+ mobile|ID number plus|national ID and mobile', notes, re.I):
            setv(iso, r, 'C2', '1', 'R1', 'login is national ID number plus registered mobile (portal account), not a state digital-identity credential')
        if iso == 'EGY' and r.get('C2') == '2' and 'Digital Egypt' in notes and 'Digital Identity app' in notes:
            setv(iso, r, 'C2', '1', 'R1', 'Digital Egypt login (national ID number plus mobile); Digital Identity app promoted but not stated as the login for this service')
        # R2
        if r.get('C12') == '1' and re.search(r'kiosk|bank counters|convenience store|tax agents|architect|engineering office', notes, re.I) \
                and not re.search(r'post offices renew|banks register companies|bank branch', notes, re.I):
            setv(iso, r, 'C12', '0', 'R2', 'kiosk / cash counter / mandatory or private professional is not an optional assisted digital channel')
        # R3
        if r.get('C1') in ('0', '1') and r.get('C9') not in ('', 'NA'):
            setv(iso, r, 'C9', 'NA', 'R3', 'C1 <= 1: no online service for an alternative channel to complement')
        # R4
        if iso == 'SAU' and sc in ('S02', 'S04', 'S09') and r.get('C3') == '1':
            setv(iso, r, 'C3', '', 'R4', 'online payment inferred from absence of a visit; payment method not stated on the service card')
        if re.search(r'C2=2 inferred', notes) and r.get('C2') == '2':
            setv(iso, r, 'C2', '', 'R4', 'login method inferred, not observed')
        # R5
        if r.get('C1') == '3' and r.get('C11') == '' and (sc == 'S08' or re.search(r'immediate', notes, re.I)):
            setv(iso, r, 'C11', 'NA', 'R5', 'transaction completed immediately; status tracking not applicable')
    with open(os.path.join(OUT, f'{iso}.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

    with open(os.path.join(IN, f'{iso}_portal.csv'), encoding='utf-8-sig') as f:
        rd = csv.DictReader(f); pf = rd.fieldnames; prow = list(rd)
    for p in prow:
        if iso == 'LBY' and p.get('P1') == '0':
            setv(iso, p, 'P1', '1', 'R6', 'ejraat.gov.ly is the national portal listing procedures (information only); aligns with C5 coding')
            p['Notes'] = (p.get('Notes', '') + ' [R6: P1 set to 1 = national information-only portal.]').strip()
    with open(os.path.join(OUT, f'{iso}_portal.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=pf); w.writeheader(); w.writerows(prow)

with open(os.path.join('results', 'standardisation_log.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['ISO3', 'item', 'criterion', 'old', 'new', 'rule', 'reason'])
    w.writeheader(); w.writerows(log)
print(len(log), 'changes')
from collections import Counter
print(Counter((x['rule'], x['ISO3']) for x in log))
for x in log:
    if x['rule'] in ('R1', 'R2', 'R4', 'R6'):
        print(' ', x['rule'], x['ISO3'], x['item'], x['criterion'], x['old'], '->', x['new'])
