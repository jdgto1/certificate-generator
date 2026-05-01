from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter
import io

# =========================
# FONT
# =========================
pdfmetrics.registerFont(TTFont("Times", "fonts/times.ttf"))

def generate_idcec_certificate(data):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # =========================
    # NAME - CENTERED BY TEXT CENTER
    # =========================
    NAME_CENTER_X = 385
    NAME_CENTER_Y = 390
 
    name_text = data["person_name"]

    can.setFont("Times", 14.04)

   # ajuste vertical (baseline fix)
    NAME_Y = NAME_CENTER_Y - 9

    can.drawCentredString(NAME_CENTER_X, NAME_Y, name_text)

    # =========================
    # DATE OF ISSUE
    # =========================
    DATE_X = 200
    DATE_Y = 117

    can.setFont("Times", 14.04)
    can.drawString(DATE_X, DATE_Y, data["date_of_issue"])

    # =========================

    # =========================
    # SAVE CANVAS
    # =========================
    can.save()
    packet.seek(0)

    # =========================
    # MERGE WITH TEMPLATE
    # =========================
    template = PdfReader(data["template_path"])
    overlay = PdfReader(packet)

    output = PdfWriter()
    page = template.pages[0]
    page.merge_page(overlay.pages[0])
    output.add_page(page)

    output_stream = io.BytesIO()
    output.write(output_stream)
    output_stream.seek(0)

    return output_stream