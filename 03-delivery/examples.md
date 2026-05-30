# 03-delivery/examples.md — Phase 3 calibration tape

Three locked v0 samples anchor the dashboard's three possible shapes. The renderer + data-dict pipeline produces all three from the same template — only the populated data changes.

Each example references its full sample deliverable in `reference/samples/` (HTML + PDF). Open the PDFs to see what "correct" looks like for that shape.

---

## Example D1 — Unknown-evidence shape (fasting + Stage III NHL)

**Reference:** `reference/samples/sample-unknown-evidence.{html,pdf}`

*Demonstrates: no studies in patient's cancer; verdict explains the absence of evidence rather than calling it "weak"; HELP dots = 0/5 with label "We can't tell yet"; HURT dots = 2/5 with label "Maybe — some concern"; "What we found" surfaces zero trials in lymphoma as the biggest gap; anecdotal callout names podcasts + subreddits + traces claims to source; gaps tied to patient's R-CHOP + possible CAR-T context; questions opener uses "still thinking about trying" framing.*

**Data dict shape (excerpt):**
```python
{
  "TITLE": "Fasting during R-CHOP for Stage III non-Hodgkin lymphoma",
  "VERDICT_PARAGRAPH": "No one has tested fasting in people with your kind of cancer yet. The few small studies that exist are in other cancers (mostly breast), and they had mixed results — so we can't just take those findings and apply them to lymphoma. That means there's no direct evidence telling us whether fasting will help or hurt in your case. What we do know: R-CHOP makes it harder to keep weight up and eat enough protein, which your body needs to handle treatment. So the safety side matters more than the buzz online.",
  "HELP_DOTS_FILLED": 0, "HELP_LABEL": "We can't tell yet",
  "HELP_EXPLAIN": "No studies have tested fasting in people with lymphoma. The few trials in other cancers had mixed results.",
  "HURT_DOTS_FILLED": 2, "HURT_LABEL": "Maybe — some concern",
  "HURT_EXPLAIN": "Doctors recommend eating enough during chemo. Fasting could be risky if you lose weight or run low on protein.",
  "COUNTS": [
    {"n": 2, "label": "High-quality reviews (not in lymphoma)"},
    {"n": 1, "label": "Clinical trial (in breast cancer)"},
    {"n": 0, "label": "Trials in lymphoma", "tag": "biggest gap"},
    {"n": 4, "label": "Smaller studies and case reports"},
    {"n": 6, "label": "Online claims we checked"}
  ],
  # ... see sample-unknown-evidence.html for full dataset
}
```

This is the most common shape (CAM literature is dominated by under-studied questions).

---

## Example D2 — Strong-evidence-against shape (apricot kernels + Stage II breast cancer)

**Reference:** `reference/samples/sample-strong-against.{html,pdf}`

*Demonstrates: solid evidence base showing harm; HELP dots = 5/5 with label "No"; HURT dots = 4/5 with label "Yes"; verdict acknowledges the patient + names ideological capture explicitly; findings cite real RCT + Cochrane review + FDA action + case reports; anecdotal callout names "World Without Cancer" + Mexican clinics + suppression conspiracy and addresses each; questions opener uses "weighing this against your doctor's view" framing; clinical summary surfaces structural-COI (ideological capture across 60+ years) as the dominant feature.*

This is the rarer shape — most CAM questions don't have decades of clear negative evidence. When they do (laetrile, MMS, etc.), this is how the dashboard renders that clarity.

---

## Example D3 — Mixed-evidence shape (IV vitamin C + Stage IV pancreatic)

**Reference:** `reference/samples/sample-mixed-evidence.{html,pdf}`

*Demonstrates: small evidence base with mixed signals + one real safety risk; HELP dots = 2/5 with label "Maybe"; HURT dots = 3/5 with label "Yes — one real risk" (G6PD deficiency); verdict explicitly frames this as "maybe, with eyes open" rather than a clear yes or no; findings cite real published trials with patient-relevant caveats (different chemo regimen, no control arm); anecdotal callout names Joe Rogan + Riordan Clinic + alternative-cancer subreddits; structural-COI = research-agenda capture (non-patentable); questions tie back to G6PD screening + regimen-specific gap.*

This is the most demanding shape because it asks the patient to hold mixed information without collapsing it into a binary. The two-question dashboard is what makes this shape readable.

---

## How to use these examples

When generating a new deliverable:
1. Read the patient's scoping-summary + evidence-ledger
2. Identify which of the three shapes the evidence most resembles (unknown / strong-against / mixed)
3. Open the matching sample HTML/PDF and study how that shape was rendered
4. Populate the data dict to match the structural pattern of the matching sample
5. Call `render_deliverable.render(data, output_dir)`
6. Confirm the rendered PDF visually matches the sample shape before delivering to chat

The samples are calibration tape — they show what "right" looks like for each shape. The renderer is the production tool that turns a populated dict into the same shape.
