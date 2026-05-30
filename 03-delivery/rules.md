---
title: VERA — Phase 3 Delivery Rules
date: 2026-05-29
author: claude-code
project: vera-researcher
role: phase-rules
phase: 03-delivery
deliverable_version: v0
---

**State preamble required on every response (REQUIRED — not optional):**
`[Phase: 3 | Gate: <which deliverable artifact is being produced or "final-report.pdf not yet written">]`

FORBIDDEN: dropping the state preamble.

## Inputs

| File | Why |
|------|-----|
| `01-scoping/output/scoping-summary.md` | Patient context, target outcome, conditional fields, Research question |
| `02-research/output/evidence-ledger.md` | Fixed evidence base — STRENGTH SUMMARY (direction ratings), T6 anecdotal claims, structural-COI explanations, source URLs, Audit notes |
| `02-research/output/audit-notes.md` | Full (if file exists) — sub-agent crosscheck output |
| `examples.md` | Phase 3 calibration tape — three canonical shapes (unknown / strong-against / mixed) |
| `reference/voice.md` | Voice rules (6th-grade, warmth woven, dot semantic, lack-of-evidence framing, banned phrasings) |
| `reference/samples/` | Three locked v0 sample deliverables — visual + structural ground truth |
| `reference/template-keys.md` | Canonical placeholder list — every `{{KEY}}` Phase 3 must populate |
| `reference/render_deliverable.py` | Pure-Python deliverable renderer (reportlab; no Chrome, no system libs) |

No other `reference/` files beyond voice.md, samples/, template-keys.md, and render_deliverable.py. Delivery does not re-research.

## Process

**1. Confirm gate and clear prior-case output.**

Stop if `02-research/output/evidence-ledger.md` does not exist. Do not begin delivery.

**Verify Phase 2 enforcement sections in the ledger.** Before rendering, the ledger must contain both:

1. A `SEARCH LOG` section with ≥12 entries (Phase 2 Step 1.5 requirement). Each entry must show `action`, `source`, `query`, `result`.
2. An `Audit` section with per-task reconciliation `TASK 1` through `TASK 6` from the adversarial sub-agent crosscheck (Phase 2 Step 9.6) — OR a documented fallback statement quoting the sub-agent's verbatim launch error.

If either section is missing, empty, or appears templated/unfilled (e.g., placeholder `<...>` brackets still present, "TBD", or zero log entries), do NOT proceed to delivery. The ledger bypassed Phase 2 enforcement and is not a safe basis for a patient-facing report. Re-enter Phase 2 (read `02-research/rules.md`) and complete the missing enforcement steps before returning to Phase 3.

If `03-delivery/output/final-report.pdf` exists from a prior case, archive it before rendering. Also clean up any legacy `page-1.png` from pre-X-pivot runs (the renderer no longer emits one as of 2026-05-30):

1. Create `03-delivery/output/_archive/<YYYYMMDD-HHMM>/` (timestamp at delivery).
2. Move `final-report.pdf` (if present) into that folder.
3. Move any legacy `page-1.png` (if present) into the same folder.

This clears the path for the new render. The prior case's deliverable is preserved as history, not destroyed.

FORBIDDEN: proceeding to delivery when the ledger lacks SEARCH LOG or per-task Audit reconciliation. Phase 2 enforcement is the only check between shallow research and a confident-sounding patient deliverable; bypassing that check via Phase 3 makes the architecture cosmetic.
FORBIDDEN: bailing out of Phase 3 because a prior case's `final-report.pdf` exists. Archive it and continue. A new case has its own deliverable.

**2. Populate the data dict.**
[Gate: data dict not yet populated]

Read `reference/template-keys.md` for the required key list. From scoping-summary + evidence-ledger, populate every key. Specifically:

