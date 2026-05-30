#!/usr/bin/env python3
"""Stop-hook safety net for VERA's Phase 1 → Phase 2 → Phase 3 cascade.

Triggered on every agent stop. Inspects workspace file state and decides whether
the agent stopped mid-cascade — which empirical testing has shown happens with
Haiku at the Phase 1 → Phase 2 boundary because the transition phrase
("Give me a few minutes…") is a strong turn-end pattern in the model's prior,
overriding the rules.md instruction to invoke the Bash tool next.

Behavior:
  • mid-intake (no scoping-summary.md yet)       → let stop proceed (normal)
  • Phase 1 done, Phase 2 not started            → BLOCK stop, inject Step 5 action 3 prompt
  • Phase 2 done, Phase 3 not started or stale   → BLOCK stop, inject Step 5 action 4 prompt
  • full cascade complete (intermediates archived, fresh PDF)  → let stop proceed
  • anything else                                → let stop proceed

The injected `additionalContext` is read by the orchestrator agent and re-enters
its turn so it can execute the missing Bash invocation.
"""

import json
import os
import sys
from pathlib import Path

# Hook script lives at <workspace>/.claude/hooks/cascade-watch.py
# Walk up to workspace root.
WORKSPACE = Path(__file__).resolve().parent.parent.parent

SCOPING = WORKSPACE / "01-scoping" / "output" / "scoping-summary.md"
LEDGER  = WORKSPACE / "02-research" / "output" / "evidence-ledger.md"
REPORT  = WORKSPACE / "03-delivery" / "output" / "final-report.pdf"


def _proceed():
    """Allow the stop to proceed normally."""
    sys.exit(0)


def _block(reason, additional_context):
    """Block the stop and inject context so the agent continues its turn."""
    payload = {
        "decision": "block",
        "reason": reason,
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": additional_context,
        },
    }
    print(json.dumps(payload))
    sys.exit(0)


def main():
    # Read hook stdin (best-effort). If unparseable, never block.
    try:
        _ = json.load(sys.stdin)
    except Exception:
        _proceed()

    scoping_exists = SCOPING.exists()
    ledger_exists  = LEDGER.exists()
    report_exists  = REPORT.exists()

    # Case 1: mid-intake. No scoping summary yet. Normal stop between intake turns.
    if not scoping_exists:
        _proceed()

    # Case 2: Phase 1 done, Phase 2 not started. Step 5 action 3 missing.
    if scoping_exists and not ledger_exists:
        msg = (
            "CASCADE INCOMPLETE — Step 5 action 3 not executed.\n\n"
            "You wrote 01-scoping/output/scoping-summary.md and sent the transition "
            "phrase, but you did NOT invoke the Bash tool to spawn the Phase 2 "
            "subprocess. Per 01-scoping/rules.md Step 5 action 3, invoke the Bash "
            "tool NOW with this exact command (Bash timeout=600000):\n\n"
            "claude -p --model haiku --permission-mode bypassPermissions "
            "--output-format json \"CASCADE CONTINUATION — Phase 2 invocation per "
            "routing table. Scoping summary exists at 01-scoping/output/scoping-summary.md. "
            "Execute Phase 2 per 02-research/rules.md. Stop after writing "
            "02-research/output/evidence-ledger.md. Return only EVIDENCE_LEDGER_WRITTEN "
            "as your final reply.\"\n\n"
            "After the Bash call returns, continue with action 4 (Phase 3 subprocess) "
            "and action 5 (emit Phase 3's chat message) per the same Step 5 sequence."
        )
        _block("Phase 1 finished but Phase 2 subprocess not yet spawned.", msg)

    # Case 3: Phase 2 done but Phase 3 deliverable not produced (or stale from prior case).
    if ledger_exists:
        if not report_exists or REPORT.stat().st_mtime < LEDGER.stat().st_mtime:
            msg = (
                "CASCADE INCOMPLETE — Step 5 action 4 not executed.\n\n"
                "02-research/output/evidence-ledger.md exists but a fresh "
                "03-delivery/output/final-report.pdf has not yet been written. "
                "Per 01-scoping/rules.md Step 5 action 4, invoke the Bash tool NOW "
                "with this exact command (Bash timeout=600000):\n\n"
                "claude -p --model haiku --permission-mode bypassPermissions "
                "--output-format json \"CASCADE CONTINUATION — Phase 3 invocation "
                "per routing table. Phase 1 and Phase 2 outputs exist. Execute "
                "Phase 3 per 03-delivery/rules.md. Return EXACTLY the chat message "
                "text (warm acknowledgment + URL-encoded PDF link) as your final reply.\"\n\n"
                "After the Bash call returns, emit Phase 3's `result` text as your "
                "final reply to the patient (Step 5 action 5)."
            )
            _block("Phase 2 ledger written but Phase 3 deliverable not yet rendered.", msg)

    # All other cases: cascade is complete or not yet started. Allow stop.
    _proceed()


if __name__ == "__main__":
    main()
