import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Custom canvas to handle two-pass page numbering and professional running footers."""
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
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        
        # Draw top running header (Skipped on cover page)
        if self._pageNumber > 1:
            self.drawString(54, 750, "JARVIS AI: ARCHITECTURAL SPECIFICATION & TECHNICAL REPORT")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
            # Bottom running footer
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 40, page_text)
            self.drawString(54, 40, "CONFIDENTIAL - INTERNAL DEVELOPMENT USE ONLY")
            self.line(54, 52, 558, 52)
            
        self.restoreState()

def build_pdf(filename="Jarvis_Project_Report.pdf"):
    # Target 0.75-inch margins (54 points) for professional print clearance
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette Definitions Archetype (Deep Tech Indigo/Slate)
    PRIMARY = colors.HexColor("#1A2B4C")
    SECONDARY = colors.HexColor("#2E5B88")
    TEXT_COLOR = colors.HexColor("#1C1E21")
    BG_LIGHT = colors.HexColor("#F8F9FA")
    BORDER_COLOR = colors.HexColor("#E2E8F0")
    
    # Modify/Inject Typography Configurations
    styles.add(ParagraphStyle(
        name='CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=10
    ))
    
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=SECONDARY,
        spaceAfter=30
    ))

    styles.add(ParagraphStyle(
        name='ReportHeading1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='ReportHeading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=TEXT_COLOR,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name='CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#232629"),
        spaceAfter=0
    ))

    story = []
    
    # ---------------------------------------------------------
    # COVER PAGE BLOCK
    # ---------------------------------------------------------
    story.append(Spacer(1, 100))
    story.append(Paragraph("PROJECT JARVIS: SYSTEM SPECIFICATION REPORT", styles['CoverTitle']))
    story.append(Paragraph("Production Architecture, Unified Intent Routing, Framework Benchmarks & Interview Readiness", styles['CoverSubtitle']))
    
    story.append(Spacer(1, 40))
    meta_text = """
    <b>Author / Lead Engineer:</b> Anirudh Baror<br/>
    <b>Supervisor Blueprint Engine:</b> Gemini Client Engine<br/>
    <b>Commencement Date:</b> June 28, 2026<br/>
    <b>Unified Freeze Date:</b> July 5, 2026<br/>
    <b>System Build Version:</b> 1.0.0-Stable (Phase-1 Build)
    """
    story.append(Paragraph(meta_text, styles['ReportBody']))
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # SECTION 1: SYSTEM OVERVIEW
    # ---------------------------------------------------------
    story.append(Paragraph("1. System Architecture & Contextual Scope", styles['ReportHeading1']))
    story.append(Paragraph(
        "Project Jarvis represents an implementation of a decoupled modular voice automation system. "
        "Unlike legacy monolithic applications where routing logic, communication bindings, and hardware "
        "interfacing exist in a unified script, Jarvis breaks down computational concerns into strictly "
        "independent sub-packages: <b>ai</b>, <b>voice</b>, and <b>automation</b>.",
        styles['ReportBody']
    ))
    
    story.append(Paragraph("Why Decoupling Was Mandatory (Kyu Kiya):", styles['ReportHeading2']))
    story.append(Paragraph(
        "Monolithic architectures suffer from high regression risk. Modifying an audio listener parameters "
        "could inadvertently break API calls. By splitting concerns into native Python packages containing "
        "explicit <code>__init__.py</code> initializers, components communicate across clear borders, lowering "
        "maintenance costs and allowing seamless scaling for complex pipelines.",
        styles['ReportBody']
    ))
    
    # ---------------------------------------------------------
    # SECTION 2: LIBRARY REGISTRY & TAXONOMY
    # ---------------------------------------------------------
    story.append(Paragraph("2. Core Dependency Analysis & Infrastructure", styles['ReportHeading1']))
    story.append(Paragraph(
        "Below is the complete registry of production-level frameworks bound within the virtualized local architecture:",
        styles['ReportBody']
    ))
    
    lib_data = [
        [Paragraph("<b>Framework / Library</b>", styles['ReportBody']), 
         Paragraph("<b>Location Matrix</b>", styles['ReportBody']), 
         Paragraph("<b>Functional Mandate (Kyu and Kahan Use Kiya)</b>", styles['ReportBody'])],
        
        [Paragraph("<code>google-genai</code>", styles['CodeStyle']),
         Paragraph("<code>ai/gemini_client.py</code>", styles['CodeStyle']),
         Paragraph("Provides production access to Google Gemini flagship LLM engines for processing unbounded cognitive strings.", styles['ReportBody'])],
        
        [Paragraph("<code>python-dotenv</code>", styles['CodeStyle']),
         Paragraph("Root Engine Namespace", styles['CodeStyle']),
         Paragraph("Extracts localized cryptographic tokens and environment settings from <code>.env</code> file directly into OS system variables.", styles['ReportBody'])],
        
        [Paragraph("<code>webbrowser</code>", styles['CodeStyle']),
         Paragraph("<code>automation/browser.py</code>", styles['CodeStyle']),
         Paragraph("Native low-level wrapper interface used to inject uniform resource identifiers (URIs) cleanly into OS default platform browsers.", styles['ReportBody'])],
         
        [Paragraph("<code>urllib.parse</code>", styles['CodeStyle']),
         Paragraph("<code>automation/browser.py</code>", styles['CodeStyle']),
         Paragraph("Sanitizes standard audio text string inputs into URL-encoded tokens via <code>quote_plus()</code> method mappings.", styles['ReportBody'])]
    ]
    
    t = Table(lib_data, colWidths=[100, 130, 274])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BORDER_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    # ---------------------------------------------------------
    # SECTION 3: INTENT ROUTING LOGIC & CONSOLIDATION
    # ---------------------------------------------------------
    story.append(Paragraph("3. Central Engine Design & Intent Redirection", styles['ReportHeading1']))
    story.append(Paragraph(
        "The control center of the assistant relies inside <code>main.py</code>. The architecture uses "
        "an optimized, deterministic conditional intent scanner bound inside an infinite runtime thread. "
        "When an audio query string passes through the listener matrix, it undergoes structured checking:",
        styles['ReportBody']
    ))
    
    story.append(Paragraph("Mathematical String Sanitization & Loop Control:", styles['ReportHeading2']))
    story.append(Paragraph(
        "To stop commands from leaking into cognitive AI layers, we use the <code>continue</code> statement "
        "inside our intent routing rules. As soon as an execution condition matches a deterministic system path "
        "(e.g., Google Search or YouTube opening), the control sequence instantly returns back to the beginning of the main processing loop. "
        "This completely avoids processing unwanted code blocks and drops token calculation overhead down to exactly 0.",
        styles['ReportBody']
    ))
    
    # ---------------------------------------------------------
    # SECTION 4: PRODUCTION-READY SECURITY POLICIES
    # ---------------------------------------------------------
    story.append(Paragraph("4. Virtualization & Runtime Security Framework", styles['ReportHeading1']))
    story.append(Paragraph(
        "To ensure production security, two safety mechanisms are strictly enforced across the system codebase:",
        styles['ReportBody']
    ))
    story.append(Paragraph(
        "<b>A. Cryptographic Masking via `.gitignore`:</b> The configuration tokens and API keys are stored in a "
        "non-tracked local file (<code>.env</code>). Git explicitly skips tracking this path, blocking high-risk credential leaks to public GitHub remote sync paths.",
        styles['ReportBody']
    ))
    story.append(Paragraph(
        "<b>B. PowerShell Session Execution Bypass:</b> Windows environments prevent unsigned local script execution by default. "
        "To start the environment safely without breaking overall OS security policies, the run wrapper targets process-scoped execution parameters:<br/>"
        "<code>Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process</code><br/>"
        "This drops constraints exclusively for the active PowerShell terminal window instance, reverting back to full system lock instantly upon closure.",
        styles['ReportBody']
    ))
    
    # ---------------------------------------------------------
    # SECTION 5: REVISION NOTES (KYA, KESE, KYU)
    # ---------------------------------------------------------
    story.append(Paragraph("5. Technical Revision Master Notes", styles['ReportHeading1']))
    
    notes_data = [
        ["Core Metric", "Architectural Execution Realities"],
        ["What Happened (Kya Hua)?", "The application was refactored from a messy prototype into clean packages. A unified intent router was injected to choose between local OS automation paths and cloud LLM execution branches dynamically."],
        ["How It Works (Kese Hua)?", "The engine continuously samples user speech token strings, cleans unwanted trigger text using string mutation methods, maps values using URI encoding patterns, and fires isolated execution targets."],
        ["Why This Way (Kyu Hua)?", "Maximizes module scalability. New automation wrappers (like filesystem file management, volume adjustment, desktop application tracking) can be dropped directly into the automation pack without changing the core engine code."]
    ]
    t2 = Table(notes_data, colWidths=[130, 374])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), BG_LIGHT),
        ('BACKGROUND', (0,0), (-1,0), BORDER_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t2)
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # SECTION 6: INTERVIEW PREPARATION COMPENDIUM
    # ---------------------------------------------------------
    story.append(Paragraph("6. Architectural Interview Compendium (Q&A)", styles['ReportHeading1']))
    story.append(Paragraph(
        "Below are production-level interview questions mapping directly to the architectural decisions made during this build cycle.",
        styles['ReportBody']
    ))
    
    qa_pairs = [
        ("Q1: Why did you partition your code into packages like 'ai', 'automation', and 'voice' instead of writing everything inside main.py?",
         "A: To implement clean separation of concerns and lower architectural coupling. Modular structures ensure regression isolation—meaning errors inside the audio capture module cannot crash or break independent cloud LLM wrappers. It also matches standard production practices, making it clean for multiple developers to scale features together."),
        
        ("Q2: What is the exact function of 'urllib.parse.quote_plus' in your automation logic, and what failure mode does it solve?",
         "A: It translates text strings with spaces and punctuation into valid URL-encoded patterns (converting spaces into '+' characters). Without it, passing user commands with spaces straight to system browsers creates malformed URI requests, which will cause browser routing failures and system-level exceptions."),
        
        ("Q3: Explain how the 'continue' keyword affects token costs in your system routing structure.",
         "A: The <code>continue</code> statement stops further downward processing inside our execution block. If a command matches a local automation task (e.g., opening YouTube), the system processes it and jumps straight back to start a new command capture cycle. This blocks the string from hitting the cloud generative AI endpoints, saving API costs and avoiding extra latency."),
        
        ("Q4: Why use process-scoped execution policies instead of changing your global system parameters?",
         "A: Changing system policies globally (via <code>Unrestricted</code>) permanently exposes a Windows system to high-risk malware scripts. Using <code>-Scope Process</code> bypasses authorization policies exclusively for that specific terminal process window instance, keeping the rest of the OS completely locked down and safe."),
         
        ("Q5: If you push your workspace to public GitHub repos, how do you protect corporate or secret API keys?",
         "A: By configuring a strict <code>.gitignore</code> manifest entry matching our environment environment registry (<code>.env</code>). This keeps local key configurations unindexed on our machines, ensuring we only push reusable, clean framework architecture code and never compromise live deployment tokens.")
    ]
    
    for q, a in qa_pairs:
        story.append(Paragraph(f"<b>{q}</b>", styles['ReportBody']))
        story.append(Paragraph(a, styles['ReportBody']))
        story.append(Spacer(1, 6))
        
    # Build Document using our custom canvas tracker
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    build_pdf()
    print("Success: 'Jarvis_Project_Report.pdf' has been generated in your workspace directory!")