- `TITLE` — one-line case title naming the intervention + cancer + treatment
- `PATIENT_META` — single-line summary from scoping (age/sex · cancer/stage · treatment · meds · weight/appetite if relevant)
- `VERDICT_PARAGRAPH` — 4–6 sentence honest answer at 6th-grade reading level. When evidence is absent, explain the absence rather than calling it "weak." Never lead with a single-word rating.
- `HELP_DOTS_FILLED` (int 0–5) and `HURT_DOTS_FILLED` (int 0–5) — dots represent **confidence in the answer**, not strength of evidence in favor. Direction lives in `HELP_LABEL` / `HURT_LABEL` words ("Yes", "Probably yes", "Maybe", "Probably not", "No", "We can't tell yet"). Strong evidence against = high dots + "No" / "Probably not".
- `HELP_EXPLAIN` / `HURT_EXPLAIN` — one plain-language sentence each
- `COUNTS` — patient-facing count list grouped by plain-language descriptions (NOT tiers). At least one item may carry a `tag` ("biggest gap", "safety") highlighting the most relevant signal.
- `FINDINGS` — 3–5 findings at 6th-grade reading level; `url` (when source URL exists) is wrapped around the bolded study name; `coi` only present when a real conflict exists and is written as a full plain-language sentence (never abbreviated "COI:")
- `ANEC_PARAGRAPHS` — 1–3 paragraphs naming platforms specifically, tracing claims to source, explaining structural-COI in plain language
- `GAPS` — 3–5 gaps with bold headline + 1–2 plain-language sentences tied to the patient's specific situation
- `QUESTIONS_LEDE` — conditional opener: *"If you're still thinking about trying [X]…"* when verdict is maybe/unknown; *"If you're weighing this against your doctor's view…"* when verdict is strong-against
- `QUESTIONS` — 3–5 actionable questions tied to patient's specific situation; each with one italic "why" line
- `CLINICAL_KV` and `CLINICAL_BLOCKS` — oncologist-facing; technical register OK; tier codes still forbidden (use "phase II RCT" not "T2"); funding written in full ("independent funding" not "no COI"). **Length cap: 4 CLINICAL_BLOCKS items max, body text ≤ 400 chars each (≤ 1,600 chars combined). CLINICAL_KV ≤ 8 rows.** Dense oncologist summaries that exceed these caps overflow page 5 and push the reference list to page 7, breaking the locked 6-page spec. Compress: pick the strongest single line per concept; oncologists scan, not read.
- `REFERENCES` — every reference has a URL; preference order PubMed > journal open-access > ClinicalTrials.gov > government PDQ > Cochrane Library; anecdotal sources are NOT in references

See `reference/template-keys.md` for the full key list with types and source-phase mapping.

**3. Render the deliverable.**
[Gate: render not yet complete]

Call the renderer with the populated dict and the output directory:

```python
from render_deliverable import render
paths = render(data_dict, "03-delivery/output/")
# paths = {"pdf": "03-delivery/output/final-report.pdf"}
```

The renderer produces a single artifact:
- `final-report.pdf` — 6-page deliverable (page 1 = hero + verdict + dashboard; page 2 = findings; page 3 = gaps; page 4 = questions; page 5 = clinical summary; page 6 = references). Page 1 is the patient's at-a-glance view; the user sees it on click.

If your environment cannot execute Python (e.g., a Claude.ai Project session with no shell), fall back to populating the data dict in markdown form, attaching the markdown, and instructing the recipient to run the renderer in a Python-capable environment.

**4. Deliver — return chat message text as subprocess stdout.**
[Gate: chat message not yet returned]

You are running as a one-shot Phase 3 subprocess spawned by the orchestrator. The "chat message" below is what you RETURN as your final reply — the orchestrator consumes your subprocess stdout (the JSON `result` field) and re-emits this text verbatim to the patient. There is no separate "chat send" step from inside this subprocess; the orchestrator handles delivery.

Your final reply must be exactly two lines, in this order, with nothing else before, between, or after:

```
Here's what I found about [intervention] for your situation.

[Click here for the full report](<URL-ENCODED-ABSOLUTE-PATH-TO-PDF>)
```

The dashboard is page 1 of the linked PDF — the patient sees it the moment they open the link. There is no separate page-1 image artifact (architecturally retired 2026-05-30 after empirical testing in Claude Code; see "Why" below).

**Path format — REQUIRED.** Take the absolute path returned by `render()["pdf"]` and URL-encode every literal space (replace each ` ` with `%20`). All other path characters pass through unchanged. The encoding step is mandatory — raw absolute paths with spaces do not resolve.

Concrete example:
- `render()["pdf"]` returns: `/Users/gregfaysash/Library/CloudStorage/GoogleDrive-julianargus01@gmail.com/Other computers/My Mac/Main/workspaces/vera-researcher/03-delivery/output/final-report.pdf`
- Encoded for the link: `/Users/gregfaysash/Library/CloudStorage/GoogleDrive-julianargus01@gmail.com/Other%20computers/My%20Mac/Main/workspaces/vera-researcher/03-delivery/output/final-report.pdf`

**Why URL-encoded absolute paths and single PDF (empirical, 2026-05-30).** Direct testing in Claude Code:
- URL-encoded absolute-path link `[text](path%20with%20encodings)` → ✅ opens the file
- Raw absolute path (spaces unescaped) → ❌ link cuts off at first space, does not resolve
- Relative paths (either form) → ❌ outside session folder, does not resolve
- Image embed syntax `![alt](path)` (any encoding) → ❌ never renders as an image in Claude Code; the previous PNG-inline design depended on a chat-platform behavior that does not hold

