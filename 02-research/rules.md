---
title: VERA — Phase 2 Research Rules
date: 2026-05-29
phase: 02-research
pattern: 18
---

Activate when `01-scoping/output/scoping-summary.md` exists AND `02-research/output/evidence-ledger.md` does not.

**State preamble required on every response (REQUIRED — not optional):**
`[Phase: 2 | Gate: <which source is pending OR "evidence-ledger.md not yet written">]`

FORBIDDEN: dropping the state preamble.

## Inputs

| File | Why |
|------|-----|
| `01-scoping/output/scoping-summary.md` | Defines intervention, cancer type/stage, prior treatments, current regimen, target outcome, patient profile, conditional fields, and Research question |
| `examples.md` | Phase 2 calibration tape (R1–R3 ledger examples); read before producing the ledger |
| `reference/voice.md` | Phase 2 voice rules; when to speak, how to write gap statements and tier+COI annotations |
| `reference/source-databases.md` | Two-track source map: academic chain (1–6) + anecdotal/community track (7) |
| `reference/evidence-tiers.md` | 6-tier hierarchy and downgrade rules |
| `reference/coi-flags.md` | Per-source COI by tier + 5 structural-COI patterns |
| `reference/cam-categories.md` | Load only if intervention type is ambiguous |
| `reference/audit-brief.md` | Verbatim sub-agent prompt for Step 9.6 adversarial crosscheck — pass contents to sub-agent without paraphrase |
| `reference/ledger-schema.md` | Verbatim schema for evidence-ledger.md output — Phase 2 Step 10 writes per this schema; Phase 3 Step 1 validates conformance |

## Process

**1 — Parse scoped question.** Extract from scoping-summary: Research question, intervention, cancer type/stage, prior treatments, current regimen, target outcome, patient profile, and conditional fields. Population for the ledger includes patient-profile + conditional fields. Stop if scoping-summary is absent.

**1.5 — Open the SEARCH LOG.**

From this point until the ledger is written, every action that touches a source MUST be recorded in the SEARCH LOG. The log is a required section of `evidence-ledger.md` (see Output schema below). Without it, the ledger is not complete.

Each log entry uses this format:

```
[YYYY-MM-DD HH:MM] action: <query | fetch | anecdotal>  source: <database / URL / platform>  query: "<exact text>"  result: <count or success/empty/fail>  classification: <T1-T6 or "anecdotal" or "off-topic">
```

Minimum: 12 distinct log entries across the source chain before Step 10 (write ledger). Log entries include zero-result queries — a logged "PubMed query: 'mistletoe Stage II breast cancer' → 0 results" counts; an unlogged claim that PubMed was searched does not.

The SEARCH LOG exists to make "I queried X" empirically verifiable. The failure pattern this rule prevents: an agent listing "Europe PMC ✓, PubMed ✓, ClinicalTrials.gov ✓" with checkmarks while having retrieved zero sources for an intervention where the literature demonstrably exists. That pattern is grep-checkable falsification — if the log shows `PubMed query: "ivermectin cancer" → 0 results`, the adversarial sub-agent (Step 9.6) will run the same query, find 30+ hits, and the audit will flag the falsification.

FORBIDDEN: claiming a source was queried without a corresponding SEARCH LOG entry showing query text + result count.
FORBIDDEN: backfilling SEARCH LOG entries after the fact. Log as you go.
FORBIDDEN: writing the ledger with fewer than 12 SEARCH LOG entries. This is independent of the 20-source minimum in Step 9.5 — log entries can be zero-result queries; the 20-source floor counts sources actually retrieved.

**2 — Query Europe PMC first** (Source 1). Log result count.

**3 — Query PubMed + ClinicalTrials.gov in parallel** (Sources 2–3). ClinicalTrials.gov: also surface "completed, no results posted" entries as publication-bias signals. A failed source doesn't terminate — log and continue.

**4 — Descend to Semantic Scholar then Unpaywall only if needed** (Sources 4–5).

**5 — WebSearch as academic discovery fallback** (Source 6). Only after Sources 1–5 exhausted. Citation must point to primary source.

**5a — Anecdotal / community scan** (Source 7 — runs alongside academic, NOT a fallback). Per `reference/source-databases.md`, scan Reddit, podcast transcripts, patient forums, and social media for claims patients are encountering. Tag everything T5 or T6. Purpose: KNOW what the patient is hearing and address it in delivery. Record per claim: platform, prevalence (rare/common/viral), claim pattern, COI flag.

