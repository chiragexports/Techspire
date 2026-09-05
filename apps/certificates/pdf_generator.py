import os
from io import BytesIO
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_certificate_pdf_buffer(certificate, request=None):
    """
    Generates a high-quality, professional landscape PDF certificate for TECHSPIRE Learning.
    """
    buffer = BytesIO()
    
    # Page size: Landscape Letter (11 x 8.5 inches)
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter) # 792 x 612 points

    # Ensure QR code exists
    if not certificate.qr_code:
        certificate.generate_qr_code(request)
        certificate.save()

    # 1. Background styling
    c.setFillColor(colors.HexColor('#F8FAFC')) # light slate bg
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # 2. Elegant Outer & Inner Borders
    c.setStrokeColor(colors.HexColor('#1E3A8A')) # Dark Blue border
    c.setLineWidth(6)
    c.rect(20, 20, width - 40, height - 40)

    c.setStrokeColor(colors.HexColor('#D97706')) # Warm Gold accent border
    c.setLineWidth(2)
    c.rect(28, 28, width - 56, height - 56)

    # Corner decorative accents
    corner_size = 25
    c.setFillColor(colors.HexColor('#1E3A8A'))
    # Top Left
    c.rect(28, height - 28 - corner_size, corner_size, corner_size, fill=1, stroke=0)
    # Top Right
    c.rect(width - 28 - corner_size, height - 28 - corner_size, corner_size, corner_size, fill=1, stroke=0)
    # Bottom Left
    c.rect(28, 28, corner_size, corner_size, fill=1, stroke=0)
    # Bottom Right
    c.rect(width - 28 - corner_size, 28, corner_size, corner_size, fill=1, stroke=0)

    # 3. Header Branding
    c.setFillColor(colors.HexColor('#1E3A8A'))
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2.0, height - 75, "TECHSPIRE LEARNING")

    c.setFillColor(colors.HexColor('#D97706'))
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2.0, height - 95, "Learn Today, Lead Tomorrow. • Certificate of Completion")

    # Thin separator line
    c.setStrokeColor(colors.HexColor('#CBD5E1'))
    c.setLineWidth(1)
    c.line(width / 2.0 - 180, height - 105, width / 2.0 + 180, height - 105)

    # 4. Presentation Text
    c.setFillColor(colors.HexColor('#475569'))
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2.0, height - 140, "This is proudly presented to")

    # 5. Student Full Name
    c.setFillColor(colors.HexColor('#0F172A'))
    c.setFont("Helvetica-Bold", 28)
    student_name = certificate.user.full_name
    c.drawCentredString(width / 2.0, height - 185, student_name)

    # Underline for name
    c.setStrokeColor(colors.HexColor('#2563EB'))
    c.setLineWidth(2)
    name_width = c.stringWidth(student_name, "Helvetica-Bold", 28)
    c.line(width / 2.0 - (name_width / 2.0) - 15, height - 195, width / 2.0 + (name_width / 2.0) + 15, height - 195)

    # 6. Completion narrative
    c.setFillColor(colors.HexColor('#334155'))
    c.setFont("Helvetica", 13)
    c.drawCentredString(width / 2.0, height - 230, "for successfully demonstrating mastery and completing all curriculum requirements for")

    # 7. Course Title
    c.setFillColor(colors.HexColor('#1E3A8A'))
    c.setFont("Helvetica-Bold", 20)
    course_title = certificate.course.title
    c.drawCentredString(width / 2.0, height - 268, course_title)

    # 8. Description / Score Detail
    c.setFillColor(colors.HexColor('#64748B'))
    c.setFont("Helvetica-Oblique", 11)
    issued_date_str = certificate.issued_at.strftime("%B %d, %Y")
    c.drawCentredString(width / 2.0, height - 300, f"Issued on {issued_date_str} • Passing Score: {certificate.score_percentage:.1f}% • ID: {certificate.certificate_id}")

    # 9. Left Column: QR Code & Verification
    if certificate.qr_code and os.path.exists(certificate.qr_code.path):
        c.drawImage(certificate.qr_code.path, 60, 60, width=75, height=75)
    
    c.setFillColor(colors.HexColor('#64748B'))
    c.setFont("Helvetica", 9)
    c.drawString(145, 115, "Scan QR or verify online at:")
    c.setFillColor(colors.HexColor('#2563EB'))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(145, 98, f"techspire.in/verify/?id={certificate.certificate_id}")
    c.setFillColor(colors.HexColor('#64748B'))
    c.setFont("Helvetica", 8)
    c.drawString(145, 82, "Udyam Reg: UDYAM-MP-23-0283495")
    c.drawString(145, 68, "Indore, Madhya Pradesh, India")

    # 10. Center: Gold Medallion / Seal
    c.setFillColor(colors.HexColor('#FEF3C7'))
    c.setStrokeColor(colors.HexColor('#D97706'))
    c.setLineWidth(2)
    c.circle(width / 2.0, 95, 36, fill=1, stroke=1)
    
    c.setFillColor(colors.HexColor('#92400E'))
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(width / 2.0, 102, "VERIFIED")
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(width / 2.0, 88, "EXCELLENCE")

    # 11. Right Column: Signature of Vivek Jat
    sig_x = width - 230
    c.setStrokeColor(colors.HexColor('#1E293B'))
    c.setLineWidth(1.5)
    c.line(sig_x, 100, width - 60, 100)

    c.setFillColor(colors.HexColor('#1E3A8A'))
    c.setFont("Helvetica-BoldOblique", 14)
    c.drawCentredString(sig_x + 85, 112, "Vivek Jat")

    c.setFillColor(colors.HexColor('#0F172A'))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(sig_x + 85, 85, "Vivek Jat")

    c.setFillColor(colors.HexColor('#64748B'))
    c.setFont("Helvetica", 9)
    c.drawCentredString(sig_x + 85, 72, "Proprietor & Lead Director")
    c.drawCentredString(sig_x + 85, 59, "TECHSPIRE, Indore (M.P.)")

    # Finalize PDF
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer
