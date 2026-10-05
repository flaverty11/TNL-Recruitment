#!/usr/bin/env python3
"""Build the free parent guide PDF (downloads/tnl-parent-guide.pdf).

Run from the repo root:  python3 guide/build_guide.py
Needs: pip install reportlab   (uses the macOS Georgia fonts)
"""
import os
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "downloads", "tnl-parent-guide.pdf")
LOGO = os.path.join(ROOT, "images", "tnl-logo.png")
FONTS = "/System/Library/Fonts/Supplemental"

pdfmetrics.registerFont(TTFont("Serif", f"{FONTS}/Georgia.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Italic", f"{FONTS}/Georgia Italic.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", f"{FONTS}/Georgia Bold.ttf"))

INK = HexColor("#111111")
BODY = HexColor("#333333")
MUTED = HexColor("#6b6b6b")
GOLD = HexColor("#8c6d1f")
GOLD_BRIGHT = HexColor("#c9a84c")
RULE = HexColor("#e2ddd2")
CREAM = HexColor("#f6f2ea")
DARK = HexColor("#0b0b0b")

W, H = A4
M = 20 * mm

st = {
    "h1": ParagraphStyle("h1", fontName="Serif", fontSize=24, leading=29, textColor=INK, spaceAfter=4),
    "kicker": ParagraphStyle("kicker", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=GOLD, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="Serif", fontSize=15, leading=19, textColor=INK, spaceBefore=14, spaceAfter=5),
    "lead": ParagraphStyle("lead", fontName="Helvetica", fontSize=12, leading=18, textColor=INK, spaceAfter=10),
    "p": ParagraphStyle("p", fontName="Helvetica", fontSize=10.5, leading=16, textColor=BODY, spaceAfter=7),
    "li": ParagraphStyle("li", fontName="Helvetica", fontSize=10.5, leading=15.5, textColor=BODY, leftIndent=14, bulletIndent=2, spaceAfter=4),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=BODY),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=9.5, leading=13.5, textColor=INK),
    "th": ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=GOLD),
    "box": ParagraphStyle("box", fontName="Helvetica", fontSize=10.5, leading=16, textColor=INK),
}


def P(text, s="p"):
    return Paragraph(text, st[s])


def bullets(items):
    return [Paragraph(i, st["li"], bulletText="•") for i in items]


def numbered(items):
    return [Paragraph(i, st["li"], bulletText=f"{n}.") for n, i in enumerate(items, 1)]


def table(rows, widths):
    data = [[Paragraph(c, st["th"]) for c in rows[0]]]
    for r in rows[1:]:
        data.append([Paragraph(r[0], st["cellb"])] + [Paragraph(c, st["cell"]) for c in r[1:]])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 1, GOLD),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def callout(text):
    t = Table([[Paragraph(text, st["box"])]], colWidths=[W - 2 * M])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("LINEBEFORE", (0, 0), (0, -1), 3, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    return KeepTogether([Spacer(1, 4), t, Spacer(1, 8)])


def cover(c, doc):
    c.saveState()
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    size = 62 * mm
    c.drawImage(LOGO, (W - size) / 2, H - 40 * mm - size, size, size, mask="auto")
    y = H - 40 * mm - size - 22 * mm
    c.setFillColor(GOLD_BRIGHT)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W / 2, y, "FREE PARENT GUIDE  ·  2026–27 EDITION")
    c.setFillColor(white)
    c.setFont("Serif", 30)
    c.drawCentredString(W / 2, y - 18 * mm, "The UK & Irish Parent's Guide to")
    c.setFillColor(GOLD_BRIGHT)
    c.setFont("Serif-Italic", 34)
    c.drawCentredString(W / 2, y - 33 * mm, "US Soccer Scholarships")
    c.setFillColor(HexColor("#bdbdbd"))
    c.setFont("Helvetica", 11.5)
    for i, line in enumerate(["Costs, grades, timelines and the questions to ask,",
                              "explained in plain English for football families."]):
        c.drawCentredString(W / 2, y - 48 * mm - i * 6 * mm, line)
    c.setFillColor(HexColor("#8a8a8a"))
    c.setFont("Helvetica", 9.5)
    c.drawCentredString(W / 2, 22 * mm, "The Next Level  ·  tnlrecruitment.com  ·  WhatsApp +44 7346 804838")
    c.restoreState()