FORBIDDEN: skipping Step 5a. If the patient is asking about an intervention, they have likely encountered it in these spaces; ignoring those spaces produces a final report that fails to address what the patient actually read.

**6 — Assign tier to every source before citing it.** Use `reference/evidence-tiers.md`. Do not cite a source without an assignable tier.

**7 — Apply per-source COI flags AND screen for structural COI.** Per `reference/coi-flags.md`:

*Per-source (always check on every citation):* funding source, author affiliations, practitioner-researcher conflict. COI downgrade applies — one tier, floor T4. Flag goes inline with citation, never in a footnote.

*Structural COI (screen the WHOLE evidence base — five categories):*
- **Corporate research-agenda capture** — sparse evidence for non-patentable interventions is often a research-supply problem, not absence of effect
- **Political / regulatory capture** — findings aligning suspiciously with funder political priorities, or contentious findings suppressed
- **Geographic capture** — state-funded research promoting national medical traditions
- **Ideological capture** — sources affiliated with movements ideologically committed to the intervention (Anthroposophy + mistletoe, etc.)
- **Publication bias** — pooled estimates showing effect while trial registries reveal unpublished completed trials

Each structural flag goes in the Structural-COI section of the ledger, not on individual citations.

**8 — Name evidence gaps explicitly.** Wrong population, wrong stage, animal-only, no human data, no intervention-specific trials. Treat absence as investigative information, not null result. When absence plausibly explained by research-agenda capture, note that.

**9 — Surface conflicts, do not average them.** Name both sources, state design / sample size / funding / direction. Record conflict as its own ledger entry.

**9.5 — SELF-AUDIT before writing ledger.**

**Hard minimum: 20 distinct sources retrieved across the source chain (academic + anecdotal combined) before you may write the ledger.** Sources include peer-reviewed papers, registered trials (with or without posted results), grey-literature reports, and anecdotal/community claims from Step 5a.

If your retrieval has fewer than 20 sources, the search was shallow. Re-search using:
- Synonyms and alternate names — brand → generic, common name → scientific (mistletoe / Viscum album / iscador; ivermectin / Stromectol / avermectin)
- Adjacent populations — the patient's exact cancer type, then closely related types, then any solid tumor / hematologic context
- Adjacent regimens — the patient's specific drug, then drug class, then broader cancer-treatment context
- Broader and narrower phrasings — intervention alone, intervention + chemo, intervention + specific side effect, intervention + mechanism
- Mechanism queries — proposed mechanism + cancer biology terms

If after genuine search expansion the universe truly contains fewer than 20 sources, that is itself a finding — but the sparse-literature exemption REQUIRES all of the following before it can be invoked:

1. The SEARCH LOG records ≥15 distinct queries (not just 12 — the higher floor exists to prove exhaustive search).
2. The queries cover ALL of: synonyms/alternate names, ≥2 adjacent cancer types, ≥2 adjacent regimens, the proposed mechanism, the structural-COI explanation pattern (e.g., off-patent, jurisdictional restriction).
3. For multi-intervention questions (e.g., "ivermectin + fenbendazole + vitamin C"), search EACH intervention separately AND the named combination — the source floor scales: minimum 20 sources per named intervention, NOT 20 total. Three interventions → 60 source floor.
4. The Step 9.6 adversarial sub-agent's Task 3 missed-sources list has been EXECUTED — every search area the sub-agent identified as untried has been run and its results either added to the ledger or explicitly documented as "executed: zero results, query: <text>". Acknowledging the gap in the Gaps section without running the search does not count.

Then re-read what you retrieved as a skeptic:
- Did I miss high-tier sources? Search again with synonyms, alternate intervention names, related cancer types
- Did I under-weight contradicting evidence?
- Did I let any uncited claim sneak through?
- What would a Cochrane reviewer say about the certainty I'm implying?
- What would a CAM advocate say I missed? Address or note why excluded
- What would a regulator say is risky? Address it
- Did I capture structural COI or only per-source funding?
- Did I run the anecdotal scan (Step 5a)? Recorded the claims the final report needs to address?

If self-audit reveals gaps, address them before proceeding. Document re-checks in the ledger's Audit section.

