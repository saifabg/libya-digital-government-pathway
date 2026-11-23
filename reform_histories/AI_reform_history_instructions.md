# Reform-history brief

Goal: explain HOW each comparison country improved its digital government, focusing on the turning points in its UN E-Government Development Index (EGDI) world rank. This feeds a paper comparing Libya with Tunisia, Egypt (neighbours), South Africa (Africa #1), Saudi Arabia (Arab #1) and the Republic of Korea (world #1, 2026).

UN EGDI world rank by edition (computed from UN DESA data):
| Country | 2003 | 2004 | 2005 | 2008 | 2010 | 2012 | 2014 | 2016 | 2018 | 2020 | 2022 | 2024 | 2026 |
| Korea | 13 | 5 | 5 | 6 | 1 | 1 | 1 | 3 | 3 | 2 | 3 | 4 | 1 |
| Saudi Arabia | 104 | 89 | 80 | 70 | 58 | 41 | 36 | 44 | 52 | 43 | 31 | 6 | 4 |
| South Africa | 45 | 55 | 58 | 61 | 97 | 101 | 92 | 77 | 68 | 78 | 65 | 40 | 52 |
| Egypt | 140 | 136 | 99 | 79 | 86 | 107 | 79 | 108 | 114 | 111 | 103 | 95 | 109 |
Note: the 2024 UN revision of the Telecommunications Infrastructure Index affects comparability with earlier editions.

For each assigned country, produce a timeline of the main digital-government reforms 2000–2026 and explain what happened around each turning point. Organise the explanation by the paper's five dimensions:
1. Governance and authority (lead agency, mandate, strategy, law, budget control)
2. Shared infrastructure (digital ID, single sign-on, payments, data exchange/interoperability, national portal, cloud)
3. Organisational change (process re-engineering, once-only, workforce, procurement)
4. Inclusion and trust (assisted channels, data protection law, accessibility)
5. Measurement and learning (KPIs, maturity assessments, user satisfaction, evaluation)

Rules:
- Only verified sources. Peer-reviewed articles: verify each DOI on Crossref (https://api.crossref.org/works/<DOI>) or record its OpenAlex ID. Official documents (government, UN, OECD, World Bank): load the page or PDF and confirm title and date. News may only be used to locate an official source, never as evidence.
- Never invent a reference, date, law number or figure. If you cannot verify something, list it under "not verified".
- At least 5 peer-reviewed sources per country, plus official documents for key dates (laws, agency creation, ID/portal launches).
- Do not log in, create accounts or bypass bot checks. If you use Chrome, open your own tab and close it.

Output: write reform_histories/<ISO3>.md (UTF-8) in D:\papers\done\Libya_DT_six_country_study with:
(a) a dated timeline table (year | reform | dimension | source key);
(b) for each turning point, 1–2 paragraphs explaining the plausible mechanisms, and their limits;
(c) a short assessment of what is transferable to Libya and what depends on conditions Libya lacks;
(d) a reference list in APA 6 (journal articles: no issue number unless issues restart at page 1; "doi:" prefix), each with how it was verified (Crossref DOI / OpenAlex ID / URL loaded + date);
(e) "not verified" list.
Return a summary under 400 words.
