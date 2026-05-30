# Template Keys — Canonical placeholder list for `final-report` deliverable

The Phase 3 agent populates these keys from `scoping-summary.md` + `evidence-ledger.md`, then passes the populated dict to `render_deliverable.py`.

## Hero & verdict

| Key | Source | Type | Notes |
|---|---|---|---|
| `TITLE` | scoping-summary | string | One-line case title, e.g., "Fasting during R-CHOP for Stage III non-Hodgkin lymphoma" |
| `PATIENT_META` | scoping-summary | string | "49M · Stage III NHL · about to start R-CHOP · fish oil + turmeric + Zyrtec · 190 lb, appetite stable" |
| `REPORT_DATE` | runtime | ISO date | "2026-05-29" |
| `VERDICT_PARAGRAPH` | Phase 3 synthesis | string | 4-6 sentence honest-answer paragraph at 6th-grade reading level; explains the absence of evidence when applicable; does not lead with a single-word rating |

## Dashboard — two-question rating

| Key | Source | Type | Notes |
|---|---|---|---|
| `HELP_DOTS_FILLED` | Phase 3 from ledger STRENGTH SUMMARY | int 0–5 | Confidence in the WILL IT HELP answer |
| `HELP_LABEL` | Phase 3 | string | "We can't tell yet" / "Maybe" / "Probably yes" / "Yes" / "No" / "Probably not" |
| `HELP_EXPLAIN` | Phase 3 | string | One sentence explaining the rating, plain language |
| `HURT_DOTS_FILLED` | Phase 3 | int 0–5 | Confidence in the COULD IT HURT answer |
| `HURT_LABEL` | Phase 3 | string | Same value space as HELP_LABEL |
| `HURT_EXPLAIN` | Phase 3 | string | One sentence |

## Dashboard — count list

| Key | Source | Type | Notes |
|---|---|---|---|
| `COUNTS` | Phase 3 from ledger | list of `{n: int, label: str, tag: optional str}` | Each item renders as: big coral number + plain-language label + optional "biggest gap" / "safety" tag |

## Findings (page 2)

| Key | Source | Type | Notes |
|---|---|---|---|
| `FINDINGS` | Phase 3 from ledger | list of `{text: str, url: optional str, coi: optional str}` | Plain-language at 6th-grade. `text` is the full sentence. If present, `url` is wrapped around the bolded study-name span. `coi` only set when a conflict exists — "Conflict of interest: ..." printed after the finding (never abbreviated). |
| `ANEC_PARAGRAPHS` | Phase 3 from ledger T6 + Structural COI | list of strings | 1–3 paragraphs. Names platforms specifically (Reddit, podcasts). Traces claims to source. Explains structural-COI in plain language when relevant. |

## Gaps (page 3)

| Key | Source | Type | Notes |
|---|---|---|---|
| `GAPS` | Phase 3 from ledger Gaps section | list of `{headline: str, body: str}` | `headline` is bold short summary. `body` is 1–2 plain-language sentences explaining what the gap means for the patient. |

## Questions (page 4)

| Key | Source | Type | Notes |
|---|---|---|---|
| `QUESTIONS_LEDE` | Phase 3 | string | Conditional opener — "If you're still thinking about trying [X]…" when verdict is maybe/unknown; "If you're weighing this against your doctor's view…" when verdict is strong-against. |
| `QUESTIONS` | Phase 3 derived from gaps + patient context | list of `{ask: str, why: str}` | 3–5 questions. Each `ask` is the question text, `why` is one italic line explaining why this question matters for this patient. |

## Clinical Summary (page 5 — oncologist-facing)

| Key | Source | Type | Notes |
|---|---|---|---|
| `CLINICAL_KV` | scoping-summary + ledger | list of `{label: str, value: str}` | Patient context, current treatment, comorbidities & meds, conditional context, research question, intervention |
| `CLINICAL_BLOCKS` | Phase 3 from ledger | list of `{title: str, body: str/html}` | Required blocks in order: "Strongest Evidence" (citation list, no tier codes, full funding statement), "Structural COI" (plain-language explanation), "Interaction Concerns", "Evidence Gaps" |

## References (page 6)

| Key | Source | Type | Notes |
|---|---|---|---|
| `REFERENCES` | Phase 3 from ledger | list of `{citation: str, url: str}` | Every reference is a hyperlink. URL preferences: PubMed > journal open-access > ClinicalTrials.gov > government PDQ > Cochrane Library. Anecdotal sources are NOT included in references. |

## Overflow handling

When a list exceeds its target page (>5 findings, >5 gaps, >5 questions), the renderer applies the D20 proportional shrink. The Phase 3 agent should still try to keep lists to ≤5 items each by selecting the most clinically relevant; let the renderer handle minor overflow.

## Locked at v0 — 2026-05-29

Any structural change (new section, new dot semantic, new required field) bumps to v1. Internal data revisions stay at v0.