FORBIDDEN: writing the ledger with fewer than 20 sources (or fewer than 20 × N for N-intervention questions) unless ALL FOUR sparse-literature exemption preconditions above are met AND documented in the Audit section. "I tried briefly and stopped" is the failure mode this rule exists to prevent.
FORBIDDEN: declaring the audit Task 3 missed-sources list "documented as unresolved gaps" without executing the searches. Task 3 findings must be acted on — searches run, results added (even if zero), classification + COI applied per the same standard as primary citations.
FORBIDDEN: applying the sparse-literature exemption when the named interventions are off-patent OR research-agenda-captured WITHOUT explicitly searching for the structural pattern that explains the sparsity (e.g., for off-patent: search "ivermectin off-label cancer protocols" / "fenbendazole cancer community" / etc. to surface the grey-lit and anecdotal sources that DO exist around the gap).

**9.6 — Adversarial sub-agent crosscheck — MANDATORY.**

This step is required in every environment that supports launching a sub-agent (Claude Code, Anthropic Agent SDK, OpenClaw, Cowork, Codex with delegation, any equivalent). The pattern of opt-out via "my environment doesn't support it" is forbidden — verify by attempting the launch, not by assumption.

### How to launch the sub-agent — execute this sequence exactly:

1. Confirm `02-research/output/evidence-ledger.md` does NOT yet exist. The audit runs against the DRAFT, before final write.
2. Confirm SEARCH LOG (per Step 1.5) is populated with ≥12 entries.
3. Save the current draft to `02-research/output/evidence-ledger.draft.md`. Include the SEARCH LOG in the draft.
4. Launch a fresh sub-agent. In Claude Code: use the Agent tool with `subagent_type: "general-purpose"`. In Agent SDK: equivalent delegation. Pass the brief below verbatim as the sub-agent's prompt — substitute only the angle-bracketed placeholders.

### Sub-agent brief

Load `02-research/reference/audit-brief.md` and pass its contents verbatim as the sub-agent's prompt. Substitute only the angle-bracketed placeholders shown in that file.

FORBIDDEN: paraphrasing the audit brief. The brief is locked verbatim because compressed prompts produce compressed audits — the exact failure mode this audit exists to catch.

5. Wait for the sub-agent to complete. Read `02-research/output/audit-notes.md`.

6. Reconcile every audit finding in the primary ledger before final write:
   - Add missed sources from Task 3, classifying each with tier + COI per the reference files.
   - Apply tier and finding-summary corrections from Task 1.
   - Apply COI corrections from Task 4 to existing citations and structural-COI section.
   - Integrate data connections from Task 5 into the ledger's Findings or Structural-COI section.
   - If Task 6 recommends a loop-back, execute the Loop-back trigger procedure NOW — do NOT write the final ledger. The next agent turn re-enters Phase 2 with updated scope.

7. Document each audit finding's resolution in the Audit section of the final ledger, item by item, by task number. Silent incorporation is forbidden — the final ledger must show the audit fired and was addressed.

8. Delete `evidence-ledger.draft.md`. The audited final lands at `02-research/output/evidence-ledger.md` in Step 10.

### Fallback if launch genuinely fails:

If the sub-agent tool returns an error (not "I assume my environment doesn't support it" — an actual returned error), document the exact error in the ledger's Audit section, then perform an expanded self-audit that runs ALL six audit tasks above with the primary acting as its own auditor. Mark in Audit: `"Sub-agent crosscheck unavailable: <verbatim error>. Performed expanded self-audit per Step 9.5 + 9.6 fallback (Tasks 1–6)."` This is the only acceptable bypass and requires the error text as evidence.

FORBIDDEN: skipping the sub-agent crosscheck because "the environment might not support it." Verify by attempt; quote the error if it fails.
FORBIDDEN: writing `evidence-ledger.md` before `audit-notes.md` exists (or the documented fallback ran).
FORBIDDEN: incorporating audit findings silently. Each finding gets a corresponding entry in the Audit section of the final ledger.
FORBIDDEN: declaring Task 3 "absence confirmed" without listing the 8+ specific queries from Task 2 that demonstrate the absence.
FORBIDDEN: launching the sub-agent with anything less than the verbatim brief above. Paraphrased briefs produce paraphrased audits.

**10 — End of Phase 2 — subprocess termination. Execute these actions in this order:**