That is the entire chat message. No signoff, no summary of findings, no "I hope this helps," no explanation of the dashboard, no rendering of the data dict, no description of which Python call you made, no separate page-1 surfacing via Read tool. The user sees the dashboard by clicking the link.

FORBIDDEN: writing `Click here for the full report` as plain text without the markdown link syntax `[text](path)`. A description is not a link.
FORBIDDEN: PDF link with unencoded spaces. Spaces in the path MUST be `%20` in the link URL — every space, no exceptions.
FORBIDDEN: relative file paths in chat markdown. Use the absolute path returned by `render()["pdf"]`, URL-encoded.
FORBIDDEN: surfacing a separate page-1 artifact (via Read tool on a PNG, markdown image embed, or any other mechanism). The X-pivot retired that path; page 1 of the linked PDF IS the dashboard.
FORBIDDEN: rendering the patient section as conversational chat prose with inline citations. The deliverable IS the linked PDF — the chat text is the acknowledgment + link wrapper, nothing else.
FORBIDDEN: visible JSON, Python code, data-dict contents, `render(...)` call invocations, or any internal-process narration in the chat message.

**4.5. Archive intermediates after delivery.**
[Gate: chat message text returned as subprocess final reply; intermediates still in `output/` folders]

Move the Phase 1 and Phase 2 artifacts out of their `output/` folders so they stop surfacing as separate file chips in chat UI and so the next session sees a clean state for the routing table:

1. Create `01-scoping/output/_archive/<YYYYMMDD-HHMM>/` (timestamp at delivery).
2. Move `01-scoping/output/scoping-summary.md` into that folder.
3. Create `02-research/output/_archive/<YYYYMMDD-HHMM>/` (same timestamp).
4. Move `02-research/output/evidence-ledger.md` (and `audit-notes.md` if present) into that folder.
5. Leave `03-delivery/output/final-report.pdf` in place — that IS the deliverable; the user needs to click it from the chat link.

If the environment lacks file-move capability, skip this step silently. The user-message routing row in `identity.md` already protects new cold-start sessions from stale state — archiving is belt-and-suspenders + chat-UI cleanup.

FORBIDDEN: deleting intermediates. Archive, do not destroy — they're case history. If the patient asks a follow-up, the archived files can be re-loaded.

**5. Stop conditions.**
- PDF written, chat message returned as final reply (subprocess stdout) → done. The orchestrator consumes the return text and re-emits it to the patient.
- If patient asks a follow-up: complete the deliverable first, then address the follow-up using the already-saved evidence-ledger as the source of truth.
- If patient pushes back on the verdict: state which evidence the verdict rests on (cite the finding). Do not revise without new evidence.
- If patient requests dose or treatment advice: decline. Redirect to the oncologist handoff section of the PDF.

**Delivery failure modes (named — do not commit these):**
- Skipping the renderer and writing markdown to chat instead
- Writing a single-word rating ("Weak", "Strong") as the lead of VERDICT_PARAGRAPH instead of an explanation of the evidence picture
- Filling more dots when evidence is sparse to imply confidence we don't have
- Using tier codes (T1–T6) anywhere in the rendered PDF
- Abbreviating "COI" — always "Conflict of interest:" with plain-language explanation of how it might affect the finding
- Hyperlinking anecdotal sources (Reddit, podcasts) — directing patients to viral CAM content amplifies it
- Writing the patient section in chat prose instead of delivering the URL-encoded PDF link
- Surfacing a separate page-1 artifact (Read tool on PNG, image embed, etc.) — page 1 of the linked PDF IS the dashboard
- Generating a PDF that omits any of the 6 required sections

## Output

The deliverable is a single file written to `03-delivery/output/`:

| File | Audience | Used by |
|------|----------|---------|
| `final-report.pdf` | Patient (pages 1–4) + oncologist (pages 5–6 clinical appendix) | Patient opens via the URL-encoded chat link; brings to oncology team |

The file is generated by a single call to `render_deliverable.render(data, output_dir)`, which returns `{"pdf": absolute_path}`. The renderer is the only mechanism that writes the deliverable.

Report is complete when `final-report.pdf` exists and the chat message text has been returned as the subprocess's final reply (containing the URL-encoded link). The orchestrator (Phase 1 main session) consumes this stdout and emits it to the patient. No trailing summary, no VERA sign-off paragraph.
