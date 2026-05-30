---
title: VERA Source Databases
project: vera-researcher
role: reference
---

# Source Databases

Two tracks: the **academic track** (Sources 1–6) for tier-rated evidence, and the **anecdotal/community track** (Source 7) for understanding what claims patients are encountering about an intervention. Both are queried in every research session; they serve different purposes. The academic track produces evidence to weight; the anecdotal track produces claims to address.

---

## Academic track (Sources 1–6) — for tier-rated evidence

Work down in order. A failed source does not terminate the session — note the failure and continue.

### 1. Europe PMC (Primary)
**URL:** `https://www.ebi.ac.uk/europepmc/webservices/rest/search`
**Covers:** 40M+ biomedical records including MEDLINE, PubMed Central, and European sources (EMBL, WHO, UKRI). Returns abstracts inline. Best CAM indexing of any free source.
**Use:** All queries. Primary source for evidence retrieval.
**Fallback trigger:** HTTP error; empty result list; timeout >10s.

### 2. PubMed E-utilities (Fallback)
**Endpoints:** `esearch.fcgi` (returns PMIDs) → `efetch.fcgi` (returns abstract text)
**Covers:** MEDLINE + PubMed Central. NIH-maintained. Authoritative for US biomedical literature.
**Use:** When Europe PMC fails or returns sparse results.
**Fallback trigger:** HTTP error; empty `idlist`; rate limit (HTTP 429).

### 3. ClinicalTrials.gov v2 API
**URL:** `https://clinicaltrials.gov/api/v2/studies`
**Covers:** Registry of clinical studies worldwide. Trial status, endpoints, sponsor, results when submitted. Identifies registered-but-unpublished trials (publication-bias signal).
**Use:** Any query involving trial status, pipeline, dosing, efficacy, or pre-registration verification. Run in parallel with Sources 1–2 when query involves trial / treatment / dose / efficacy terms.
**Fallback trigger:** HTTP error; zero studies returned.

### 4. Semantic Scholar (DOI Lookup Only)
**Endpoint:** `/graph/v1/paper/DOI:{doi}`
**Covers:** 214M papers across all fields.
**Use:** Only when a specific DOI is known from Sources 1–2 and the abstract was missing.

### 5. Unpaywall
**URL:** `https://api.unpaywall.org/v2/{doi}`
**Covers:** Open-access full-text versions of paywalled papers.
**Use:** When a citation is identified but full text is needed and paywalled. Query by DOI.

### 6. WebSearch (Academic discovery fallback)
**Use:** When Sources 1–5 fail or a paper cannot be located by DOI. Query format: `[intervention] [condition] systematic review RCT site:pubmed.ncbi.nlm.nih.gov` or `[Author] [Year] [Journal]` for known papers.
**Note:** WebSearch is acceptable for discovery. The citation itself must point to the primary source (PMC, PubMed, journal) — not the search result page.

---

## Anecdotal/community track (Source 7) — for patient-encountered claims

This is **not a fallback** to the academic chain. It runs alongside it because patients arrive carrying claims from these spaces, and VERA's job includes addressing those claims directly. Tag everything found here as T5 or T6 per `evidence-tiers.md` — never weight as evidence for synthesis. The purpose is to KNOW what claims the patient is hearing, who's making them, and whether they should be addressed in the final report.

### 7. Anecdotal / community scan

Run this scan once per session, after the academic track is complete. Capture claim patterns, prevalence, and any commercial/affiliate COI flags.

**Reddit (primary anecdotal source):**
- Search via WebSearch with `site:reddit.com [intervention] [cancer type]` and `site:reddit.com [intervention] cancer experience`
- Target subreddits: `r/cancer`, `r/breastcancer`, `r/lymphoma`, `r/ovariancancer`, `r/PancreaticCancer`, `r/lungcancer`, `r/coloncancer`, `r/[intervention-specific]` (e.g., `r/Fasting`, `r/keto`), `r/IntegrativeOncology`, `r/AskDocs`
- Collect: dominant claim patterns ("what people say it does"), reported side effects, recurring success/failure stories, recurring patient questions, link/citation patterns (if Redditors repeatedly cite the same paper or podcast, note it)

**Podcast transcripts:**
- Search via WebSearch with `[intervention] [cancer type] podcast transcript` and `[intervention] cancer episode`
- Notable spaces: integrative-oncology podcasts, naturopathic-medicine podcasts, "wellness" podcasts that cover cancer (Joe Rogan, Huberman, Tim Ferriss, Peter Attia have all done relevant episodes), specific-disease podcasts (e.g., "Mama Doctor Jones" for women's health)
- Collect: claims made, named experts cited, named studies referenced (cross-check against academic track — sometimes podcast experts cite real but cherry-picked studies, sometimes they cite nothing)

**Patient forums:**
- Inspire (`inspire.com/groups/...`)
- CancerCare community (`cancercare.org/community`)
- Disease-specific: `breastcancer.org/community`, `lung.org/forums`, similar for other cancer types
- Search via WebSearch with `site:inspire.com [intervention] [cancer type]`
- Collect: similar to Reddit — claim patterns and any moderators/repeat posters who may have commercial COI

**Social media trends:**
- TikTok and YouTube comment-section patterns: search WebSearch for `[intervention] [cancer] tiktok` and `[intervention] [cancer] youtube reviews`
- Identify viral claims (multiple high-view videos saying the same thing), frequency, and the named people pushing them
- Note when a wellness influencer with no medical credentials is driving the conversation

**What to record per source in the ledger T6 section:**
```
- Source: [Reddit r/breastcancer] — T6 — [COI: see ledger structural-COI] — [prevalence: rare/common/viral] — [claim being made: "X helped my chemo fatigue"; ~20 mentions in past 12 months; one repeat poster sells coaching]
```

---

## When to use the anecdotal track

**Always.** Step 5a of `02-research/rules.md` requires the anecdotal scan for every session. The output may be sparse for obscure interventions or rich for trending ones, but the scan happens. Patient sessions where VERA didn't check the conversation the patient is bringing in produce final reports that fail to address it — and a final report that ignores what the patient has read is a final report the patient cannot use.

---

## Do Not Use

- **Google Scholar** — bot-blocked; no programmatic access
- **OpenGrey** — shut down 2021
- **Cochrane Library API** — no public API; cite abstracts only via web
- **Pirated full-text repositories** — never; if Unpaywall fails, cite the abstract only
