---
title: VERA COI Flags
project: vera-researcher
role: reference
---

# COI Flags

A conflict of interest exists when an author, sponsor, funder, or larger structural force has a financial, political, geographic, or ideological relationship that could bias study design, conduct, analysis, or reporting. Apply COI flags at every tier before citing a source. Beyond per-source COI, screen for **structural-COI patterns** that affect the entire evidence base.

---

## Per-source COI by tier

### Tier 1 — Systematic Reviews & Meta-Analyses
- Industry funding of constituent RCTs (captured via individual study disclosures)
- Review authors receiving honoraria, consulting fees, or grants from entities with financial interest in the outcome
- Protocol not pre-registered (allows post-hoc inclusion/exclusion to favor outcomes)

### Tier 2 — Individual RCTs
- Funding source from supplement or device manufacturer
- Author employment at or consulting for the manufacturer
- Practitioner-researcher studying their own product (common in CAM trials)
- No pre-registration on ClinicalTrials.gov or equivalent — enables endpoint switching

**Corporate capture pattern:** Supplement companies fund small positive trials, rarely replicate them, and use the single study in marketing. Industry-funded CAM trials consistently show positive-result bias vs. independently-funded trials.

### Tier 3 — Observational Studies
- Industry-funded data collection or database access
- Investigator with financial stake in the intervention
- National health body funding with policy mandate to promote the intervention

### Tier 4 — Case Reports / Case Series
- Report authored by the treating practitioner
- No independent outcome verification
- Selective reporting (practitioners report successes, not failures)

### Tier 5 — Grey Literature
- Conference abstracts funded by industry (only positive results typically submitted)
- Guidelines from government ministries with mandate to promote the intervention

### Tier 6 — Anecdotal
- Testimonials on company-owned platforms
- Practitioner reports where the practitioner sells the intervention
- Podcast / social media content from individuals with affiliate relationships, paid sponsorships, or supplement-line businesses
- Reddit/forum accounts associated with practitioners or sellers (verify before citing)

---

## Structural COI — screen the whole evidence base, not just individual sources

These patterns affect what evidence EXISTS and what evidence APPEARS in the literature. They cannot be detected by per-source COI flags alone. Screen for all five before finalizing the ledger.

### 1. Corporate research-agenda capture
Pharma and supplement industries shape WHAT gets studied at all, not just how individual studies are funded. Topics with no commercial incentive — off-label use of cheap generics, lifestyle interventions, non-patentable compounds, behavioral changes — are systematically under-studied. Absence of evidence in these areas is often a structural artifact, not a true absence of effect.

**Flag when:** Evidence is sparse for a non-patentable or low-margin intervention.
**Ledger note format:** "Research-agenda gap — [intervention] is [non-patentable / low-margin / behavioral], which limits commercial sponsorship and constrains evidence supply. Absence of trials should not be read as absence of effect."

### 2. Political / regulatory capture
Funding agencies and regulators face political pressure that affects which topics get funded and which findings get amplified or buried.
- NIH funding cycles favoring certain disease areas based on advocacy intensity
- FDA pressure cycles around contentious approvals (e.g., supplements with strong industry lobbying)
- State-level public health priorities affecting research mandates

**Flag when:** Conclusions align suspiciously with current funding-body political priorities OR contentious findings appear suppressed (registered trials with no published results, retractions).
**Ledger note format:** "Political/regulatory note — [observation about funding pattern or finding suppression]."

### 3. Geographic capture
State-funded research promoting traditional medicine as national policy carries systematic bias analogous to industry funding:
- **China:** government-funded TCM research, strong publication pressure toward positive results
- **India:** AYUSH ministry promotes Ayurvedic and homeopathic treatments
- **Russia, Iran, Cuba:** similar patterns for state-promoted traditional approaches
- **Germany:** historically lighter regulation of Anthroposophic medicine

**Flag when:** Funder is a government body with a policy mandate to promote the intervention under study.
**Ledger note format:** "Geographic capture — [N studies] in this evidence base come from [country/agency] with a policy mandate to promote [intervention]."

### 4. Ideological capture
Research funded or promoted by movements with a worldview commitment to the intervention, independent of evidence:
- **Anthroposophy** (Steiner-influenced) funding mistletoe research
- **Naturopathy / integrative medicine** movements promoting specific supplements
- **Anti-cancer-industry** advocacy promoting alternatives (apricot kernels, baking soda, fenbendazole, etc.)
- **Religious / spiritual** movements promoting fasting, prayer, or specific dietary practices as cancer treatments

**Flag when:** Source is affiliated with a movement that has an ideological commitment to the intervention preceding any evidence.
**Ledger note format:** "Ideological capture — most [positive / negative] sources are affiliated with [movement], whose commitment to [intervention] predates the data."

### 5. Publication bias
Positive results are more likely published than negative or null results. In CAM meta-analyses, this means pooled estimates often overstate efficacy.
- Cochrane reviews counter this by searching trial registries for registered-but-unpublished studies — a key reason Tier 1 carries more weight than pooled non-Cochrane meta-analyses.
- **ClinicalTrials.gov check:** search for "completed, no results posted" — these are publication-bias signals.

**Flag when:** Pooled estimates show effect AND trial registries reveal unpublished studies on the same intervention.
**Ledger note format:** "Publication bias — ClinicalTrials.gov shows [N] completed trials with no results posted on [intervention]; pooled estimates may overstate effect."

---

## How structural COI flows downstream

Per-source COI goes inline next to citations (`[COI: yes — manufacturer-funded]`). Structural COI goes in a separate `Structural COI considerations:` section at the end of the ledger. Phase 3 delivery surfaces structural COI in plain language in the patient section, not only in the oncologist handoff — because patients deserve to know when a whole evidence base is shaped by movement-loyalty or research-supply limits.
