# Adversarial Sub-Agent Audit Brief

This is the verbatim prompt the primary agent passes to the sub-agent in Phase 2 Step 9.6.

**Usage:** Phase 2 Step 9.6 instructs the primary to load this file and pass its contents verbatim as the sub-agent's prompt — substitute only the angle-bracketed placeholders in the brief. Paraphrasing is forbidden (Step 9.6 FORBIDDEN clause).

---

**AUDIT BRIEF**

You are an adversarial auditor reviewing a research ledger produced by a primary agent on this scoped question:

`<copy the verbatim Research question from 01-scoping/output/scoping-summary.md>`

Patient context:

`<copy verbatim from scoping-summary.md — type/stage, prior treatments, current regimen, profile, conditional fields>`

The primary agent is suspected of shallow retrieval. The specific failure pattern we are auditing for: claiming databases were searched (e.g., "Europe PMC ✓, PubMed ✓") while having retrieved zero or near-zero sources for an intervention where sources demonstrably exist. Assume the ledger is incomplete until you prove otherwise.

**Read these files in order before starting:**
1. `01-scoping/output/scoping-summary.md` — patient context
2. `02-research/output/evidence-ledger.draft.md` — the draft ledger you are auditing (includes SEARCH LOG)
3. `02-research/reference/evidence-tiers.md` — the 6-tier hierarchy you must use
4. `02-research/reference/coi-flags.md` — COI schema (per-source + 5 structural patterns)
5. `02-research/reference/source-databases.md` — source chain you must search

**Execute these six tasks. Each task must produce concrete output in audit-notes.md.**

**TASK 1 — Verify every cited source.** For each source in the draft ledger, fetch the URL and confirm: (a) it exists, (b) the tier assignment is correct per evidence-tiers.md, (c) the one-line finding summary is faithful to what the source actually says. Flag every mismatch.

**TASK 2 — Independent search.** Run your own searches across the full source chain (Europe PMC, PubMed, ClinicalTrials.gov, Semantic Scholar, Unpaywall, WebSearch, plus anecdotal platforms per source-databases.md). Use synonyms and adjacent variations the primary may have missed: brand vs generic, common vs scientific name, adjacent cancer types, adjacent regimens, mechanism-only queries, alternate spellings. Minimum: 8 distinct queries you run yourself, logged with results.

**TASK 3 — Produce a missed-sources list.** Hard requirement: identify at least 5 sources the primary did not cite, OR document with the specific 8+ queries you ran in Task 2 that the literature is genuinely sparse beyond what the primary captured. "Absence confirmed" without the query log is not acceptable — it is the failure mode this audit exists to catch.

**TASK 4 — Probe COI aggressively.** For every T1–T3 source in the primary's draft AND every source you found, check: funding source, author affiliations, practitioner-researcher conflicts, and the 5 structural-COI patterns from coi-flags.md (corporate research-agenda capture, political/regulatory, geographic, ideological, publication bias). List every COI the primary missed or under-played.

**TASK 5 — Find data connections.** Identify connections in the retrieved evidence the primary did not make: drug-class effects across studies, mechanism overlap, dose-response patterns, contradictions between high-tier and low-tier sources, suspiciously aligned findings, gaps that point to a research-agenda story the primary missed.

**TASK 6 — Loop-back decision.** Per the Loop-back trigger section in `02-research/rules.md`, determine whether any retrieved evidence suggests the question needs revisiting (intervention has multiple meanings, profile gap that shapes interpretation, drug-interaction concern depending on undisclosed med, safety signal needing lab data). If yes, name the specific trigger and the exact clarifying question to send.

**Write your findings to `02-research/output/audit-notes.md` using this exact structure (mandatory format — do not reorder, do not omit any task, do not skip empty tasks):**

```
ADVERSARIAL AUDIT
Auditor: <sub-agent ID or model name>
Audited draft: 02-research/output/evidence-ledger.draft.md
Timestamp: <YYYY-MM-DD HH:MM>

TASK 1 — Source verification
- <citation as in draft>: verified | tier mismatch (primary said TX; actual TY because Z) | finding-summary mismatch (primary said X; source actually says Y)
- ...

TASK 2 — Independent searches run
- [timestamp] source: <db> query: "<text>" → <result count> | <tier-1-bucket>
- ... (minimum 8 entries)

TASK 3 — Missed sources
- [Author, Year, Title, URL, proposed tier, proposed COI flag, one-line finding]
- ... (minimum 5 entries, OR a written absence statement referencing the 8+ queries from Task 2)

TASK 4 — COI corrections
- <source-id>: primary said <X>; actual COI is <Y> with funding evidence <link or affiliation>
- ...

TASK 5 — Data connections
- <one-sentence connection>
- ...

TASK 6 — Loop-back decision
- Recommended: yes | no
- Trigger (if yes): <name from Loop-back trigger section>
- Proposed clarifying question (if yes): "<exact text>"
```

Be adversarial. The primary's defense is "I searched and there's nothing." Your job is to test that claim by running the searches yourself.
