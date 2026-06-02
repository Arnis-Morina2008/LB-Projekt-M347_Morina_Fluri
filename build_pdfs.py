import sys
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line

# ----------------------------------------------------------------------
# 1. Numbered Canvas for Dynamic Page Numbering and Running Headers/Footers
# ----------------------------------------------------------------------
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        width, height = self._pagesize
        
        # LANDSCAPE (Presentation)
        if width > height:
            if self._pageNumber == 1:
                # Cover slide has dark background, no decorations
                self.restoreState()
                return
            
            # Slide page number
            self.setFont("Helvetica", 10)
            self.setFillColor(colors.HexColor("#555555"))
            page_text = f"Folie {self._pageNumber} von {page_count}"
            self.drawRightString(width - 40, 32, page_text)
            
        # PORTRAIT (Documentation)
        else:
            if self._pageNumber == 1:
                # Cover page has no header/footer
                self.restoreState()
                return
            
            # Header
            self.setFont("Helvetica-Oblique", 9)
            self.setFillColor(colors.HexColor("#666666"))
            self.drawString(54, height - 40, "LB-Projekt M347 - Dienst in Betrieb nehmen")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(54, height - 46, width - 54, height - 46)
            
            # Footer
            self.line(54, 55, width - 54, 55)
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor("#666666"))
            self.drawString(54, 42, "Autoren: A. Morina & K. Fluri")
            page_text = f"Seite {self._pageNumber} von {page_count}"
            self.drawRightString(width - 54, 42, page_text)
            
        self.restoreState()


# ----------------------------------------------------------------------
# 2. Slide Layout Drawing Callbacks
# ----------------------------------------------------------------------
def draw_cover_slide(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(colors.HexColor('#0d254c'))
    canvas_obj.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=True, stroke=False)
    canvas_obj.restoreState()

def draw_normal_slide(canvas_obj, doc):
    canvas_obj.saveState()
    # Bottom separator line
    canvas_obj.setStrokeColor(colors.HexColor('#cccccc'))
    canvas_obj.setLineWidth(1)
    canvas_obj.line(40, 50, doc.pagesize[0] - 40, 50)
    
    # Footer text
    canvas_obj.setFont("Helvetica-Bold", 10)
    canvas_obj.setFillColor(colors.HexColor('#555555'))
    canvas_obj.drawString(40, 32, "LB-Projekt M347: Dienst in Betrieb nehmen")
    canvas_obj.restoreState()


