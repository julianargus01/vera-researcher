---
title: VERA — README
date: 2026-05-29
author: claude-code
project: vera-researcher
role: readme
---

# VERA — Verified Evidence Research Analyst

A research partner for cancer patients evaluating complementary and alternative therapies alongside conventional treatment.

VERA investigates. She doesn't summarize what's out there — she weighs it, flags conflicts of interest, names what's missing, and tells you exactly what to bring to your oncologist.

---

## Quick start

Load this folder into a fresh project — Claude Code, Cowork, or Codex - and say "Start" or "Begin".
VERA will greet you. Just ask your question.

---

## 90-second cold test

Open a new session. Tell VERA you're a Stage II breast cancer patient finishing AC chemotherapy and you want to know whether continuing daily cold plunges is safe once you start Taxol. Don't over-explain — give her the basics and let her ask what she needs. Watch how she scopes the question before synthesizing. That's the behavior that separates her from a search engine.

---

## What you get back

When VERA finishes, she delivers a graphic report — not a wall of text.

- **In chat:** a single link that reads "Click here for the full report." Clicking it opens the 6-page PDF. Page 1 IS the hero + the honest answer + the two-question dashboard — your at-a-glance view is the first page of the report.
- **The full report (`final-report.pdf`):** six pages. Pages 1–4 are written for you (the verdict, the findings, what we don't know, and questions to bring to your oncologist). Pages 5–6 are written for your oncologist (a dense one-page clinical summary plus a hyperlinked reference list).

Two questions sit at the heart of the dashboard: *Will it help?* and *Could it hurt?* Each gets 0–5 confidence dots and a plain-language label. Strong evidence against (5 dots + "No"), nothing to go on (0 dots + "We can't tell yet"), and everything in between read the same way at a glance.

Patient-facing pages are written at a 6th-grade reading level. Internal evidence tiers (T1 through T6) and conflict-of-interest flags drive the analysis but are translated into plain language for you — no jargon, no abbreviations.

## What VERA will not do

- Diagnose, recommend treatment, or advise on dose
- Tell you whether your situation is an emergency
- Produce a synthesis without sourced, cited evidence
- Change her findings because you push back

These are structural limits, not preferences. They exist to protect you.

---

## How it's built

VERA implements Interpretable Context Methodology (ICM) to canonical, with one architectural extension: **phase isolation via subprocess dispatch**. Each phase runs in its own context window to prevent the bloat that single-turn cascades produce.

- **`identity.md`** is the L1 router. It carries a `| Task | Go to | Read |` table. VERA reads it first every session and matches her current task to a row based on which `output/` files exist.
- **`01-scoping/`, `02-research/`, `03-delivery/`** are the three phase folders. Each holds a `rules.md` (Inputs / Process / Outputs contract), an `examples.md` (calibration tape), a `reference/` folder (voice rules plus any phase-scoped references), and an `output/` folder where the phase's artifact lands.
- **Phase 1 (intake) runs in the main agent session.** Multi-turn user dialogue happens here.
- **At end of Phase 1, the orchestrator spawns Phase 2 as a subprocess** via Bash + `claude -p` with `CASCADE CONTINUATION` prompt prefix. Fresh context. Phase 2 reads scoping-summary.md, executes research per its rules, writes `evidence-ledger.md`, returns.
- **Orchestrator then spawns Phase 3 as another subprocess** with fresh context. Phase 3 reads scoping-summary.md + evidence-ledger.md, renders the 6-page PDF, returns the chat message text.
- **Phase 2 cannot begin** until `01-scoping/output/scoping-summary.md` exists.
- **Phase 3 cannot begin** until `02-research/output/evidence-ledger.md` exists.
- **`02-research/reference/`** holds shared evidence files: `evidence-tiers.md` (the 6-tier CAM hierarchy), `coi-flags.md` (conflict-of-interest schema), `source-databases.md` (the 6-source fallback chain), `cam-categories.md` (CAM taxonomy), `audit-brief.md` (verbatim adversarial sub-agent prompt), `ledger-schema.md` (output schema).

The cascade is the file system + subprocess boundaries. The routing table is the only "logic"; subprocess spawning is the only "automation."

---

## File map

```
vera-researcher/
├── CLAUDE.md                                (3-line bootstrap — tells the agent "you are VERA; read identity.md")
├── identity.md                              (L1 router with the routing table)
├── README.md                                (this file)
├── WRITEUP.md                               (3-paragraph submission summary)
├── JUDGE_GUIDE.md                           (orientation for evaluators)
├── 01-scoping/
│   ├── rules.md                             (Pattern 1 contract: Inputs / Process / Outputs)
│   ├── examples.md                          (3 scoping dialogues)
│   ├── reference/voice.md                   (scoping voice rules)
│   └── output/                              (scoping-summary.md lands here)
├── 02-research/
│   ├── rules.md
│   ├── examples.md                          (3 evidence-ledger examples)
│   ├── reference/
│   │   ├── voice.md                         (research voice rules)
│   │   ├── evidence-tiers.md
│   │   ├── coi-flags.md
│   │   ├── source-databases.md
│   │   └── cam-categories.md
│   └── output/                              (evidence-ledger.md lands here)
└── 03-delivery/
    ├── rules.md
    ├── examples.md                          (3 final-report examples — one per canonical evidence shape)
    ├── reference/
    │   ├── voice.md                         (delivery voice rules)
    │   ├── template-keys.md                 (canonical placeholder list the renderer consumes)
    │   ├── render_deliverable.py            (Python renderer — reportlab + Pillow, environment-agnostic)
    │   └── samples/                         (v0 canonical samples — unknown / strong-against / mixed evidence shapes)
    └── output/                              (final-report.pdf lands here)
```

---

## Limitations

VERA is a research tool. She is not a substitute for medical advice, a second opinion from an oncologist, or a clinical decision-making system. Every finding she produces is a starting point for a conversation with your care team — not a conclusion that replaces it.

Evidence in complementary oncology is often limited, conflicting, or industry-funded. VERA names these limitations explicitly. An honest "the evidence is weak and here's why" is more useful to you than a confident summary of poorly designed trials.
