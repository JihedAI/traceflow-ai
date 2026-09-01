from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

OUT = Path("public/mock-documents")
OUT.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="DocumentTitle", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=21, leading=25, textColor=colors.HexColor("#1d2733"), spaceAfter=7))
styles.add(ParagraphStyle(name="Subtle", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=12, textColor=colors.HexColor("#687384")))
styles.add(ParagraphStyle(name="BodyCopy", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5, leading=15, textColor=colors.HexColor("#303b48")))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=colors.HexColor("#263b50"), spaceBefore=14, spaceAfter=7))

def header(story, company, doc_id, title, subtitle):
    story += [Paragraph(company.upper(), ParagraphStyle("brand", parent=styles["Subtle"], fontName="Helvetica-Bold", textColor=colors.HexColor("#4853a5"), tracking=1.2)), Spacer(1, 8), Paragraph(title, styles["DocumentTitle"]), Paragraph(subtitle, styles["Subtle"]), Spacer(1, 14)]
    info = [["Document ID", doc_id, "Issue date", "28 August 2026"], ["Status", "Controlled copy", "Prepared by", "Compliance Office"]]
    table = Table(info, colWidths=[27*mm, 52*mm, 27*mm, 52*mm])
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f4f6f8")), ("GRID", (0,0), (-1,-1), .25, colors.HexColor("#d9dee5")), ("FONTNAME", (0,0), (-1,-1), "Helvetica"), ("FONTSIZE", (0,0), (-1,-1), 8), ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#465160")), ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"), ("FONTNAME", (2,0), (2,-1), "Helvetica-Bold"), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7)]))
    story += [table]

def section(story, heading, body):
    story += [Paragraph(heading, styles["Section"]), Paragraph(body, styles["BodyCopy"])]

def data_table(story, rows, widths=(54, 116)):
    table = Table(rows, colWidths=[w*mm for w in widths], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#263b50")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTNAME", (0,1), (-1,-1), "Helvetica"), ("FONTSIZE", (0,0), (-1,-1), 8.5), ("LEADING", (0,0), (-1,-1), 11), ("GRID", (0,0), (-1,-1), .35, colors.HexColor("#d5dce4")), ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f7f9fb")]), ("VALIGN", (0,0), (-1,-1), "TOP"), ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7), ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8)]))
    story += [Spacer(1, 8), table]

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d9dee5")); canvas.line(18*mm, 14*mm, 192*mm, 14*mm)
    canvas.setFont("Helvetica", 7.5); canvas.setFillColor(colors.HexColor("#788393"))
    canvas.drawString(18*mm, 9*mm, "Demo document - generic sample content - not a commercial certificate")
    canvas.drawRightString(192*mm, 9*mm, f"Page {doc.page}")
    canvas.restoreState()

def build(name, company, doc_id, title, subtitle, content):
    doc = SimpleDocTemplate(str(OUT / name), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=21*mm)
    story=[]; header(story, company, doc_id, title, subtitle); content(story)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)

def bom(story):
    section(story, "Product scope", "This controlled bill of materials identifies the primary components approved for the AeroStep Runner sample, style S-042. Quantities are expressed per pair and are intended for traceability demonstrations.")
    data_table(story, [["Component", "Material specification", "Supplier / reference"], ["Upper", "Full-grain bovine leather, finished, 1.4-1.6 mm", "LeatherWorks Italia / L-18"], ["Lining", "Recycled polyester mesh, 120 g/m2", "Nova Textiles / NT-204"], ["Outsole", "Natural rubber compound, carbon black free", "RubberForm / RF-88"], ["Insole", "Molded EVA foam with textile cover", "Nova Components / NC-17"]], (43, 79, 48))
    section(story, "Revision note", "Revision 3 clarifies the approved outsole material. Any supplier substitution requires written product engineering approval before production release.")

def declaration(story):
    section(story, "Declaration", "LeatherWorks Italia declares that the material supplied under reference L-18 is intended for use in AeroStep Runner, style S-042, manufactured for Nova Footwear.")
    data_table(story, [["Declared attribute", "Value"], ["Material", "Full-grain bovine leather"], ["Upper composition", "Approximately 78% of the finished upper by mass"], ["Tannery reference", "LWI-TN-418"], ["Finish", "Water-based protective finish"], ["Production lot", "L18-0826-A"]])
    section(story, "Traceability statement", "The material is tracked by production lot from incoming hide selection through finishing. Supporting country-of-origin documentation may be provided separately upon customer request.")
    section(story, "Authorized sign-off", "Compliance Office, LeatherWorks Italia | Signed electronically for demonstration purposes")

def reach_old(story):
    section(story, "Compliance declaration", "Based on supplier information and internal assessment, the material covered by this declaration is intended to meet applicable restricted-substances requirements under Regulation (EC) No 1907/2006 (REACH).")
    data_table(story, [["Assessment item", "Result"], ["Material reference", "L-18 finished leather"], ["SVHC communication", "No intentionally added listed substance above reporting threshold"], ["Issue date", "15 January 2025"], ["Validity", "Valid through 31 December 2025"]])
    section(story, "Important notice", "This expired sample declaration is included for workflow testing only. A current declaration is required before the product record may be published.")

def origin(story):
    section(story, "Origin confirmation", "This letter confirms the country of origin recorded for the bovine leather supplied under material reference L-18 for the AeroStep Runner S-042 program.")
    data_table(story, [["Traceability attribute", "Confirmed value"], ["Material reference", "L-18 full-grain bovine leather"], ["Country of origin", "Italy"], ["Tannery location", "Santa Croce sull'Arno, Italy"], ["Supporting lot", "L18-0826-A"], ["Confirmation date", "28 August 2026"]])
    section(story, "Statement", "The origin value above is supported by the supplier's lot traceability records. This document is a generic demo example and does not attest to a real commercial shipment.")

def reach_new(story):
    section(story, "Compliance declaration", "LeatherWorks Italia confirms that the L-18 finished leather supplied for AeroStep Runner S-042 has been assessed against its restricted-substances management program and applicable REACH communication requirements.")
    data_table(story, [["Assessment item", "Result"], ["Material reference", "L-18 finished leather"], ["SVHC communication", "No intentionally added listed substance above reporting threshold"], ["Latest internal review", "22 August 2026"], ["Validity", "Valid through 31 December 2026"], ["Declaration reference", "L18-REACH-2026"]])
    section(story, "Authorized sign-off", "Compliance Office, LeatherWorks Italia | Current controlled copy for workflow demonstration")

build("BOM_S042.pdf", "Nova Footwear", "BOM-S042-REV3", "Bill of Materials", "AeroStep Runner / Style S-042 / Product engineering release", bom)
build("Supplier_L18.pdf", "LeatherWorks Italia", "L18-DECL-2026-08", "Supplier Material Declaration", "Material declaration for AeroStep Runner S-042", declaration)
build("REACH_L18.pdf", "LeatherWorks Italia", "L18-REACH-2025", "REACH Declaration", "Archived declaration - expired sample", reach_old)
build("LeatherOrigin_L18.pdf", "LeatherWorks Italia", "L18-ORIGIN-2026", "Country of Origin Confirmation", "Supporting traceability evidence for material L-18", origin)
build("REACH_L18_2026.pdf", "LeatherWorks Italia", "L18-REACH-2026", "REACH Declaration", "Current controlled declaration", reach_new)
