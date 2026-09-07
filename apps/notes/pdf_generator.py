import io
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header
        self.drawString(54, 750, "TECHSPIRE Learning — Premium Technical Notes")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 744, 558, 744)

        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}  |  Licensed to: {getattr(self, 'licensee_email', 'Verified Student')}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "© 2026 TECHSPIRE Learning. All Rights Reserved.")
        self.line(54, 48, 558, 48)
        self.restoreState()


def generate_notes_pdf_buffer(product, user=None):
    """
    Generates a high-quality educational PDF book for a NotesProduct.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=60,
        bottomMargin=60
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#0F172A") # Navy
    accent_color = colors.HexColor("#1E3A8A")  # Royal Blue
    amber_color = colors.HexColor("#D97706")   # Amber Gold
    text_color = colors.HexColor("#1E293B")

    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=15
    )

    cover_sub_style = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=amber_color,
        alignment=1,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'ChapterH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceBefore=15,
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=accent_color,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'NoteBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=text_color,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'NoteBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        leftIndent=15,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#F8FAFC"),
        spaceAfter=0
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # 1. COVER PAGE
    story.append(Spacer(1, 40))
    story.append(Paragraph("TECHSPIRE LEARNING", ParagraphStyle('CoverBrand', fontName='Helvetica-Bold', fontSize=14, textColor=amber_color, alignment=1, spaceAfter=20)))
    story.append(Spacer(1, 20))
    story.append(Paragraph(product.title, cover_title_style))
    if product.subtitle:
        story.append(Paragraph(product.subtitle, cover_sub_style))
    story.append(HRFlowable(width="60%", thickness=2, color=amber_color, spaceAfter=30))
    
    metadata_text = f"""
    <b>Category:</b> {product.category.name}<br/>
    <b>Difficulty:</b> {product.get_difficulty_display()}<br/>
    <b>Version:</b> {product.version}<br/>
    <b>Published:</b> {product.updated_at.strftime('%B %Y')}<br/>
    <b>Author:</b> {product.author_name}
    """
    story.append(Paragraph(metadata_text, ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=10, leading=16, alignment=1, textColor=colors.HexColor("#475569"))))
    
    story.append(Spacer(1, 100))
    license_user = user.email if (user and user.is_authenticated) else "Verified Licensed Student"
    license_box = [
        [Paragraph(f"<b>OFFICIAL LICENSED STUDY MATERIAL</b><br/>Licensed to: <i>{license_user}</i><br/>Unique License ID: TS-LIC-{timezone.now().strftime('%Y%m%d')}-001<br/>All rights reserved. Unauthorized redistribution is prohibited.", ParagraphStyle('LicenseText', fontName='Helvetica', fontSize=8, leading=11, alignment=1, textColor=colors.HexColor("#334155")))]
    ]
    t = Table(license_box, colWidths=[400])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t)
    story.append(PageBreak())

    # 2. TABLE OF CONTENTS
    story.append(Paragraph("Table of Contents", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceAfter=15))

    toc_data = []
    chapters = list(product.chapters.all().order_by('order'))
    for ch in chapters:
        toc_data.append([
            Paragraph(f"<b>Chapter {ch.order}:</b> {ch.title}", body_style),
            Paragraph(f"Est. {ch.read_time_mins} mins", ParagraphStyle('TocRight', fontName='Helvetica', fontSize=9, alignment=2, textColor=colors.HexColor("#64748B")))
        ])
    
    if toc_data:
        toc_table = Table(toc_data, colWidths=[380, 120])
        toc_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#F1F5F9")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(toc_table)
    
    story.append(PageBreak())

    # 3. CHAPTERS CONTENT
    for ch in chapters:
        story.append(Paragraph(f"Chapter {ch.order}: {ch.title}", h1_style))
        if ch.summary:
            story.append(Paragraph(f"<i>Overview: {ch.summary}</i>", ParagraphStyle('SummaryItalic', fontName='Helvetica-Oblique', fontSize=9.5, leading=14, textColor=colors.HexColor("#475569"), spaceAfter=10)))
        
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceAfter=10))

        # Split content into paragraphs or simple text blocks
        lines = ch.content_markdown.split('\n')
        in_code_block = False
        code_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('```'):
                if in_code_block:
                    # End code block
                    code_content = "<br/>".join([Paragraph(cl, code_style).text for cl in code_lines])
                    code_table = Table([[Paragraph(code_content, code_style)]], colWidths=[490])
                    code_table.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
                        ('TOPPADDING', (0,0), (-1,-1), 8),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                        ('LEFTPADDING', (0,0), (-1,-1), 10),
                        ('RIGHTPADDING', (0,0), (-1,-1), 10),
                        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
                    ]))
                    story.append(code_table)
                    story.append(Spacer(1, 6))
                    code_lines = []
                    in_code_block = False
                else:
                    in_code_block = True
                    code_lines = []
                continue

            if in_code_block:
                code_lines.append(line.replace('<', '&lt;').replace('>', '&gt;'))
                continue

            if not stripped:
                continue

            if stripped.startswith('# '):
                story.append(Paragraph(stripped[2:], h1_style))
            elif stripped.startswith('## '):
                story.append(Paragraph(stripped[3:], h2_style))
            elif stripped.startswith('### '):
                story.append(Paragraph(stripped[4:], ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=primary_color, spaceBefore=8, spaceAfter=4)))
            elif stripped.startswith('- ') or stripped.startswith('* '):
                story.append(Paragraph(f"• {stripped[2:]}", bullet_style))
            elif stripped.startswith('> [!IMPORTANT]') or stripped.startswith('> [!TIP]') or stripped.startswith('> [!WARNING]'):
                # Callout box
                callout_title = "IMPORTANT NOTE" if "IMPORTANT" in stripped else ("PRO TIP" if "TIP" in stripped else "WARNING")
                callout_data = [[Paragraph(f"<b>{callout_title}:</b> Key exam & production takeaway.", callout_style)]]
                ctable = Table(callout_data, colWidths=[490])
                ctable.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
                    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ]))
                story.append(ctable)
                story.append(Spacer(1, 4))
            elif stripped.startswith('>'):
                story.append(Paragraph(stripped[1:].strip(), ParagraphStyle('Quote', fontName='Helvetica-Oblique', fontSize=9, leading=13, leftIndent=12, textColor=colors.HexColor("#475569"))))
            else:
                story.append(Paragraph(stripped, body_style))

        # Takeaways Box
        if ch.key_takeaways:
            story.append(Spacer(1, 6))
            takeaway_paras = [Paragraph("<b>Key Chapter Takeaways:</b>", ParagraphStyle('TbTitle', fontName='Helvetica-Bold', fontSize=9.5, textColor=colors.HexColor("#065F46")))]
            for t in ch.takeaways_list:
                takeaway_paras.append(Paragraph(f"✓ {t}", ParagraphStyle('TbItem', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#065F46"))))
            
            tbox = Table([[takeaway_paras]], colWidths=[490])
            tbox.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ECFDF5")),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#10B981")),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(tbox)

        story.append(PageBreak())

    # Build PDF
    canvas_maker = NumberedCanvas
    if user and user.is_authenticated:
        canvas_maker.licensee_email = user.email
    else:
        canvas_maker.licensee_email = "TECHSPIRE Student"

    doc.build(story, canvasmaker=canvas_maker)
    pdf_value = buffer.getvalue()
    buffer.close()
    return pdf_value
