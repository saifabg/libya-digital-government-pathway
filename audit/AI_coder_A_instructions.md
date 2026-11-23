# Portal audit brief (coder A, 2026-11)

Study folder: D:\papers\done\Libya_DT_six_country_study. Full protocol: audit/protocol_source.txt (read sections 4, 5, 7 and 9).

## Hard rules
- Official sources only: national portal, the responsible ministry/agency website, its official app-store listing, or official government announcements. News, blogs, private agents and Wikipedia are NOT evidence (you may use them only to find the official page).
- Observe only what is publicly visible. Never log in, create accounts, submit forms, start applications or pay.
- Never bypass bot checks, CAPTCHAs, Cloudflare pages or browser security warnings (certificate errors). Record them as Access status and move on.
- Every score needs evidence. For each row save one evidence file audit/evidence/<ISO3>/<Service code>.txt containing: the URL(s), the access date (YYYY-MM-DD), and a short verbatim excerpt (max ~1,500 characters) of the official text that supports the scores. Evidence ID = <ISO3>_<Service code>.
- If you cannot determine a criterion from official evidence, leave it blank and say why in Notes. Do not guess. Blank is better than wrong.
- Score C2, C3, C11 as NA when C1 < 2. C3 is NA if there is no fee.
- Coder = AI-A. Access date = the date you checked.

## Services (code, name, domain)
- S01: Birth registration / birth certificate (Civil status)
- S02: National ID card: first issue or renewal (Identity)
- S03: Passport renewal (Identity / travel)
- S04: Civil-status extract (e.g. family record, marriage certificate) (Civil status)
- S05: Company (business) registration (Business)
- S06: Commercial or business activity licence (Business)
- S07: Income or corporate tax filing and payment (Tax)
- S08: Electricity bill payment (public utility) (Utilities)
- S09: Vehicle registration renewal (Transport)
- S10: Public university admission / enrolment (Education)
- S11: Social-assistance or social-security benefit application (Social protection)
- S12: Building permit (Municipal)

## Criteria (code, name, allowed values, definition)
- C1 Service maturity [0/1/2/3]: 0 = no official online information; 1 = information only (steps, documents, fees), including downloadable forms; 2 = partly online: at least one step can be done online by the applicant (submit an application, book an appointment or pay a fee), but the process must be finished in person; 3 = fully online end to end, including delivery of the decision or document (digital document or postal/courier delivery). Revised after the pilot: downloadable forms moved from level 2 to level 1.
- C2 Digital identity [0/1/2/NA]: 0 = no login needed or offered (or service not online); 1 = service-specific or portal account (username/password, SMS code); 2 = national digital identity (eID, mobile ID, national single sign-on). NA if C1 < 2.
- C3 Online payment [0/1/NA]: 0 = fee exists but cannot be paid online; 1 = fee can be paid online; NA = no fee, or C1 < 2.
- C4 Once-only (data reuse) [0/1/2/NA]: 0 = applicant must supply documents the government already holds (e.g. copy of national ID, birth certificate); 1 = some data pre-filled or retrieved from registries; 2 = official text states no such documents are needed / data retrieved automatically. NA if no document requirements are published.
- C5 Reachable from the national portal [0/1/2]: 0 = not reachable from the national portal (or none exists); 1 = national portal links out to an agency site; 2 = service integrated in the national portal.
- C6 Arabic / national-language version [0/1]: 1 = service information available in the country's main official language (Arabic for Arab states, Korean for Korea, English for South Africa).
- C7 English version [0/1]: 1 = service information available in English.
- C8 Mobile access [0/1]: 1 = official mobile app offers the service, or the service page works on a phone screen (responsive).
- C9 Assisted channel stated [0/1]: 1 = the page names a physical or assisted channel (service centre, agent, call centre) for people who cannot use the online service.
- C10 Time and cost published [0/1]: 1 = both processing time and fee (or "free") are stated.
- C11 Status tracking [0/1/NA]: 1 = applicant can track application status online; NA if C1 < 2.
- C12 Assisted digital channel [0/1]: 1 = an official intermediary (bank branch, post office, licensed agent, kiosk, service house) carries out the digital transaction on behalf of the applicant. Added after the pilot (South Africa bank branches).

## Portal-level items (one row per country)
- P1 National single services portal exists (0/1)
- P2 Number of services listed (as stated by the portal, with date) (number)
- P3 Search function (0/1)
- P4 Privacy policy or data-protection statement on the portal (0/1)
- P5 Accessibility statement (0/1)
- P6 Feedback or complaints mechanism (0/1)
- P7 National digital identity / single sign-on offered (0/1)
- P8 Open-data portal linked (0/1)
- P9 Earliest Wayback Machine capture of the portal (year) (year)
- P10 Services listed in a Wayback capture about 5 years earlier (number, with capture date) (number)

For P9/P10 use the Internet Archive API, e.g. curl -s "https://archive.org/wayback/available?url=<portal>&timestamp=2016" and http://web.archive.org/cdx/search/cdx?url=<portal>&limit=1 for the earliest capture; you may open archived pages to count listed services.

## Output files (UTF-8 CSV with header, exactly these columns)
1. audit/coding/<ISO3>.csv — 12 rows (S01–S12):
   ISO3,Country,Service code,Service,Responsible agency,Service page URL,Access date,Coder,Access status,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,Evidence IDs,Notes
   Access status values: OK | Certificate error | Blocked (bot check / geo) | Not found (404) | Login required
2. audit/coding/<ISO3>_portal.csv — 1 row:
   ISO3,Country,Portal URL,Access date,Coder,P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,Evidence IDs,Notes

Write CSVs with Python's csv module (python -I) so commas inside notes are quoted. Use plain values exactly as allowed (e.g. 0, 1, 2, 3, NA).

## Tools
Prefer WebFetch/WebSearch/curl. Many portals render with JavaScript: then use the Claude in Chrome tools — create YOUR OWN tab with tabs_create_mcp, read with javascript_tool (document.body.innerText) or get_page_text, and close your tab when done. Do not touch other tabs.