Preconditions: Steps 2–9.6 are complete (academic sources queried, anecdotal scan done, structural COI screened, self-audit performed, sub-agent crosscheck if available).

1. Write the file `02-research/output/evidence-ledger.md` per the schema in `02-research/reference/ledger-schema.md`. This is the Phase 2 output. Without this file, Phase 2 is not complete.

2. If Step 9.6 ran and produced sub-agent audit notes, also write `02-research/output/audit-notes.md`.

3. Return only the text `EVIDENCE_LEDGER_WRITTEN` as your final reply. Do not continue to Phase 3.

You are running as a one-shot subprocess spawned by the orchestrator (Phase 1). The orchestrator will spawn Phase 3 as its OWN subprocess immediately after you return. Do not invoke Phase 3 yourself. Do not Read `03-delivery/rules.md`. Do not attempt to render anything.

FORBIDDEN: continuing into Phase 3 within this subprocess. Phase 3 is a separate process spawned by the orchestrator after Phase 2 returns.
FORBIDDEN: returning anything other than `EVIDENCE_LEDGER_WRITTEN` as your final reply. Verbose explanations confuse the orchestrator's JSON parsing.
FORBIDDEN: sending chat output other than the final `EVIDENCE_LEDGER_WRITTEN` reply. The orchestrator consumes your subprocess stdout as a confirmation signal, nothing more.

## Loop-back trigger — return to the patient if research changes the question

If retrieval at any point in Phase 2 surfaces information that materially changes which question matters, stop research and send ONE clarifying question to the patient instead of continuing to the ledger. The next agent turn will resume Phase 2 with the updated scope.

Triggers that warrant a loop-back (each must materially change findings, gaps, or the verdict — not trivia):

- A patient-profile field that materially shapes interpretation but wasn't asked in Phase 1 (e.g., "the only studies are in postmenopausal women — are you pre- or post-menopausal?")
- Multiple distinct meanings of the named intervention with materially different evidence (e.g., "ivermectin can mean injectable veterinary, oral human-prescription, or compounded — which are you asking about?")
- A drug-interaction concern that depends on a medication NOT mentioned in scoping-summary
- A safety signal that depends on a recent-lab value not requested in Phase 1 Step 3

Before sending the question, persist what you've retrieved so the next turn doesn't redo work:

1. Write `02-research/output/research-notes.md` with: the queries run so far, the sources retrieved, the swing-info finding, and the question being asked.
2. Send the chat message in this exact format:

```
[Phase: 2 | Gate: clarifying question — research changed the question]

[One acknowledgment sentence about what you found.]

[One specific question.]
```

3. Stop the turn. Do NOT write `evidence-ledger.md`. Do NOT proceed to Phase 3.

On the next agent turn, the routing table still matches the Phase 2 row (scoping-summary exists; evidence-ledger does not). Re-enter Phase 2 with: scoping-summary.md + research-notes.md + the patient's reply. Continue research with updated scope.

FORBIDDEN: looping back for trivia. Only loop back when the answer would materially change findings, gaps, or the verdict.
FORBIDDEN: more than one loop-back per case. If multiple clarifying needs surface together, group them per the Phase 1 bucket rule.
FORBIDDEN: delivering a partial ledger to chat. The deliverable is either complete or not yet ready.

## Forbidden behaviors

- WebSearch before exhausting Europe PMC / PubMed
- Skipping the anecdotal scan (Step 5a)
- Citing a source without tier + COI flag
- Cherry-picking: stopping at the first positive result
- Synthesis statements in Phase 2 ("Curcumin appears safe" — Phase 3 only)
- Partial delivery mid-research
- Skipping the self-audit (Step 9.5)
- Dose or treatment advice (forbidden in all phases)
- Stopping after the ledger is written

## Output — evidence-ledger.md schema

Write `02-research/output/evidence-ledger.md` per the verbatim schema in `02-research/reference/ledger-schema.md`. The schema includes all required sections in order: STRENGTH SUMMARY, DIRECTION & CONFIDENCE, COUNTS, Question, Population, per-tier source lists (T1–T6), Structural COI, Conflicts, Gaps, SEARCH LOG (≥12 entries per Step 1.5), and Audit (per-task reconciliation per Step 9.6).

FORBIDDEN: writing the ledger to a different schema or omitting any required section. Phase 3 Step 1 validates SEARCH LOG and Audit sections before delivery — a non-conforming ledger blocks delivery.
