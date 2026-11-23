"""Create the portal-audit workbook (audit/Portal_Audit_Workbook.xlsx).

Run from the study folder:  python -I code/04_make_audit_workbook.py
"""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

COUNTRIES = [
    ('LBY', 'Libya', 'Case', 'https://ejraat.gov.ly', 'Procedures guide (eRegulations, launched 2021); no central transactional portal found. Also check agency sites (passports, civil registry, tax, commercial registry).'),
    ('TUN', 'Tunisia', 'Neighbour', 'https://khadamet.gov.tn', 'Unified administrative-services portal (first phase reported 2026).'),
    ('EGY', 'Egypt', 'Neighbour', 'https://digital.gov.eg', 'Digital Egypt platform.'),
    ('ZAF', 'South Africa', 'Africa #1 (UN EGDI 2024, 2026)', 'https://www.gov.za', 'National government portal; services often run by departments (e.g. Home Affairs eHomeAffairs, SARS eFiling).'),
    ('SAU', 'Saudi Arabia', 'Arab #1 (UN EGDI 2024, 2026)', 'https://my.gov.sa', 'Unified National Platform (blocks automated access; open in a browser). Agency platforms such as Absher may host services.'),
    ('KOR', 'Republic of Korea', 'World #1 (UN EGDI 2026)', 'https://www.gov.kr', 'Government24.'),
]
SERVICES = [
    ('S01', 'Birth registration / birth certificate', 'Civil status'),
    ('S02', 'National ID card: first issue or renewal', 'Identity'),
    ('S03', 'Passport renewal', 'Identity / travel'),
    ('S04', 'Civil-status extract (e.g. family record, marriage certificate)', 'Civil status'),
    ('S05', 'Company (business) registration', 'Business'),
    ('S06', 'Commercial or business activity licence', 'Business'),
    ('S07', 'Income or corporate tax filing and payment', 'Tax'),
    ('S08', 'Electricity bill payment (public utility)', 'Utilities'),
    ('S09', 'Vehicle registration renewal', 'Transport'),
    ('S10', 'Public university admission / enrolment', 'Education'),
    ('S11', 'Social-assistance or social-security benefit application', 'Social protection'),
    ('S12', 'Building permit', 'Municipal'),
]
# (code, short name, allowed values, definition)
CRITERIA = [
    ('C1', 'Service maturity', ['0', '1', '2', '3'],
     '0 = no official online information; 1 = information only (steps, documents, fees), including downloadable forms; 2 = partly online: at least one step can be done online by the applicant (submit an application, book an appointment or pay a fee), but the process must be finished in person; 3 = fully online end to end, including delivery of the decision or document (digital document or postal/courier delivery). Revised after the pilot: downloadable forms moved from level 2 to level 1.'),
    ('C2', 'Digital identity', ['0', '1', '2', 'NA'],
     '0 = no login needed or offered; 1 = service-specific or portal account (username/password, or national ID number plus SMS code); 2 = state-issued digital-identity credential (national eID or mobile ID app, state-recognised certificate, national single sign-on such as Nafath). NA if C1 < 2. (Rule R1)'),
    ('C3', 'Online payment', ['0', '1', 'NA'],
     '0 = fee exists but cannot be paid online; 1 = fee can be paid online; NA = no fee, or C1 < 2.'),
    ('C4', 'Once-only (data reuse)', ['0', '1', '2', 'NA'],
     '0 = applicant must supply documents the government already holds (e.g. copy of national ID, birth certificate); 1 = some data pre-filled or retrieved from registries; 2 = official text states no such documents are needed / data retrieved automatically. NA if no document requirements are published.'),
    ('C5', 'Reachable from the national portal', ['0', '1', '2'],
     '0 = not reachable from the national portal (or none exists); 1 = national portal links out to an agency site; 2 = service integrated in the national portal.'),
    ('C6', 'Arabic / national-language version', ['0', '1'], '1 = service information available in the country\'s main official language (Arabic for Arab states, Korean for Korea, English for South Africa).'),
    ('C7', 'English version', ['0', '1'], '1 = service information available in English.'),
    ('C8', 'Mobile access', ['0', '1'], '1 = official mobile app offers the service, or the service page works on a phone screen (responsive).'),
    ('C9', 'Assisted channel stated', ['0', '1', 'NA'], '1 = the page names a physical or assisted channel (service centre, agent, call centre) for people who cannot use the online service. NA if C1 <= 1 (Rule R3).'),
    ('C10', 'Time and cost published', ['0', '1'], '1 = both processing time and fee (or "free") are stated.'),
    ('C11', 'Status tracking', ['0', '1', 'NA'], '1 = applicant can track application status online; NA if C1 < 2 or if the transaction is completed immediately (Rule R5).'),
    ('C12', 'Assisted digital channel', ['0', '1'], '1 = an official intermediary (bank branch, post office, licensed agent, kiosk, service house) carries out the digital transaction on behalf of the applicant, as an optional channel. Self-service kiosks, cash-payment counters and mandatory or private professionals (tax agents, architects, engineering offices) are 0 (Rule R2). Added after the pilot (South Africa bank branches).'),
]
PORTAL_ITEMS = [
    ('P1', 'National single services portal exists', '0/1'),
    ('P2', 'Number of services listed (as stated by the portal, with date)', 'number'),
    ('P3', 'Search function', '0/1'),
    ('P4', 'Privacy policy or data-protection statement on the portal', '0/1'),
    ('P5', 'Accessibility statement', '0/1'),
    ('P6', 'Feedback or complaints mechanism', '0/1'),
    ('P7', 'National digital identity / single sign-on offered', '0/1'),
    ('P8', 'Open-data portal linked', '0/1'),
    ('P9', 'Earliest Wayback Machine capture of the portal (year)', 'year'),
    ('P10', 'Services listed in a Wayback capture about 5 years earlier (number, with capture date)', 'number'),
]