# ----------------------------------------------------------------------
# 3. Dynamic Vector Infrastructure Diagram
# ----------------------------------------------------------------------
def make_infrastructure_diagram():
    d = Drawing(480, 210)
    
    # Background Host Box
    d.add(Rect(10, 10, 460, 190, strokeColor=colors.HexColor('#999999'), fillColor=colors.HexColor('#fafafa'), strokeWidth=1, strokeDashArray=[2,2]))
    d.add(String(20, 185, "DOCKER HOST SYSTEM", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#444444')))
    
    # Wordpress Block
    d.add(Rect(30, 95, 75, 45, fillColor=colors.HexColor('#0073aa'), strokeColor=colors.HexColor('#005177'), rx=3, ry=3))
    d.add(String(67, 120, "WordPress App", textAnchor="middle", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d.add(String(67, 107, "Port 8080:80", textAnchor="middle", fontName="Helvetica", fontSize=7, fillColor=colors.white))
    
    d.add(Line(67, 95, 67, 70, strokeColor=colors.HexColor('#666666'), strokeWidth=1.2))
    d.add(String(71, 78, "Bridge Net", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=colors.HexColor('#666666')))
    
    d.add(Rect(30, 25, 75, 45, fillColor=colors.HexColor('#4f5d95'), strokeColor=colors.HexColor('#3b4870'), rx=3, ry=3))
    d.add(String(67, 50, "MariaDB (WP)", textAnchor="middle", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d.add(String(67, 37, "Vol: db_data", textAnchor="middle", fontName="Helvetica", fontSize=7, fillColor=colors.white))
    
    # MediaWiki Block
    d.add(Rect(140, 95, 75, 45, fillColor=colors.HexColor('#3366cc'), strokeColor=colors.HexColor('#2a52be'), rx=3, ry=3))
    d.add(String(177, 120, "MediaWiki App", textAnchor="middle", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d.add(String(177, 107, "Port 8081:80", textAnchor="middle", fontName="Helvetica", fontSize=7, fillColor=colors.white))
    
    d.add(Line(177, 95, 177, 70, strokeColor=colors.HexColor('#666666'), strokeWidth=1.2))
    d.add(String(181, 78, "Bridge Net", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=colors.HexColor('#666666')))
    
    d.add(Rect(140, 25, 75, 45, fillColor=colors.HexColor('#4f5d95'), strokeColor=colors.HexColor('#3b4870'), rx=3, ry=3))
    d.add(String(177, 50, "MariaDB (MW)", textAnchor="middle", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d.add(String(177, 37, "Vol: db_data", textAnchor="middle", fontName="Helvetica", fontSize=7, fillColor=colors.white))

    # Jira Block
    d.add(Rect(250, 95, 75, 45, fillColor=colors.HexColor('#0052cc'), strokeColor=colors.HexColor('#0747a6'), rx=3, ry=3))
    d.add(String(287, 120, "Jira Software", textAnchor="middle", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d.add(String(287, 107, "Port 8082:8080", textAnchor="middle", fontName="Helvetica", fontSize=7, fillColor=colors.white))
    
    d.add(Line(287, 95, 287, 70, strokeColor=colors.HexColor('#666666'), strokeWidth=1.2))
    d.add(String(291, 78, "Bridge Net", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=colors.HexColor('#666666')))
    
    d.add(Rect(250, 25, 75, 45, fillColor=colors.HexColor('#336791'), strokeColor=colors.HexColor('#274e71'), rx=3, ry=3))
    d.add(String(287, 50, "PostgreSQL", textAnchor="middle", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d.add(String(287, 37, "Vol: pg_data", textAnchor="middle", fontName="Helvetica", fontSize=7, fillColor=colors.white))

    # Portainer Block
    d.add(Rect(360, 95, 75, 45, fillColor=colors.HexColor('#3f9cd8'), strokeColor=colors.HexColor('#267cb5'), rx=3, ry=3))
    d.add(String(397, 120, "Portainer CE", textAnchor="middle", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d.add(String(397, 107, "Port 9000/9443", textAnchor="middle", fontName="Helvetica", fontSize=7, fillColor=colors.white))
    
    d.add(Line(397, 95, 397, 70, strokeColor=colors.HexColor('#aa2222'), strokeWidth=1.2, strokeDashArray=[1,1]))
    d.add(String(401, 78, "Socket Bind", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=colors.HexColor('#aa2222')))
    
    d.add(Rect(360, 25, 75, 45, fillColor=colors.HexColor('#e0e0e0'), strokeColor=colors.HexColor('#888888'), rx=3, ry=3))
    d.add(String(397, 50, "docker.sock", textAnchor="middle", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.black))
    d.add(String(397, 37, "(Host Engine)", textAnchor="middle", fontName="Helvetica", fontSize=7, fillColor=colors.black))
    
    return d


# ----------------------------------------------------------------------
# 4. Markdown-to-Flowables Parser
# ----------------------------------------------------------------------
def parse_markdown_to_flowables(file_path, styles):
    flowables = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Code Block
        if line.strip().startswith('```'):
            if in_code_block:
                in_code_block = False
                # Add code block flowable
                code_text = '\n'.join(code_lines)
                code_style = ParagraphStyle(
                    'CodeStyle',
                    parent=styles['Normal'],
                    fontName='Courier',
                    fontSize=8,
                    leading=10,
                    textColor=colors.HexColor('#333333'),
                )
                # Use a Table to draw the background box for code
                p = Paragraph(code_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)
                code_table = Table([[p]], colWidths=[480])
                code_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f5f5f5')),
                    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
                    ('PADDING', (0,0), (-1,-1), 6),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ]))
                flowables.append(code_table)
                flowables.append(Spacer(1, 10))
                code_lines = []
            else:
                in_code_block = True
            i += 1
            continue
            
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
            
        # Table
        if line.strip().startswith('|'):
            in_table = True
            # Parse row
            cells = [c.strip() for c in line.split('|')[1:-1]]
            # If it's a separator row (like |:---|:---|), skip it
            if all(c.replace('-', '').replace(':', '').strip() == '' for c in cells):
                i += 1
                continue
            table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table:
                in_table = False
                # Compile Table flowable
                table_data = []
                for r_idx, row in enumerate(table_rows):
                    row_data = []
                    for c_idx, cell in enumerate(row):
                        # Simple format conversions for cell contents
                        cell_clean = cell.replace('**', '').replace('`', '')
                        if r_idx == 0:
                            # Header
                            style = ParagraphStyle(
                                f'TH_{r_idx}_{c_idx}',
                                parent=styles['Normal'],
                                fontName='Helvetica-Bold',
                                fontSize=8,
                                leading=10,
                                textColor=colors.white
                            )
                        else:
                            # Body
                            style = ParagraphStyle(
                                f'TD_{r_idx}_{c_idx}',
                                parent=styles['Normal'],
                                fontName='Helvetica',
                                fontSize=8,
                                leading=10,
                            )
                        row_data.append(Paragraph(cell_clean, style))
                    table_data.append(row_data)
                
                # Determine column widths
                col_widths = None
                if len(table_data[0]) == 4:
                    col_widths = [50, 210, 80, 140] # Specially for our test protocols
                
                t = Table(table_data, colWidths=col_widths)
                
                # Table style
                t_styles = [
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0d254c')),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
                    ('TOPPADDING', (0,0), (-1,-1), 5),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                    ('LEFTPADDING', (0,0), (-1,-1), 5),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                ]
                # Alternating row colors
                for row_idx in range(1, len(table_data)):
                    if row_idx % 2 == 0:
                        t_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor('#f9f9f9')))
                
                t.setStyle(TableStyle(t_styles))
                flowables.append(t)
                flowables.append(Spacer(1, 10))
                table_rows = []
                
        # Empty Line
        if line.strip() == '':
            i += 1
            continue
            
        # Horizontal Rule
        if line.strip() in ['---', '***', '___']:
            flowables.append(Spacer(1, 10))
            hr = Table([['']], colWidths=[480])
            hr.setStyle(TableStyle([
                ('LINEABOVE', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
            ]))
            flowables.append(hr)
            flowables.append(Spacer(1, 10))
            i += 1
            continue
            
        # Heading 1
        if line.startswith('# '):
            text = line[2:].strip().replace('**', '')
            flowables.append(Paragraph(text, styles['Heading1']))
            flowables.append(Spacer(1, 8))
            i += 1
            continue
            
        # Heading 2
        if line.startswith('## '):
            text = line[3:].strip().replace('**', '')
            flowables.append(Paragraph(text, styles['Heading2']))
            flowables.append(Spacer(1, 6))
            i += 1
            continue
            
        # Heading 3
        if line.startswith('### '):
            text = line[4:].strip().replace('**', '')
            flowables.append(Paragraph(text, styles['Heading3']))
            flowables.append(Spacer(1, 4))
            i += 1
            continue
            
        # Bullet list
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:].strip()
            # Basic formatting replacement
            text_clean = text.replace('**', '<b>', 1).replace('**', '</b>', 1)
            text_clean = text_clean.replace('`', '<font name="Courier">', 1).replace('`', '</font>', 1)
            bullet_style = ParagraphStyle(
                'BulletStyle',
                parent=styles['Normal'],
                leftIndent=15,
                firstLineIndent=-10
            )
            flowables.append(Paragraph(f"&bull;&nbsp;&nbsp;{text_clean}", bullet_style))
            flowables.append(Spacer(1, 4))
            i += 1
            continue
            
        # Paragraph Text
        text = line.strip()
        # Basic markdown formatting conversions
        text_clean = text
        while '**' in text_clean:
            text_clean = text_clean.replace('**', '<b>', 1).replace('**', '</b>', 1)
        while '`' in text_clean:
            text_clean = text_clean.replace('`', '<font name="Courier">', 1).replace('`', '</font>', 1)
            
        flowables.append(Paragraph(text_clean, styles['Normal']))
        flowables.append(Spacer(1, 8))
        i += 1
        
    return flowables


# ----------------------------------------------------------------------
# 5. Build Document PDF (Projektdokumentation)
# ----------------------------------------------------------------------
def build_projektdokumentation_pdf():
    styles = getSampleStyleSheet()
    
    # Custom base styles
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 14
    styles['Normal'].textColor = colors.HexColor('#222222')
    
    styles['Heading1'].fontSize = 18
    styles['Heading1'].leading = 22
    styles['Heading1'].textColor = colors.HexColor('#0d254c')
    styles['Heading1'].spaceBefore = 12
    styles['Heading1'].spaceAfter = 8
    styles['Heading1'].keepWithNext = True
    
    styles['Heading2'].fontSize = 14
    styles['Heading2'].leading = 18
    styles['Heading2'].textColor = colors.HexColor('#0052cc')
    styles['Heading2'].spaceBefore = 10
    styles['Heading2'].spaceAfter = 6
    styles['Heading2'].keepWithNext = True

    styles['Heading3'].fontSize = 11
    styles['Heading3'].leading = 14
    styles['Heading3'].textColor = colors.HexColor('#333333')
    styles['Heading3'].spaceBefore = 8
    styles['Heading3'].spaceAfter = 4
    styles['Heading3'].keepWithNext = True

    story = []
    
    # Page 1: COVER PAGE
    story.append(Spacer(1, 40))
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.HexColor('#0d254c'),
        alignment=0,
    )
    story.append(Paragraph("LB-Projekt M347: Dienst in Betrieb nehmen", title_style))
    story.append(Spacer(1, 12))
    
    sub_style = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#555555')
    )
    story.append(Paragraph("Verteilte Infrastruktur mit WordPress, MediaWiki, Jira Software und Portainer", sub_style))
    story.append(Spacer(1, 20))
    
    # Blue accent bar
    bar = Table([['']], colWidths=[480])
    bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0d254c')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(bar)
    story.append(Spacer(1, 160))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Modul:</b>", styles['Normal']), Paragraph("M347 - Dienst in Betrieb nehmen", styles['Normal'])],
        [Paragraph("<b>Autoren:</b>", styles['Normal']), Paragraph("Arnis Morina & Kilian Fluri", styles['Normal'])],
        [Paragraph("<b>Klasse:</b>", styles['Normal']), Paragraph("4. Semester", styles['Normal'])],
        [Paragraph("<b>Schule:</b>", styles['Normal']), Paragraph("Benedict Schule", styles['Normal'])],
        [Paragraph("<b>Datum:</b>", styles['Normal']), Paragraph("2. Juni 2026", styles['Normal'])],
    ]
    meta_table = Table(meta_data, colWidths=[80, 400])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#eeeeee')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(PageBreak())
    
    # Page 2: TABLE OF CONTENTS
    story.append(Paragraph("Inhaltsverzeichnis", styles['Heading1']))
    story.append(Spacer(1, 15))
    
    toc_data = [
        ["1. Einleitung und Zielsetzung", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Seite 3"],
        ["2. Infrastruktur und Architektur", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Seite 3"],
        ["3. Konfiguration der Microservices", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Seite 4"],
        ["4. Testkonzept (Testpläne)", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Seite 5"],
        ["5. Testprotokolle (Testergebnisse)", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Seite 6"],
        ["6. Installationsanleitung", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Seite 7"],
        ["7. Hilfestellungen und Quellenverzeichnis", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Seite 8"],
        ["8. Arbeitsjournal: Arnis Morina", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Seite 9"],
        ["9. Arbeitsjournal: Kilian Fluri", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Seite 10"],
    ]
    
    toc_table_data = []
    for section, dots, page in toc_data:
        toc_table_data.append([
            Paragraph(f"<b>{section}</b>", styles['Normal']),
            Paragraph(dots, ParagraphStyle('dots', parent=styles['Normal'], textColor=colors.HexColor('#999999'), alignment=1)),
            Paragraph(page, ParagraphStyle('page', parent=styles['Normal'], alignment=2))
        ])
        
    toc_table = Table(toc_table_data, colWidths=[180, 240, 60])
    toc_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(toc_table)
    story.append(PageBreak())
    
    # Pages 3-8: DOKUMENTATION INHALTE (doku.md)
    doku_flowables = parse_markdown_to_flowables('src_docs/doku.md', styles)
    
    # Find Section 2 "Infrastruktur und Architektur" and inject the vector diagram!
    injected = False
    for flow in doku_flowables:
        # Avoid writing the title block lines (Heading 1 at start) since we have our custom cover page
        if isinstance(flow, Paragraph) and flow.text == "LB-Projekt M347: Dienst in Betrieb nehmen":
            continue
        if isinstance(flow, Paragraph) and flow.text.startswith("Modul:") and "LB-Projekt" in flow.text:
            continue
        if isinstance(flow, Paragraph) and flow.text.startswith("Autoren:") and "Morina" in flow.text:
            continue
        if isinstance(flow, Paragraph) and flow.text.startswith("Datum:") and "2026" in flow.text:
            continue
        if isinstance(flow, Paragraph) and flow.text.startswith("Schule:") and "Benedict" in flow.text:
            continue
        if isinstance(flow, Paragraph) and flow.text.startswith("Klasse:") and "4. Semester" in flow.text:
            continue
            
        story.append(flow)
        
        # Inject diagram under the infrastructure text
        if not injected and isinstance(flow, Paragraph) and "detailliertes Infrastrukturdiagramm" in flow.text:
            story.append(Spacer(1, 10))
            story.append(make_infrastructure_diagram())
            story.append(Spacer(1, 15))
            injected = True
            
    story.append(PageBreak())
    
    # Page 9: JOURNAL ARNIS MORINA (journal_morina.md)
    journal_morina_flowables = parse_markdown_to_flowables('src_docs/journal_morina.md', styles)
    for flow in journal_morina_flowables:
        story.append(flow)
        
    story.append(PageBreak())
    
    # Page 10: JOURNAL KILIAN FLURI (journal_fluri.md)
    journal_fluri_flowables = parse_markdown_to_flowables('src_docs/journal_fluri.md', styles)
    for flow in journal_fluri_flowables:
        story.append(flow)
        
    # Build the document
    doc = SimpleDocTemplate(
        "Projektdokumentation.pdf",
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Projektdokumentation.pdf successfully compiled.")


# ----------------------------------------------------------------------
# 6. Build Presentation PDF (Präsentation)
# ----------------------------------------------------------------------
def make_slide_title(title_text):
    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.white,
        alignment=1 # Center
    )
    p = Paragraph(title_text, style)
    t = Table([[p]], colWidths=[762]) # 842 - 80 margins
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0d254c')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def build_presentation_pdf():
    styles = getSampleStyleSheet()
    
    with open('src_docs/slides.md', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split content by '---' to get each slide
    slides_raw = content.split('\n---\n')
    story = []
    
    # First Slide: Cover Slide (Dark blue background handled by draw_cover_slide)
    cover_slide = slides_raw[0]
    story.append(Spacer(1, 90))
    cover_lines = cover_slide.strip().split('\n')
    for line in cover_lines:
        if line.startswith('# '):
            title = line[2:].strip()
            style = ParagraphStyle(
                'CoverSlideTitle',
                fontName='Helvetica-Bold',
                fontSize=30,
                leading=36,
                textColor=colors.white,
                alignment=1
            )
            story.append(Paragraph(title, style))
            story.append(Spacer(1, 20))
        elif line.strip() != '':
            text = line.strip().replace('**', '').replace('*', '')
            style = ParagraphStyle(
                'CoverSlideText',
                fontName='Helvetica',
                fontSize=13,
                leading=17,
                textColor=colors.HexColor('#dddddd'),
                alignment=1
            )
            story.append(Paragraph(text, style))
            story.append(Spacer(1, 8))
            
    story.append(PageBreak())
    
    # Normal Slides
    for slide_raw in slides_raw[1:]:
        lines = slide_raw.strip().split('\n')
        
        slide_title = ""
        slide_body_lines = []
        for line in lines:
            if line.startswith('# '):
                slide_title = line[2:].strip()
                if ':' in slide_title:
                    slide_title = slide_title.split(':', 1)[1].strip()
            else:
                slide_body_lines.append(line)
                
        # Slide Header Banner
        story.append(make_slide_title(slide_title))
        story.append(Spacer(1, 25))
        
        # Check if the slide is the Infrastructure slide (Slide 4) to embed diagram!
        is_infrastructure_slide = ("Infrastruktur" in slide_title)
        
        if is_infrastructure_slide:
            # We will split slide horizontally or just add the diagram and bullets.
            # Let's add bullets first, then diagram inside a centered table, or side-by-side!
            # Side-by-side is amazing for 16:9 landscape!
            bullet_texts = []
            for line in slide_body_lines:
                if line.strip().startswith('- ') or line.strip().startswith('* '):
                    text = line.strip()[2:].strip()
                    text_clean = text.replace('**', '<b>', 1).replace('**', '</b>', 1)
                    text_clean = text_clean.replace('`', '<font name="Courier">', 1).replace('`', '</font>', 1)
                    bullet_texts.append(text_clean)
            
            bullet_html = "".join([f"&bull;&nbsp;&nbsp;{t}<br/><br/>" for t in bullet_texts])
            bullet_style = ParagraphStyle(
                'SlideBulletInfra',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=12,
                leading=16,
                textColor=colors.HexColor('#333333')
            )
            bullet_p = Paragraph(bullet_html, bullet_style)
            
            # Create a 2-column layout Table: Left Column = Bullets (320px), Right Column = Diagram (420px)
            # Resize the diagram slightly for the slide layout
            diag = make_infrastructure_diagram()
            
            layout_table = Table([[bullet_p, diag]], colWidths=[320, 442])
            layout_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 10),
                ('RIGHTPADDING', (0,0), (-1,-1), 10),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(layout_table)
        else:
            # Normal slide rendering
            for line in slide_body_lines:
                if line.strip() == '':
                    continue
                if line.strip().startswith('- ') or line.strip().startswith('* '):
                    text = line.strip()[2:].strip()
                    text_clean = text.replace('**', '<b>', 1).replace('**', '</b>', 1)
                    text_clean = text_clean.replace('`', '<font name="Courier">', 1).replace('`', '</font>', 1)
                    bullet_style = ParagraphStyle(
                        'SlideBulletNormal',
                        parent=styles['Normal'],
                        fontName='Helvetica',
                        fontSize=15,
                        leading=22,
                        leftIndent=40,
                        firstLineIndent=-15,
                        textColor=colors.HexColor('#333333')
                    )
                    story.append(Paragraph(f"&bull;&nbsp;&nbsp;{text_clean}", bullet_style))
                    story.append(Spacer(1, 12))
                else:
                    text = line.strip().replace('**', '<b>', 1).replace('**', '</b>', 1)
                    text_clean = text.replace('`', '<font name="Courier">', 1).replace('`', '</font>', 1)
                    style = ParagraphStyle(
                        'SlideTextNormal',
                        parent=styles['Normal'],
                        fontName='Helvetica',
                        fontSize=14,
                        leading=20,
                        leftIndent=20,
                        textColor=colors.HexColor('#333333')
                    )
                    story.append(Paragraph(text_clean, style))
                    story.append(Spacer(1, 8))
                    
        story.append(PageBreak())
        
    doc = SimpleDocTemplate(
        "Präsentation.pdf",
        pagesize=landscape(A4),
        leftMargin=40,
        rightMargin=40,
        topMargin=30,
        bottomMargin=60
    )
    doc.build(story, onFirstPage=draw_cover_slide, onLaterPages=draw_normal_slide, canvasmaker=NumberedCanvas)
    print("Präsentation.pdf successfully compiled.")


# ----------------------------------------------------------------------
# 7. Main Execution
# ----------------------------------------------------------------------
if __name__ == '__main__':
    try:
        build_projektdokumentation_pdf()
        build_presentation_pdf()
        print("All PDFs successfully built.")
    except Exception as e:
        print(f"Error during PDF compilation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
