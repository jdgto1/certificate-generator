from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PyPDF2 import PdfReader, PdfWriter
import io

# =========================
# FUENTES (CLOUD SAFE)
# =========================
pdfmetrics.registerFont(TTFont('Arial', 'fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'fonts/arialbd.ttf'))

def generate_certificate(data):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    PAGE_WIDTH, PAGE_HEIGHT = letter

    # =========================
    # POSICIONES BASE
    # =========================
    LEFT = 108
    RIGHT_MARGIN = 40
    usable_width = PAGE_WIDTH - LEFT - RIGHT_MARGIN

    NAME_Y = 530

    # 🔥 CONTROL ABSOLUTO DEL BLOQUE
    COURSE_Y = 410   # 👈 AJUSTA SOLO ESTE VALOR

    # =========================
    # NOMBRE
    # =========================
    can.setFont("Arial-Bold", 24)
    can.drawString(LEFT, NAME_Y, data["person_name"])

    # =========================
    # CURSO (WRAP)
    # =========================
    course_style = ParagraphStyle(
        name="CourseStyle",
        fontName="Arial-Bold",
        fontSize=24,
        leading=28,
        wordWrap='LTR'
    )

    course = Paragraph(data["course_name"], course_style)

    # Calcula tamaño
    w, h = course.wrap(usable_width, 200)

    # 🔥 POSICIÓN FIJA REAL
    course.drawOn(can, LEFT, COURSE_Y)

    # =========================
    # DETALLES
    # =========================
    can.setFont("Arial", 12)

    details_y = COURSE_Y - h - 18

    can.drawString(
        LEFT,
        details_y,
        f"Course Number {data['course_number']}, Session Number {data['session_number']}"
    )

    # =========================
    # FECHA
    # =========================
    can.drawString(
        LEFT,
        details_y - 18,
        data["date"]
    )

    can.save()
    packet.seek(0)

    # =========================
    # MERGE CON TEMPLATE
    # =========================
    template = PdfReader("template.pdf")
    overlay = PdfReader(packet)

    output = PdfWriter()
    page = template.pages[0]
    page.merge_page(overlay.pages[0])
    output.add_page(page)

    output_stream = io.BytesIO()
    output.write(output_stream)
    output_stream.seek(0)

    return output_stream