# Pilot of S03 (passport renewal), 22 November 2026, one coder. Blank = not yet determined.
PILOT = [
    ['LBY', 'Libya', '2026-11-22', 'ejraat.gov.ly/procedure/48; nid.gov.ly; reservation.nid.gov.ly', 'Certificate error', '1', 'NA', 'NA', '0', '2', '1', '1', 'NA', '0', 'Scored; booking site to retry',
     'eJraat lists 4 in-person steps (appointment, photo, fee, collection) at the Passports and Nationality Department; 9 documents incl. electronic birth certificate, family status certificate, residence certificate and family album (government-held data, C4 = 0); cost LYD 50.5; 2.5-10.5 days. nid.gov.ly links to an online booking site (reservation.nid.gov.ly) that failed the browser HTTPS certificate check; nid.gov.ly footer still links to the Government of National Accord (ended 2021). If booking works on retry, C1 = 2.'],
    ['TUN', 'Tunisia', '2026-11-22', 'khadamet.gov.tn (Interior section); interieur.gov.tn', 'OK', '1', 'NA', 'NA', '', '0', '', '0', 'NA', '0', 'Scored (partial)',
     'Passport not on the national portal (Interior section lists only criminal-record certificate online and its tracking). Interior Ministry site offers a downloadable passport form (PDF). Biometric passport project still pending per ministry and press.'],
    ['EGY', 'Egypt', '2026-11-22', 'digital.gov.eg (civil services)', 'OK', '', '', '', '', '', '', '', '', '', 'Provisional: official page not found',
     'Passport not found in Digital Egypt civil-services category. Press reports online renewal with online payment and home delivery via the Passports Department; press is not admissible evidence, so the official service page must be located before scoring.'],
    ['ZAF', 'South Africa', '2026-11-22', 'gov.za media statement 18 Nov 2026 (Department of Home Affairs)', 'OK', '1', 'NA', '', '2', '1', '1', '', 'NA', '1', 'Provisional: check myhomeaffairsonline.dha.gov.za',
     'Adult passport applications live at 480 bank branches (708 locations in total) with "no prior bookings, paperwork, or queues"; courier delivery announced for the next phase. Self-service online application not yet confirmed.'],
    ['SAU', 'Saudi Arabia', '2026-11-22', 'absher.sa FAQ; my.gov.sa (blocked)', 'Blocked (bot check / geo)', '3', '2', '1', '', '', '', '', '', '1', 'Scored (partial); my.gov.sa to retry',
     'Absher FAQ (official) describes online passport renewal and postal delivery to the registered national address. my.gov.sa returned a Cloudflare check from this location; Absher services sit behind login. C3 based on renewal fee payment in Absher; confirm on the service page.'],
    ['KOR', 'Republic of Korea', '2026-11-22', 'gov.kr / plus.gov.kr search', 'OK', '2', '', '', '', '2', '', '', '1', '0', 'Scored (partial)',
     'Government24 lists "passport reissue online application" (expiry, loss) and an online passport issuance-status service; first issuance requires a visit. Collection versus delivery and login method to confirm on the service page.'],
]

H = Font(bold=True, color='FFFFFF'); HF = PatternFill('solid', fgColor='1F3864')
WRAP = Alignment(wrap_text=True, vertical='top')


def header(ws, cols, widths):
    ws.append(cols)
    for i, w in enumerate(widths, 1):
        c = ws.cell(row=1, column=i); c.font = H; c.fill = HF; c.alignment = WRAP
        ws.column_dimensions[c.column_letter].width = w
    ws.freeze_panes = 'A2'


