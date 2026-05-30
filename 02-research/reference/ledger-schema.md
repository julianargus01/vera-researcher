# Evidence Ledger Schema

This is the verbatim schema `02-research/output/evidence-ledger.md` must conform to.

**Usage:** Phase 2 Step 10 instructs the primary to write the ledger using this schema. Phase 3 Step 1 verifies the written ledger contains the SEARCH LOG and Audit sections defined here before delivery.

Required sections (in this order):

```
EVIDENCE-LEDGER

STRENGTH SUMMARY
T1 (Cochrane/meta): X sources — [supports / no clear benefit / against / mixed]
T2 (RCTs): X sources — [direction]
T3 (observational): X sources — [direction]
T4 (case reports): X sources — [direction]
T5 (grey literature): X sources — [direction]
T6 (anecdotal claims surveyed): X — [dominant claim direction]
Net strength: STRONG | MODERATE | MIXED | WEAK | INSUFFICIENT
Reason: <one-line summary>

DIRECTION & CONFIDENCE (for Phase 3 dashboard — `03-delivery/reference/template-keys.md` D18)
- Will it help?  dots: <int 0–5>  label: <one of: "Yes" | "Probably yes" | "Maybe" | "Probably not" | "No" | "We can't tell yet">  explain: <one plain-language sentence>
- Could it hurt? dots: <int 0–5>  label: <same value space>  explain: <one plain-language sentence>

Dots = confidence in the answer (not strength of evidence in favor). Direction lives in the words. Strong evidence against = high dots + "No" / "Probably not". No evidence at all = 0 dots + "We can't tell yet". See `03-delivery/reference/voice.md` for the full dot semantic table.

COUNTS (for Phase 3 patient-facing count list — NO tier codes visible to patient)
- Group findings into plain-language categories the patient can read at a glance. Tag the most relevant gap or safety signal with a one-word badge:
  - <n>: High-quality reviews (Cochrane / meta-analyses) [optional tag]
  - <n>: Clinical trials (RCTs) [optional tag]
  - <n>: Smaller studies / case reports
  - <n>: Online claims surveyed [optional tag]
  - <n>: <case-specific category if useful>  [tag: "biggest gap" | "safety" | etc.]

Question: <verbatim Research question from scoping-summary.md>
Population: <cancer type/stage, prior treatments, current regimen, age, sex, comorbidities, relevant supplements/meds, conditional fields>

T1 — Cochrane Reviews / Meta-analyses
- [Author, Year, Title, Source URL] — T1 — [COI or NONE] — [1-line finding]
  (URL is required — Phase 3 hyperlinks the citation in findings + references)

T2 — Individual RCTs
- [Author, Year, Title, Source] — T2 — [COI or NONE] — [1-line finding]

T3 — Observational Studies
- ...

T4 — Case Reports / Series  |  T5 — Grey Literature
- ...

T6 — Anecdotal / Patient-encountered claims
- [Source: Reddit r/X | Podcast Y | Inspire forum | TikTok trend] — T6 — [COI or NONE] — [prevalence: rare/common/viral] — [claim being made]

Structural COI considerations:
- Corporate research-agenda capture: <if relevant>
- Political/regulatory capture: <if relevant>
- Geographic capture: <if relevant>
- Ideological capture: <if relevant>
- Publication bias: <if relevant>

Conflicts:
- [Study A] vs [Study B]: [design/size/funding + nature of conflict]

Gaps — what the evidence does NOT cover:
- [Population, stage, outcome not represented]
- [Reason absent — including research-agenda gaps]

SEARCH LOG (Step 1.5 — minimum 12 entries; logged as searches happen, not backfilled)
- [YYYY-MM-DD HH:MM] action: query  source: Europe PMC  query: "<exact text>"  result: <count>  classification: <T-bucket or off-topic>
- [YYYY-MM-DD HH:MM] action: query  source: PubMed  query: "<exact text>"  result: <count>  classification: <T-bucket>
- [YYYY-MM-DD HH:MM] action: fetch  source: <URL>  result: <success/empty/fail>  classification: <T-tier>
- [YYYY-MM-DD HH:MM] action: anecdotal  source: Reddit r/<sub>  query: "<terms>"  result: <count of claims>  classification: T6
- ... (≥12 entries total across the source chain)

Audit (Step 9.5 self-audit + Step 9.6 adversarial sub-agent crosscheck):
- Self-audit re-checks: <synonyms, alternate names, related cancer types searched after first pass>
- Self-audit gaps surfaced and addressed: <list, or "none found">
- Sub-agent crosscheck status: <"audit-notes.md written by sub-agent <id>" OR "Sub-agent unavailable: <verbatim error>; fallback expanded self-audit performed">
- Audit reconciliation (item by item, by task number):
  - TASK 1 (source verification): <each flagged mismatch and the correction applied>
  - TASK 2 (independent searches): <integrated into SEARCH LOG above>
  - TASK 3 (missed sources): <each missed source from audit-notes.md, with where in the ledger it was added>
  - TASK 4 (COI corrections): <each correction applied to per-source citations or Structural COI section>
  - TASK 5 (data connections): <each connection integrated into Findings or Structural COI>
  - TASK 6 (loop-back decision): <"no loop-back triggered" OR "loop-back executed per Loop-back trigger procedure">
- Net strength rating change from audit: <unchanged | changed from X to Y because Z>
```
