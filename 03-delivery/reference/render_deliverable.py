"""
VERA — Deliverable Renderer
===========================

Generates `final-report.pdf` (6 pages) from a populated data dict. Page 1 is the
hero + verdict + two-question dashboard; pages 2–4 are patient-facing findings, gaps,
and questions; pages 5–6 are the oncologist clinical summary + references.

Pure-Python; no Chrome, no system libraries. Uses `reportlab` only (`pip install reportlab`).

Brand tokens (v0, locked 2026-05-29):
    cream      #faf7f4   background (screen only; PDF uses white)
    coral      #c4614a   primary accent (bars, tags, links, callouts)
    coral-light#f9ece8   secondary surfaces
    teal       #3d7a73   secondary accent (finding dots, clinical-block borders)
    warm-gray  #6b5e54   muted text
    dark       #2d2520   headings, primary text
    Lora       headings (serif)
    DM Sans    body (sans)

Fonts: if `DMSans-Regular.ttf` and `Lora-Regular.ttf` are present in `./fonts/`, they're loaded.
Otherwise the renderer falls back to Helvetica + Times-Roman. The fallback is visually less
brand-matched but functionally correct.

Public API:
    render(data: dict, out_dir: str) -> dict[str, str]
        Returns {"pdf": path_to_pdf}

Data dict shape: see `template-keys.md` (D18 + this file's `validate_data()` for required keys).
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Any
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, ListFlowable, ListItem, Flowable
)

# ---------- Brand tokens ----------

CREAM       = colors.HexColor("#faf7f4")
WARM_WHITE  = colors.HexColor("#f5f0eb")
CORAL       = colors.HexColor("#c4614a")
CORAL_LIGHT = colors.HexColor("#f9ece8")
TEAL        = colors.HexColor("#3d7a73")
TEAL_LIGHT  = colors.HexColor("#e8f3f2")
WARM_GRAY   = colors.HexColor("#6b5e54")
WARM_GRAY_L = colors.HexColor("#9e8f86")
DARK        = colors.HexColor("#2d2520")
TEXT        = colors.HexColor("#3c322d")

REQUIRED_KEYS = {
    "TITLE", "PATIENT_META", "REPORT_DATE", "VERDICT_PARAGRAPH",
    "HELP_DOTS_FILLED", "HELP_LABEL", "HELP_EXPLAIN",
    "HURT_DOTS_FILLED", "HURT_LABEL", "HURT_EXPLAIN",
    "COUNTS", "FINDINGS", "ANEC_PARAGRAPHS", "GAPS",
    "QUESTIONS_LEDE", "QUESTIONS",
    "CLINICAL_KV", "CLINICAL_BLOCKS", "REFERENCES",
}


def validate_data(data: dict) -> None:
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise ValueError(f"Missing required keys: {sorted(missing)}. See template-keys.md.")
    if not 0 <= data["HELP_DOTS_FILLED"] <= 5:
        raise ValueError("HELP_DOTS_FILLED must be int 0–5.")
    if not 0 <= data["HURT_DOTS_FILLED"] <= 5:
        raise ValueError("HURT_DOTS_FILLED must be int 0–5.")


# ---------- Font loading ----------

def _load_fonts() -> tuple[str, str, str, str]:
    """Returns (sans, sans_bold, serif, serif_bold). Falls back to Helvetica/Times built-ins.

    Also registers font families so <b> tags in Paragraph markup route to the
    correct Bold TTF (Lora-Bold / DMSans-Bold) instead of synthesizing or falling back.
    """
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    sans, sans_bold = "Helvetica", "Helvetica-Bold"
    serif, serif_bold = "Times-Roman", "Times-Bold"
    fonts_dir = Path(__file__).parent / "fonts"
    if fonts_dir.exists():
        try:
            for face, file in [
                ("DMSans", "DMSans-Regular.ttf"),
                ("DMSans-Bold", "DMSans-Bold.ttf"),
                ("Lora", "Lora-Regular.ttf"),
                ("Lora-Bold", "Lora-Bold.ttf"),
            ]:
                p = fonts_dir / file
                if p.exists():
                    pdfmetrics.registerFont(TTFont(face, str(p)))
            if (fonts_dir / "DMSans-Regular.ttf").exists():
                sans = "DMSans"
                if (fonts_dir / "DMSans-Bold.ttf").exists():
                    sans_bold = "DMSans-Bold"
                    registerFontFamily("DMSans", normal="DMSans", bold="DMSans-Bold",
                                       italic="DMSans", boldItalic="DMSans-Bold")
            if (fonts_dir / "Lora-Regular.ttf").exists():
                serif = "Lora"
                if (fonts_dir / "Lora-Bold.ttf").exists():
                    serif_bold = "Lora-Bold"
                    registerFontFamily("Lora", normal="Lora", bold="Lora-Bold",
                                       italic="Lora", boldItalic="Lora-Bold")
        except Exception:
            pass  # fall back silently
    return sans, sans_bold, serif, serif_bold


# ---------- Custom flowables ----------

class DotRow(Flowable):
    """Renders 5 circular dots, `filled` of them coral, rest coral-light."""

    def __init__(self, filled: int, size: float = 12, gap: float = 6):
        super().__init__()
        self.filled = max(0, min(5, int(filled)))
        self.size = size
        self.gap = gap
        self.width = 5 * size + 4 * gap
        self.height = size

    def draw(self):
        c = self.canv
        for i in range(5):
            x = i * (self.size + self.gap) + self.size / 2
            y = self.size / 2
            c.setFillColor(CORAL if i < self.filled else CORAL_LIGHT)
            c.setStrokeColor(CORAL if i < self.filled else CORAL_LIGHT)
            c.circle(x, y, self.size / 2, stroke=1, fill=1)


class _BulletCircle(Flowable):
    """A single dot bullet — filled or stroked — used as list marker.
    Renders as drawn vector circle so it works regardless of font subset."""
    def __init__(self, color, diameter=8, filled=True, stroke_width=1.5):
        super().__init__()
        self.color = color
        self.diameter = diameter
        self.filled = filled
        self.stroke_width = stroke_width

    def wrap(self, aw, ah):
        return (self.diameter, self.diameter)

    def draw(self):
        r = self.diameter / 2.0
        if self.filled:
            self.canv.setFillColor(self.color)
            self.canv.circle(r, r, r, fill=1, stroke=0)
        else:
            self.canv.setStrokeColor(self.color)
            self.canv.setLineWidth(self.stroke_width)
            self.canv.circle(r, r, r - self.stroke_width / 2, fill=0, stroke=1)


class _RoundedPill(Flowable):
    """Stadium-shaped pill with text inside. Used for tags and number badges."""
    def __init__(self, text, font_name, font_size, fg_color, bg_color,
                 pad_x=8, pad_y=3, radius=10):
        super().__init__()
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.fg = fg_color
        self.bg = bg_color
        self.pad_x = pad_x
        self.pad_y = pad_y
        self.radius = radius
        from reportlab.pdfbase import pdfmetrics
        self._tw = pdfmetrics.stringWidth(text, font_name, font_size)

    def wrap(self, aw, ah):
        return (self._tw + 2 * self.pad_x, self.font_size + 2 * self.pad_y)

    def draw(self):
        w = self._tw + 2 * self.pad_x
        h = self.font_size + 2 * self.pad_y
        self.canv.setFillColor(self.bg)
        self.canv.setStrokeColor(self.bg)
        self.canv.roundRect(0, 0, w, h, self.radius, fill=1, stroke=0)
        self.canv.setFillColor(self.fg)
        self.canv.setFont(self.font_name, self.font_size)
        # Center text vertically: text baseline above bottom by ~pad_y + font_descent offset
        self.canv.drawString(self.pad_x, self.pad_y + 1, self.text)


# ---------- Page composition (skeleton) ----------

def _build_styles(sans: str, sans_bold: str, serif: str, serif_bold: str) -> dict[str, ParagraphStyle]:
    """Brand-aligned paragraph styles. Used by all page builders.

    Heading-weight elements use the bold serif/sans variants directly (not <b>
    wrapping) so the embedded font subset includes the bold faces and the
    visual hierarchy matches the locked design (e.g., title is Lora-Bold, not
    Lora-Regular with synthetic bold).
    """
    return {
        "brand": ParagraphStyle("brand", fontName=serif_bold, fontSize=13, leading=15,
                                textColor=CORAL, spaceAfter=10),
        "h1": ParagraphStyle("h1", fontName=serif_bold, fontSize=20, leading=24,
                             textColor=DARK, spaceAfter=8),
        "meta": ParagraphStyle("meta", fontName=sans, fontSize=10, leading=14,
                               textColor=WARM_GRAY, spaceAfter=14),
        "verdict_label": ParagraphStyle("vl", fontName=sans_bold, fontSize=8, leading=10,
                                        textColor=CORAL, spaceAfter=4),
        "verdict_body": ParagraphStyle("vb", fontName=sans, fontSize=11, leading=14,
                                       textColor=TEXT, spaceAfter=14),
        "h2": ParagraphStyle("h2", fontName=serif_bold, fontSize=18, leading=22,
                             textColor=DARK, spaceBefore=8, spaceAfter=10),
        "h3": ParagraphStyle("h3", fontName=sans_bold, fontSize=10, leading=13,
                             textColor=TEAL, spaceAfter=6),
        "body": ParagraphStyle("body", fontName=sans, fontSize=11, leading=15,
                               textColor=TEXT, spaceAfter=8),
        "direction_q": ParagraphStyle("dq", fontName=sans_bold, fontSize=10, leading=12,
                                      textColor=DARK, spaceAfter=2),
        "direction_label": ParagraphStyle("dl", fontName=serif_bold, fontSize=13, leading=15,
                                          textColor=DARK),
        "direction_explain": ParagraphStyle("de", fontName=sans, fontSize=9.5, leading=12,
                                            textColor=WARM_GRAY),
        "found_num": ParagraphStyle("fn", fontName=serif_bold, fontSize=18, leading=20,
                                    textColor=CORAL, alignment=TA_RIGHT),
        "found_label": ParagraphStyle("fl", fontName=sans, fontSize=11, leading=12,
                                      textColor=TEXT),
    }


def render(data: dict, out_dir: str | Path) -> dict[str, str]:
    """Main entry point. Validates data, generates the 6-page PDF deliverable."""
    validate_data(data)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / "final-report.pdf"

    sans, sans_bold, serif, serif_bold = _load_fonts()
    styles = _build_styles(sans, sans_bold, serif, serif_bold)
    # expose bold-sans name to flowables that build their own inline <font> markup
    styles["_sans_bold"] = sans_bold

    doc = SimpleDocTemplate(
        str(pdf_path), pagesize=letter,
        leftMargin=0.95 * inch, rightMargin=0.95 * inch,
        topMargin=0.7 * inch, bottomMargin=0.7 * inch,
        title=data["TITLE"],
    )

    story: list = []
    story += _build_page_1(data, styles)
    story.append(PageBreak())
    story += _build_findings(data, styles)
    story.append(PageBreak())
    story += _build_gaps(data, styles)
    story.append(PageBreak())
    story += _build_questions(data, styles)
    story.append(PageBreak())
    story += _build_clinical(data, styles)
    story.append(PageBreak())
    story += _build_references(data, styles)

    doc.build(story)
    return {"pdf": str(pdf_path)}


def _build_page_1(data: dict, S: dict) -> list:
    """Hero + verdict + dashboard. The chat-embedded image renders just this page."""
    story = [
        Paragraph("VERA · VERIFIED EVIDENCE RESEARCH ANALYST", S["brand"]),
        Paragraph(data["TITLE"], S["h1"]),
        Paragraph(data["PATIENT_META"] + f" &nbsp;·&nbsp; <b>Date:</b> {data['REPORT_DATE']}",
                  S["meta"]),
        _verdict_block(data["VERDICT_PARAGRAPH"], S),
        Spacer(1, 8),
        Paragraph("What does the evidence actually say?", S["h2"]),
        _direction_row("Will it help?", data["HELP_DOTS_FILLED"],
                       data["HELP_LABEL"], data["HELP_EXPLAIN"], S),
        _direction_row("Could it hurt?", data["HURT_DOTS_FILLED"],
                       data["HURT_LABEL"], data["HURT_EXPLAIN"], S),
        Spacer(1, 14),
        Paragraph("<b>What we found</b>", S["h3"]),
        _count_list(data["COUNTS"], S),
    ]
    return story


def _verdict_block(text: str, S: dict):
    """Left-bar callout for the honest answer."""
    inner = [
        Paragraph("THE HONEST ANSWER", S["verdict_label"]),
        Paragraph(text, S["verdict_body"]),
    ]
    tbl = Table([[inner]], colWidths=[6.0 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WARM_WHITE),
        ("LINEBEFORE", (0, 0), (0, -1), 3, CORAL),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    return tbl


def _direction_row(question: str, filled: int, label: str, explain: str, S: dict):
    """One row of the two-question rating."""
    q_cell = Paragraph(question.upper(), S["direction_q"])
    dots = DotRow(filled, size=11, gap=5)
    label_para = Paragraph(label, S["direction_label"])
    explain_para = Paragraph(explain, S["direction_explain"])
    text_cell = Table(
        [[label_para], [explain_para]],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ])
    )
    tbl = Table([[q_cell, dots, text_cell]],
                colWidths=[1.4 * inch, 1.3 * inch, 3.3 * inch])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, CORAL_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return tbl


def _count_list(counts: list[dict], S: dict):
    """Big coral number + plain-language label, optional rounded pill inline with label.

    Layout: 2-column outer table [count_num | label_cell]. label_cell is itself a
    horizontal 2-column sub-table [label_para | optional_pill] so the pill sits
    immediately to the right of its label (matching the locked v0 design), not
    floating at the right edge of the page.
    """
    rows = []
    # Hard cap: page 1 fits at most 4 count items (verdict block takes variable space).
    # Drop overflow silently — Phase 3 should pick the 4 most informative.
    counts = counts[:4]
    from reportlab.pdfbase.pdfmetrics import stringWidth as _sw
    label_font = S["found_label"].fontName
    label_size = S["found_label"].fontSize
    available_label_width = 5.45 * inch  # outer table col 2 width
    for c in counts:
        label_para = Paragraph(c["label"], S["found_label"])
        if c.get("tag"):
            pill = _RoundedPill(c["tag"].upper(), S["_sans_bold"], 7,
                                colors.white, CORAL)
            pill_w = pill.wrap(0, 0)[0]
            # Size label column to its actual text width so pill sits adjacent.
            # If label is long, fall back to fitting label + pill on one row.
            natural_label_w = _sw(c["label"], label_font, label_size) + 4
            max_label_w = available_label_width - pill_w - 16  # 8 gap + 8 spacer
            label_w = min(natural_label_w, max_label_w)
            label_cell = Table(
                [[label_para, pill, ""]],
                colWidths=[label_w, pill_w, None],
                style=TableStyle([
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ("LEFTPADDING", (1, 0), (1, 0), 8),  # gap between label and pill
                ])
            )
        else:
            label_cell = label_para
        rows.append([
            Paragraph(str(c["n"]), S["found_num"]),
            label_cell,
        ])
    tbl = Table(rows, colWidths=[0.55 * inch, 5.45 * inch])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (1, 0), (1, -1), 12),  # gap between count number and label
    ]))
    return tbl


# ---------- Page 2: Findings ----------

def _build_findings(data: dict, S: dict) -> list:
    story = [Paragraph("What the research says", S["h2"])]
    for f in data["FINDINGS"]:
        # If url provided, wrap the leading bold span (e.g., "2018 review") in <link>
        text = f["text"]
        if f.get("url"):
            # naive: wrap the first <b>...</b> in a link
            text = text.replace("<b>", f'<link href="{f["url"]}" color="#c4614a"><b>', 1)
            text = text.replace("</b>", "</b></link>", 1)
        story.append(Table(
            [[_BulletCircle(TEAL, diameter=8, filled=True), Paragraph(text, S["body"])]],
            colWidths=[0.22 * inch, 5.78 * inch],
            style=TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (0, 0), 7),
                ("TOPPADDING", (1, 0), (1, 0), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ])
        ))
        if f.get("coi"):
            story.append(Paragraph(
                f'<i>Conflict of interest:</i> {f["coi"]}',
                ParagraphStyle("coi", parent=S["body"], textColor=CORAL,
                               leftIndent=18, fontSize=10, spaceAfter=6),
            ))
    # Anecdotal callout — single shared coral-light box containing all anecdotal paragraphs.
    # Uses a Table with BACKGROUND style instead of Paragraph backColor+borderPadding,
    # which empirically overlapped the preceding finding text and produced layout drift.
    anec_paragraphs = []
    for i, para in enumerate(data["ANEC_PARAGRAPHS"]):
        if i > 0:
            anec_paragraphs.append(Spacer(1, 8))
        anec_paragraphs.append(Paragraph(para, ParagraphStyle(
            "anec", parent=S["body"], textColor=TEXT,
        )))
    if anec_paragraphs:
        story.append(Spacer(1, 14))  # clear gap before the box
        anec_tbl = Table(
            [[anec_paragraphs]],
            colWidths=[6.0 * inch],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), CORAL_LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
            ])
        )
        story.append(anec_tbl)
    return story


# ---------- Page 3: Gaps ----------

def _build_gaps(data: dict, S: dict) -> list:
    story = [Paragraph("What we don't know yet", S["h2"])]
    for g in data["GAPS"]:
        story.append(Table(
            [[_BulletCircle(CORAL, diameter=10, filled=False, stroke_width=1.5),
              Paragraph(f'<b>{g["headline"]}</b> {g["body"]}', S["body"])]],
            colWidths=[0.22 * inch, 5.78 * inch],
            style=TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (0, 0), 7),
                ("TOPPADDING", (1, 0), (1, 0), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ])
        ))
    return story


# ---------- Page 4: Questions ----------

def _build_questions(data: dict, S: dict) -> list:
    story = [
        Paragraph("Questions to bring to your doctor", S["h2"]),
        Paragraph(data["QUESTIONS_LEDE"],
                  ParagraphStyle("ql", parent=S["body"], textColor=WARM_GRAY, spaceAfter=12)),
    ]
    for i, q in enumerate(data["QUESTIONS"], 1):
        badge = _RoundedPill(str(i), S["_sans_bold"], 11, colors.white, CORAL,
                             pad_x=6, pad_y=3, radius=10)
        story.append(Table(
            [[badge, Paragraph(q["ask"], S["body"])]],
            colWidths=[0.35 * inch, 5.65 * inch],
            style=TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ])
        ))
        story.append(Paragraph(
            f'<i>{q["why"]}</i>',
            ParagraphStyle("qw", parent=S["body"], textColor=WARM_GRAY,
                           fontSize=9.5, leftIndent=24, spaceAfter=10)))
    return story


# ---------- Page 5: Clinical Summary (oncologist-facing) ----------

def _build_clinical(data: dict, S: dict) -> list:
    story = [Paragraph("Clinical Summary", S["h2"])]
    for kv in data["CLINICAL_KV"]:
        story.append(Paragraph(
            f'<b>{kv["label"]}:</b> {kv["value"]}',
            ParagraphStyle("kv", parent=S["body"], fontSize=9.5, leading=12, spaceAfter=2)))
    # Hard caps: page 5 fits at most 4 blocks, each ≤400 chars body. Truncate overflow.
    raw_blocks = data["CLINICAL_BLOCKS"][:4]
    blocks = []
    for b in raw_blocks:
        if len(b.get("body", "")) > 400:
            blocks.append({**b, "body": b["body"][:397].rsplit(" ", 1)[0] + "..."})
        else:
            blocks.append(b)
    for block in blocks:
        story.append(Spacer(1, 5))
        story.append(Paragraph(f'<font color="#3d7a73"><b>{block["title"].upper()}</b></font>',
                               ParagraphStyle("cbh", parent=S["h3"], spaceAfter=2)))
        story.append(Paragraph(block["body"],
                               ParagraphStyle("cb", parent=S["body"], fontSize=9.5, leading=12,
                                              spaceAfter=4, leftIndent=2, rightIndent=2)))
    return story


# ---------- Page 6: References ----------

def _build_references(data: dict, S: dict) -> list:
    story = [Paragraph("Reference list", S["h2"])]
    for i, r in enumerate(data["REFERENCES"], 1):
        story.append(Paragraph(
            f'<font color="#c4614a"><b>{i}</b></font>&nbsp;&nbsp; '
            f'<link href="{r["url"]}" color="#c4614a"><u>{r["citation"]}</u></link>',
            ParagraphStyle("ref", parent=S["body"], fontSize=10, leading=13, spaceAfter=6)))
    return story


# ---------- CLI for design review ----------

if __name__ == "__main__":
    import json
    import sys
    if len(sys.argv) != 3:
        print("Usage: python render_deliverable.py <data.json> <out_dir>")
        sys.exit(2)
    with open(sys.argv[1]) as f:
        data = json.load(f)
    paths = render(data, sys.argv[2])
    print(json.dumps(paths, indent=2))