wb = Workbook()
ws = wb.active; ws.title = 'Instructions'
for line in [
    'Portal audit: Libya, Tunisia, Egypt, South Africa, Saudi Arabia, Republic of Korea',
    '',
    'Purpose: original, replicable data on how 12 everyday public services are delivered online in each country.',
    'Read the protocol (Portal_Audit_Protocol.docx) before coding. Definitions are in the Codebook sheet.',
    '1. Record each portal once in the Portal_level sheet.',
    '2. For each country x service row in Scoring, search the national portal first, then the responsible agency site.',
    '3. Score only what is publicly visible without logging in. Do not create accounts or submit applications.',
    '4. For every score, log the evidence (URL, access date, screenshot file name) in the Evidence sheet.',
    '5. Two coders score independently; a 20% random sample is double-coded and Cohen\'s kappa reported.',
    '6. Record the coder initials and the access date on every row. Re-check any page that changes during the audit window.',
]:
    ws.append([line])
ws.column_dimensions['A'].width = 120
ws['A1'].font = Font(bold=True, size=13)

ws = wb.create_sheet('Countries')
header(ws, ['ISO3', 'Country', 'Role in design', 'National portal URL', 'Notes'], [8, 20, 30, 34, 90])
for r in COUNTRIES:
    ws.append(list(r))
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment = WRAP

ws = wb.create_sheet('Services')
header(ws, ['Code', 'Service', 'Domain'], [8, 60, 20])
for r in SERVICES:
    ws.append(list(r))

ws = wb.create_sheet('Codebook')
header(ws, ['Code', 'Criterion', 'Allowed values', 'Definition'], [8, 30, 16, 120])
for code, name, vals, defn in CRITERIA:
    ws.append([code, name, ' / '.join(vals), defn])
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment = WRAP

ws = wb.create_sheet('Scoring')
cols = ['ISO3', 'Country', 'Service code', 'Service', 'Responsible agency', 'Service page URL', 'Access date (YYYY-MM-DD)', 'Coder', 'Access status']
cols += [f'{c[0]} {c[1]}' for c in CRITERIA] + ['Evidence IDs', 'Notes']
header(ws, cols, [7, 16, 8, 40, 26, 40, 14, 8, 18] + [12] * len(CRITERIA) + [16, 50])
for iso, cname, *_ in COUNTRIES:
    for scode, sname, _ in SERVICES:
        ws.append([iso, cname, scode, sname] + [''] * (len(cols) - 4))
first = 10
dv_acc = DataValidation(type='list', formula1='"OK,Certificate error,Blocked (bot check / geo),Not found (404),Login required"', allow_blank=True)
ws.add_data_validation(dv_acc); dv_acc.add(f'I2:I{len(COUNTRIES) * len(SERVICES) + 1}')
for j, (code, name, vals, _) in enumerate(CRITERIA):
    dv = DataValidation(type='list', formula1='"' + ','.join(vals) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    col = ws.cell(row=1, column=first + j).column_letter
    dv.add(f'{col}2:{col}{len(COUNTRIES) * len(SERVICES) + 1}')

ws = wb.create_sheet('Portal_level')
pcols = ['ISO3', 'Country', 'Portal URL', 'Access date', 'Coder'] + [f'{p[0]} {p[1]}' for p in PORTAL_ITEMS] + ['Evidence IDs', 'Notes']
header(ws, pcols, [7, 16, 30, 12, 8] + [16] * len(PORTAL_ITEMS) + [16, 50])
for iso, cname, _, url, _ in COUNTRIES:
    ws.append([iso, cname, url] + [''] * (len(pcols) - 3))

ws = wb.create_sheet('Evidence')
header(ws, ['Evidence ID', 'ISO3', 'Service code or P-item', 'URL', 'Access date', 'Screenshot / PDF file name', 'Wayback URL (optional)', 'What it shows'],
       [12, 7, 14, 50, 12, 30, 40, 60])

ws = wb.create_sheet('Pilot_S03_passport')
header(ws, ['ISO3', 'Country', 'Access date', 'Source checked', 'Access status', 'C1', 'C2', 'C3', 'C4', 'C5', 'C9', 'C10', 'C11', 'C12', 'Status of coding', 'Evidence and notes'],
       [7, 16, 11, 40, 18, 5, 5, 5, 5, 5, 5, 5, 5, 5, 16, 90])
for row in PILOT:
    ws.append(row)
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment = WRAP

ws = wb.create_sheet('Reliability')
header(ws, ['Row (ISO3-Service)', 'Criterion', 'Coder A', 'Coder B', 'Agreed value', 'Note'], [18, 26, 10, 10, 12, 50])

os.makedirs('audit', exist_ok=True)
out = os.path.join('audit', 'Portal_Audit_Workbook.xlsx')
wb.save(out)
print('saved', out, '| scoring rows', len(COUNTRIES) * len(SERVICES))