def inner(c, doc):
    c.saveState()
    c.drawImage(LOGO, M, H - 15 * mm, 7 * mm, 7 * mm, mask="auto")
    c.setFont("Serif", 10)
    c.setFillColor(INK)
    c.drawString(M + 9 * mm, H - 12.6 * mm, "The Next Level")
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawRightString(W - M, H - 12.6 * mm, "Parent Guide to US Soccer Scholarships")
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(M, H - 17 * mm, W - M, H - 17 * mm)
    c.line(M, 15 * mm, W - M, 15 * mm)
    c.drawString(M, 10 * mm, "tnlrecruitment.com")
    c.drawRightString(W - M, 10 * mm, str(doc.page))
    c.restoreState()


def story():
    s = [NextPageTemplate("inner"), PageBreak()]

    s += [P("WELCOME", "kicker"), P("Why the US?", "h1"),
          P("Every year hundreds of UK and Irish players swap Saturday league football for a US college team, "
            "a degree and a full-time training environment. If your son or daughter loves the game and wants "
            "a good education, it's one of the best options available.", "lead"),
          P("In the UK most players have to choose between football and education at around 16. US college soccer "
            "lets them do both: daily training, strength and conditioning, physios and travel to away games, "
            "alongside a recognised degree. Plenty of players go on to the professional game; the rest finish with a "
            "degree, great experiences and often very little debt."),
          P("This guide covers what parents ask us most: how the system works, what it really costs, which grades "
            "matter, when to start and what to watch out for.")]
    s += [P("In this guide", "h2")] + bullets([
        "How US college soccer is organised",
        "What a scholarship covers, and what families still pay",
        "Grades and eligibility for UK and Irish students",
        "A recruiting timeline by age and school year",
        "Highlight reels that coaches actually watch",
        "The student visa and moving to the US",
        "Questions to ask any coach, and any agency",
    ])

    s += [PageBreak(), P("THE SYSTEM", "kicker"), P("How US college soccer works", "h1"),
          P("There are several governing bodies, each with their own divisions and rules. The best fit is the "
            "programme where your child will play, develop and earn a degree they want, and that's not always the "
            "biggest name.", "lead"),
          table([
              ["Level", "Athletic scholarships", "Good fit for"],
              ["NCAA Division I", "Yes. Rules changed from 2025–26, with many schools moving from scholarship caps to roster limits.", "High-level players with solid grades, ready to fight for minutes."],
              ["NCAA Division II", "Yes, usually partial and shared across the squad.", "Good players who want a high level, real minutes and a balanced student life."],
              ["NCAA Division III", "No athletic scholarships, but often generous academic and merit awards.", "Strong students who want competitive football and a top academic experience."],
              ["NAIA", "Yes, usually partial and often combined with academic aid.", "Players who want a smaller university, playing time and more flexible recruiting rules."],
              ["NJCAA (junior college)", "Division I can offer full scholarships; Division II covers costs such as tuition, fees and books; Division III has no athletic aid.", "Late developers, players who need to boost grades, or a cheaper first two years before transferring."],
          ], [38 * mm, 66 * mm, 66 * mm]),
          callout("<b>Tip:</b> ask every coach directly, \"Where would I fit on your team in my first season?\" "
                  "Playing time matters more than the badge on the shirt.")]

    s += [PageBreak(), P("MONEY", "kicker"), P("What it really costs", "h1"),
          P("Every US university publishes a yearly <b>cost of attendance</b>: tuition and fees, accommodation and meals, "
            "books, and usually health insurance. It ranges from roughly <b>$25,000 a year</b> at some smaller or public "
            "universities to <b>$80,000 or more</b> at expensive private ones.", "lead"),
          P("A full scholarship exists but is rare in soccer. Most offers are <b>partial</b>: a coach splits a limited "
            "budget across the squad, so you might be offered 30%, 50% or 70% of costs. International students generally "
            "can't get US government financial aid, so athletic and academic awards are where the savings come from, and "
            "the two can often be combined."),
          P("A worked example (illustration only)", "h2"),
          table([
              ["", "Per year"],
              ["Cost of attendance", "$45,000"],
              ["Athletic scholarship (50%)", "−$22,500"],
              ["Academic award for strong grades", "−$8,000"],
              ["What the family pays", "$14,500"],
          ], [110 * mm, 60 * mm]),
          Spacer(1, 6),
          P("Also budget for", "h2")] + bullets([
              "Flights, usually a couple of return trips a year",
              "Student visa costs (the SEVIS fee and the visa application fee)",
              "Health insurance if it isn't included",
              "Day-to-day spending money. Kit, training and away travel are normally covered by the team.",
          ]) + [callout("<b>Compare offers by the total your family pays per year after all aid</b>, not the headline "
                        "percentage. A 50% offer at a cheaper university can cost less than 70% at an expensive one.")]

    s += [PageBreak(), P("ACADEMICS", "kicker"), P("Grades and eligibility", "h1"),
          P("Football gets a coach interested. Grades decide whether your child is eligible, whether the university "
            "admits them, and how much academic money can be added to an athletic offer.", "lead"),
          table([
              ["Where you studied", "What universities look at"],
              ["England, Wales &amp; NI", "GCSEs (or IGCSEs) and A-levels, or BTECs"],
              ["Scotland", "National 5s, Highers and Advanced Highers"],
              ["Ireland", "Junior Cycle and the Leaving Certificate"],
          ], [55 * mm, 115 * mm]),
          Spacer(1, 4)] + bullets([
              "<b>NCAA Division I and II:</b> register with the NCAA Eligibility Center, which checks school records against "
              "its standards for international students. Division III schools set their own admission standards.",
              "<b>NAIA:</b> has its own eligibility centre and rules for international students.",
              "<b>Junior college:</b> generally requires completed secondary school; each college checks your records.",
              "<b>SAT/ACT:</b> no longer required by the NCAA, but some universities still ask for them for admission or scholarships.",
              "<b>English tests:</b> UK and Irish students usually don't need one, but a few universities ask.",
              "<b>Before final results:</b> universities often work from results so far, predicted grades and a school reference.",
          ]) + [callout("<b>Keep copies of every certificate and results slip</b> from GCSE or Junior Cycle onwards. "
                        "If your child has played for a club that pays players, get advice about amateur status before registering.")]

    s += [PageBreak(), P("TIMING", "kicker"), P("When to start", "h1"),
          P("US college soccer is played in the autumn and coaches plan squads a year or more ahead. Starting early "
            "means more options, more time to improve footage and grades, and more choice when offers arrive.", "lead"),
          table([
              ["Age", "School year", "What to focus on"],
              ["14–15", "Year 10 · S3 · 3rd year", "Grades, playing at the highest level possible, and filming matches."],
              ["15–16", "Year 11 · S4 · TY", "Research the options, build a first highlight reel, start emailing coaches. NCAA D1 and D2 coaches generally can't start recruiting conversations until 15 June after this year; NAIA and junior college coaches can reply sooner."],
              ["16–17", "Year 12 · S5 · 5th year", "The main recruiting year: calls, video chats and offers. Register with the NCAA and/or NAIA eligibility centres."],
              ["17–18", "Year 13 · S6 · 6th year", "Compare offers, apply, sign, sort the visa and book travel for early-August pre-season."],
          ], [18 * mm, 42 * mm, 110 * mm]),
          callout("<b>Already 18 or older?</b> There are still options, especially at NCAA D2, NAIA and junior college, "
                  "where squads fill later. Under NCAA rules, organised football after leaving school can eventually count "
                  "against college eligibility, so get advice before assuming a gap year is \"free\".")]

    s += [PageBreak(), P("FOOTAGE", "kicker"), P("Highlight reels that get watched", "h1"),
          P("The highlight reel is usually the first time a coach sees your child play. Coaches receive a lot of them "
            "and decide quickly.", "lead")] + bullets([
              "<b>Keep it to 3–5 minutes</b>, with the best clips in the first 30–60 seconds.",
              "<b>Make it obvious which player is yours</b>: freeze the frame and add an arrow or circle before each clip.",
              "<b>Start with a title card</b>: name, position, preferred foot, date of birth, start year, height, club and league, headline grades, email and phone.",
              "<b>Show what the position needs</b>, not just goals: defending 1v1, receiving on the half-turn, movement, distribution.",
              "<b>Use footage from the last 12 months</b>, filmed from high up where possible (a stand, or a camera like Veo).",
              "<b>Have one or two full matches ready to send.</b> Interested coaches will ask.",
              "<b>Avoid</b> loud music, slow motion, 10-minute reels and old footage.",
              "<b>Host it on YouTube as unlisted</b> (or Hudl) and send the link rather than a large file.",
          ])

    s += [Spacer(1, 18), P("THE MOVE", "kicker"), P("The student visa", "h1"),
          P("Once your child accepts a place, the university issues a form called the <b>I-20</b>. You then pay the "
            "SEVIS fee, apply for an <b>F-1 student visa</b> and attend an interview at the US Embassy in London, or in "
            "Dublin for Irish citizens. Leave plenty of time, as appointment waiting times vary. Most players arrive in "
            "<b>early August</b> for pre-season.")]

    s += [PageBreak(), P("CHECKLISTS", "kicker"), P("Questions to ask", "h1"),
          P("Questions to ask any coach", "h2")] + numbered([
              "Where would I fit on your team in my first season?",
              "What is the total cost to us per year after all athletic and academic aid?",
              "Is the scholarship renewable each year, and on what conditions?",
              "Does it cover the summer, health insurance or books?",
              "How many international players are on the squad, and how do they settle in?",
              "Is my intended degree available, and does the training schedule allow for it?",
              "Can we speak to a current player?",
          ]) + [P("Questions to ask any agency, including us", "h2")] + numbered([
              "What exactly do you charge, and is it a one-off fee? Ask for prices in writing.",
              "What happens if my child doesn't receive an offer?",
              "Who will actually work with my child, and how often will we hear from you?",
              "Which universities have you placed players like mine at recently?",
              "Can we speak to families you've worked with?",
          ]) + [callout("<b>Be wary of anyone who guarantees a scholarship.</b> Final decisions sit with coaches and "
                        "universities. A good adviser tells you honestly where your child stands.")]

    s += [PageBreak(), P("NEXT STEPS", "kicker"), P("How The Next Level can help", "h1"),
          P("We help UK and Irish footballers win soccer scholarships at US universities, from NCAA Division I to junior "
            "college. Since 2018 we've worked with players at every level, from pro academies to school teams.", "lead"),
          table([
              ["Package", "One-off price", "Includes"],
              ["Prospect", "£450", "Athlete profile, highlight reel edit, outreach to 600+ coaches, NCAA eligibility guidance, 3 months' support."],
              ["Contender", "£1,000", "Everything in Prospect plus more reel edits, outreach to 1,000+ coaches, campus visit coordination, scholarship negotiation and a dedicated advisor. 6 months' support."],
              ["Elite Pro", "£1,350", "Everything in Contender plus Division I targeting, unlimited reel edits, outreach to 2,000+ coaches, full visa and enrolment support and pre-arrival mentoring. 12 months' support."],
          ], [28 * mm, 28 * mm, 114 * mm]),
          callout("<b>Start with a free evaluation.</b> Tell us about your child's football and grades and an advisor will "
                  "reply within 24 hours with an honest assessment. There's no obligation.<br/><br/>"
                  "<b>Apply:</b> tnlrecruitment.com/#apply<br/>"
                  "<b>WhatsApp:</b> +44 7346 804838<br/>"
                  "<b>Email:</b> tnlrecruitment@outlook.com<br/>"
                  "<b>More guides:</b> tnlrecruitment.com/blog"),
          Spacer(1, 10),
          P("This guide is general information, correct to the best of our knowledge in 2026. Eligibility, scholarship "
            "and visa rules change, so always confirm details with the university, the NCAA or NAIA, and the US Embassy.",
            "cell")]
    return s


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=26 * mm, bottomMargin=22 * mm,
                          title="The UK & Irish Parent's Guide to US Soccer Scholarships",
                          author="The Next Level", subject="US soccer scholarships for UK and Irish players")
    frame = Frame(M, 22 * mm, W - 2 * M, H - 48 * mm, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate("cover", [frame], onPage=cover), PageTemplate("inner", [frame], onPage=inner)])
    doc.build(story())
    print("wrote", OUT)


if __name__ == "__main__":
    build()
