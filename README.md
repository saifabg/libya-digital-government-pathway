# Supplementary materials (anonymised for review)

**Learning from leaders and neighbours: a readiness-gated pathway for digital government in Libya**

These files let reviewers check and reproduce every number, table and figure in the manuscript. They contain no author names.

## Contents

| Folder | What it contains | Used in the manuscript |
|---|---|---|
| `data/raw/` | UN E-Government Survey country data 2003–2026 (UN DESA E-Government Knowledgebase, `ekap_egdi_all_countries_2003_2026.json`); World Bank indicators from the public API (`worldbank_indicators.csv`: Worldwide Governance Indicators, GDP per capita, population, oil rents); World Bank GovTech datasets, October 2022 and December 2025 editions | Section 3.3 |
| `data/` | `panel_un_wb.csv` (country-edition panel, 2008–2026); `gtmi_stage_indices.csv` (governance, foundations and measurement indices from the GovTech data) | Tables 3, 4, 7 |
| `code/` | Analysis scripts, run in the order below | All results |
| `results/` | Model output, residuals, audit indices, GovTech tests, reliability, decision-rule log, figures | Tables 1–9, Figures 1–2 |
| `audit/` | Audit protocol, workbook (codebook, scores, evidence log), raw and standardised coding, saved page extracts for every country and service, second-coder sheets | Section 4.2, Table 5, Figure 2 |
| `reform_histories/` | Reform timelines for Korea, Saudi Arabia, South Africa and Egypt, with sources and lists of claims that could not be verified | Section 4.3, Table 8 |
| `framework/` | Extended description of the pathway and its evaluation; Figure 3 | Sections 5–6, Tables 6, 7, 9 |

## Reproducing the results

Python 3.12 with the packages in `requirements.txt`. Run every script from this folder:

```
python -I code/01_fetch_worldbank.py      # optional: re-downloads World Bank indicators (values may change with later API revisions)
python -I code/02_build_panel.py          # builds data/panel_un_wb.csv
python -I code/03_models.py               # models M1-M4, robustness checks, residuals, Figure 1 -> results/models.txt, residuals_*.csv, fig_residuals.png
python -I code/06_standardise.py          # applies decision rules R1-R6 to audit/coding -> audit/coding_std, results/standardisation_log.csv
python -I code/05_merge_audit.py          # validates the coding, fills the workbook, audit indices, Figure 2 -> results/audit_*.csv, fig_audit_heatmap.png
python -I code/07_framework_figure.py     # Figure 3
python -I code/08_gtmi_tests.py           # tests of propositions P1-P5 and the Libya prediction -> results/gtmi_tests.txt, gtmi_libya_profile.csv
python -I code/09_reliability.py audit/Second_Coder_Sheet_AI_coderB.xlsx _AI_coderB   # inter-coder agreement and Cohen's kappa
```

`code/04_make_audit_workbook.py` builds the empty audit workbook; `05_merge_audit.py` runs it automatically before filling in the scores.
Running steps 02–09 on the files supplied reproduces the outputs in `results/` exactly (checked on 23 November 2026).

## The portal audit

- Protocol: `audit/Portal_Audit_Protocol.docx` (services, criteria C1–C12, decision rules, evidence rules).
- Coder A (AI-assisted) coded all 72 country-service rows from official public pages on 22 November 2026: raw coding in `audit/coding/`, page extracts in `audit/evidence/<country>/`. The instructions given to the coder are in `audit/AI_coder_A_instructions.md`.
- Decision rules R1–R6 were then applied to all rows (`results/standardisation_log.csv` lists all 46 changed cells); standardised scores are in `audit/coding_std/`.
- Second coding: a blind, independent AI coder (coder B) re-coded a random sample of 15 rows on 22–23 November 2026 without access to coder A's scores (`audit/coderB_AI/`, `audit/Second_Coder_Sheet_AI_coderB.xlsx`; results in `results/reliability_AI_coderB.txt`). `audit/Second_Coder_Sheet_BLIND.xlsx` is the blank sheet for a human coder.
- No accounts were created and nothing was submitted on any government site.

## Known limitations of the materials

- Government web pages change; the saved extracts in `audit/evidence/` record what was visible on the audit dates.
- Two official sites were unreachable on the audit date (Libya's electricity company; Tunisia's vehicle circulation tax).
- Some Saudi and Egyptian official pages could be read only through Internet Archive copies; these are marked in the reform histories.
- The UN data were read from the UN DESA E-Government Knowledgebase; computed ranks can differ by one place from the UN's published ranks where scores are tied.
