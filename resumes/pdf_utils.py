from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
import io

NAVY = colors.HexColor('#0d1b2a')
SAFFRON = colors.HexColor('#f5a623')
DARK_GRAY = colors.HexColor('#2d3748')
GRAY = colors.HexColor('#718096')
LIGHT_GRAY = colors.HexColor('#f7f8fa')
WHITE = colors.white
BLACK = colors.black


def generate_resume_pdf(resume):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    template = resume.template
    if template == 'modern':
        story = build_modern_template(resume)
    elif template == 'minimal':
        story = build_minimal_template(resume)
    elif template == 'executive':
        story = build_executive_template(resume)
    else:
        story = build_classic_template(resume)

    doc.build(story)
    buffer.seek(0)
    return buffer


def build_classic_template(resume):
    story = []
    styles = getSampleStyleSheet()

    name_style = ParagraphStyle('Name', fontName='Helvetica-Bold', fontSize=24, textColor=NAVY, spaceAfter=2, alignment=TA_CENTER)
    title_style = ParagraphStyle('Title', fontName='Helvetica', fontSize=13, textColor=SAFFRON, spaceAfter=4, alignment=TA_CENTER)
    contact_style = ParagraphStyle('Contact', fontName='Helvetica', fontSize=9, textColor=DARK_GRAY, spaceAfter=2, alignment=TA_CENTER)
    section_style = ParagraphStyle('Section', fontName='Helvetica-Bold', fontSize=11, textColor=NAVY, spaceBefore=10, spaceAfter=3, borderPad=2)
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=9, textColor=DARK_GRAY, spaceAfter=3, leading=13)
    bullet_style = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=9, textColor=DARK_GRAY, spaceAfter=2, leftIndent=12, leading=13)
    subhead_style = ParagraphStyle('Subhead', fontName='Helvetica-Bold', fontSize=10, textColor=DARK_GRAY, spaceAfter=1)
    meta_style = ParagraphStyle('Meta', fontName='Helvetica-Oblique', fontSize=9, textColor=GRAY, spaceAfter=2)

    # Header
    story.append(Paragraph(resume.full_name or 'Your Name', name_style))
    if resume.job_title:
        story.append(Paragraph(resume.job_title, title_style))

    # Contact line
    contact_parts = []
    if resume.email: contact_parts.append(resume.email)
    if resume.phone: contact_parts.append(resume.phone)
    if resume.location: contact_parts.append(resume.location)
    if resume.linkedin: contact_parts.append(resume.linkedin)
    if contact_parts:
        story.append(Paragraph(' | '.join(contact_parts), contact_style))

    story.append(HRFlowable(width="100%", thickness=2, color=SAFFRON, spaceAfter=8))

    # Summary
    if resume.summary:
        story.append(Paragraph('PROFESSIONAL SUMMARY', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceAfter=4))
        story.append(Paragraph(resume.summary, body_style))

    # Experience
    exp_list = resume.get_experience()
    if exp_list:
        story.append(Paragraph('WORK EXPERIENCE', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceAfter=4))
        for exp in exp_list:
            role_company = f"<b>{exp.get('role','')}</b> — {exp.get('company','')}"
            story.append(Paragraph(role_company, subhead_style))
            if exp.get('dates'):
                story.append(Paragraph(exp['dates'], meta_style))
            desc = exp.get('description', '')
            if desc:
                for line in desc.split('\n'):
                    line = line.strip()
                    if line:
                        if line.startswith('•') or line.startswith('-'):
                            story.append(Paragraph(f"• {line.lstrip('•-').strip()}", bullet_style))
                        else:
                            story.append(Paragraph(f"• {line}", bullet_style))
            story.append(Spacer(1, 4))

    # Education
    edu_list = resume.get_education()
    if edu_list:
        story.append(Paragraph('EDUCATION', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceAfter=4))
        for edu in edu_list:
            story.append(Paragraph(f"<b>{edu.get('school','')}</b>", subhead_style))
            deg_year = edu.get('degree', '')
            if edu.get('year'): deg_year += f" | {edu['year']}"
            if edu.get('gpa'): deg_year += f" | GPA: {edu['gpa']}"
            story.append(Paragraph(deg_year, meta_style))

    # Skills
    skills = resume.get_skills()
    if skills:
        story.append(Paragraph('SKILLS', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceAfter=4))
        story.append(Paragraph(', '.join(skills), body_style))

    # Projects
    proj_list = resume.get_projects()
    if proj_list:
        story.append(Paragraph('PROJECTS', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceAfter=4))
        for p in proj_list:
            pname = p.get('name', '')
            if p.get('url'): pname += f" ({p['url']})"
            story.append(Paragraph(f"<b>{pname}</b>", subhead_style))
            if p.get('description'):
                story.append(Paragraph(p['description'], body_style))

    # Certifications
    cert_list = resume.get_certifications()
    if cert_list:
        story.append(Paragraph('CERTIFICATIONS', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceAfter=4))
        for c in cert_list:
            cert_text = f"<b>{c.get('name','')}</b>"
            if c.get('issuer'): cert_text += f" — {c['issuer']}"
            if c.get('date'): cert_text += f" ({c['date']})"
            story.append(Paragraph(cert_text, body_style))

    return story


def build_modern_template(resume):
    story = []
    name_style = ParagraphStyle('Name', fontName='Helvetica-Bold', fontSize=26, textColor=WHITE, spaceAfter=2, alignment=TA_LEFT)
    title_style = ParagraphStyle('Title', fontName='Helvetica', fontSize=13, textColor=SAFFRON, spaceAfter=4)
    contact_style = ParagraphStyle('Contact', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor('#cbd5e0'), spaceAfter=2)
    section_style = ParagraphStyle('Section', fontName='Helvetica-Bold', fontSize=10, textColor=SAFFRON, spaceBefore=10, spaceAfter=3, letterSpacing=1)
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=9, textColor=DARK_GRAY, spaceAfter=3, leading=13)
    bullet_style = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=9, textColor=DARK_GRAY, spaceAfter=2, leftIndent=12, leading=13)
    subhead_style = ParagraphStyle('Subhead', fontName='Helvetica-Bold', fontSize=10, textColor=DARK_GRAY, spaceAfter=1)
    meta_style = ParagraphStyle('Meta', fontName='Helvetica-Oblique', fontSize=8.5, textColor=GRAY, spaceAfter=2)

    # Header block with navy background simulation via table
    header_data = [[Paragraph(resume.full_name or 'Your Name', name_style)]]
    if resume.job_title:
        header_data.append([Paragraph(resume.job_title, title_style)])
    contact_parts = []
    if resume.email: contact_parts.append(resume.email)
    if resume.phone: contact_parts.append(resume.phone)
    if resume.location: contact_parts.append(resume.location)
    if contact_parts:
        header_data.append([Paragraph('  •  '.join(contact_parts), contact_style)])

    header_table = Table(header_data, colWidths=[18*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('PADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 18),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 16),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    if resume.summary:
        story.append(Paragraph('PROFESSIONAL SUMMARY', section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=SAFFRON, spaceAfter=5))
        story.append(Paragraph(resume.summary, body_style))

    exp_list = resume.get_experience()
    if exp_list:
        story.append(Paragraph('EXPERIENCE', section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=SAFFRON, spaceAfter=5))
        for exp in exp_list:
            story.append(Paragraph(f"<b>{exp.get('role','')}</b> | {exp.get('company','')}", subhead_style))
            if exp.get('dates'): story.append(Paragraph(exp['dates'], meta_style))
            for line in (exp.get('description') or '').split('\n'):
                line = line.strip()
                if line: story.append(Paragraph(f"• {line.lstrip('•-').strip()}", bullet_style))
            story.append(Spacer(1, 4))

    edu_list = resume.get_education()
    if edu_list:
        story.append(Paragraph('EDUCATION', section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=SAFFRON, spaceAfter=5))
        for edu in edu_list:
            story.append(Paragraph(f"<b>{edu.get('school','')}</b>", subhead_style))
            deg = edu.get('degree','')
            if edu.get('year'): deg += f" | {edu['year']}"
            story.append(Paragraph(deg, meta_style))

    skills = resume.get_skills()
    if skills:
        story.append(Paragraph('SKILLS', section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=SAFFRON, spaceAfter=5))
        skill_text = '   •   '.join(skills)
        story.append(Paragraph(skill_text, body_style))

    proj_list = resume.get_projects()
    if proj_list:
        story.append(Paragraph('PROJECTS', section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=SAFFRON, spaceAfter=5))
        for p in proj_list:
            story.append(Paragraph(f"<b>{p.get('name','')}</b>", subhead_style))
            if p.get('description'): story.append(Paragraph(p['description'], body_style))

    cert_list = resume.get_certifications()
    if cert_list:
        story.append(Paragraph('CERTIFICATIONS', section_style))
        story.append(HRFlowable(width="100%", thickness=1, color=SAFFRON, spaceAfter=5))
        for c in cert_list:
            txt = f"<b>{c.get('name','')}</b>"
            if c.get('issuer'): txt += f" — {c['issuer']}"
            if c.get('date'): txt += f" ({c['date']})"
            story.append(Paragraph(txt, body_style))

    return story


def build_minimal_template(resume):
    story = []
    name_style = ParagraphStyle('Name', fontName='Helvetica-Bold', fontSize=22, textColor=BLACK, spaceAfter=2, alignment=TA_LEFT)
    title_style = ParagraphStyle('Title', fontName='Helvetica', fontSize=11, textColor=GRAY, spaceAfter=4)
    contact_style = ParagraphStyle('Contact', fontName='Helvetica', fontSize=9, textColor=GRAY, spaceAfter=6)
    section_style = ParagraphStyle('Section', fontName='Helvetica-Bold', fontSize=10, textColor=BLACK, spaceBefore=12, spaceAfter=4, letterSpacing=2)
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=9, textColor=DARK_GRAY, spaceAfter=3, leading=14)
    bullet_style = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=9, textColor=DARK_GRAY, spaceAfter=2, leftIndent=10, leading=13)
    subhead_style = ParagraphStyle('Subhead', fontName='Helvetica-Bold', fontSize=9.5, textColor=BLACK, spaceAfter=1)
    meta_style = ParagraphStyle('Meta', fontName='Helvetica', fontSize=8.5, textColor=GRAY, spaceAfter=2)

    story.append(Paragraph(resume.full_name or 'Your Name', name_style))
    if resume.job_title: story.append(Paragraph(resume.job_title, title_style))
    parts = [x for x in [resume.email, resume.phone, resume.location] if x]
    if parts: story.append(Paragraph(' | '.join(parts), contact_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=6))

    if resume.summary:
        story.append(Paragraph('SUMMARY', section_style))
        story.append(Paragraph(resume.summary, body_style))

    exp_list = resume.get_experience()
    if exp_list:
        story.append(Paragraph('EXPERIENCE', section_style))
        for exp in exp_list:
            story.append(Paragraph(f"<b>{exp.get('role','')}</b>, {exp.get('company','')}", subhead_style))
            if exp.get('dates'): story.append(Paragraph(exp['dates'], meta_style))
            for line in (exp.get('description') or '').split('\n'):
                line = line.strip()
                if line: story.append(Paragraph(f"– {line.lstrip('•-').strip()}", bullet_style))
            story.append(Spacer(1, 4))

    edu_list = resume.get_education()
    if edu_list:
        story.append(Paragraph('EDUCATION', section_style))
        for edu in edu_list:
            story.append(Paragraph(f"<b>{edu.get('school','')}</b> — {edu.get('degree','')} {edu.get('year','')}", body_style))

    skills = resume.get_skills()
    if skills:
        story.append(Paragraph('SKILLS', section_style))
        story.append(Paragraph(', '.join(skills), body_style))

    proj_list = resume.get_projects()
    if proj_list:
        story.append(Paragraph('PROJECTS', section_style))
        for p in proj_list:
            story.append(Paragraph(f"<b>{p.get('name','')}</b>", subhead_style))
            if p.get('description'): story.append(Paragraph(p['description'], body_style))

    cert_list = resume.get_certifications()
    if cert_list:
        story.append(Paragraph('CERTIFICATIONS', section_style))
        for c in cert_list:
            txt = f"{c.get('name','')} — {c.get('issuer','')} {c.get('date','')}"
            story.append(Paragraph(txt, body_style))

    return story


def build_executive_template(resume):
    # Executive uses navy sidebar simulation with two-column table
    story = []
    name_style = ParagraphStyle('Name', fontName='Helvetica-Bold', fontSize=24, textColor=NAVY, spaceAfter=2)
    title_style = ParagraphStyle('Title', fontName='Helvetica', fontSize=12, textColor=SAFFRON, spaceAfter=6)
    section_style = ParagraphStyle('Section', fontName='Helvetica-Bold', fontSize=10, textColor=NAVY, spaceBefore=10, spaceAfter=3)
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=9, textColor=DARK_GRAY, spaceAfter=3, leading=13)
    bullet_style = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=9, textColor=DARK_GRAY, leftIndent=10, leading=13, spaceAfter=2)
    subhead_style = ParagraphStyle('Subhead', fontName='Helvetica-Bold', fontSize=10, textColor=DARK_GRAY, spaceAfter=1)
    meta_style = ParagraphStyle('Meta', fontName='Helvetica-Oblique', fontSize=8.5, textColor=GRAY, spaceAfter=3)
    sidebar_section = ParagraphStyle('SideSection', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE, spaceBefore=8, spaceAfter=3, letterSpacing=1)
    sidebar_body = ParagraphStyle('SideBody', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor('#cbd5e0'), spaceAfter=3, leading=13)

    story.append(Paragraph(resume.full_name or 'Your Name', name_style))
    if resume.job_title: story.append(Paragraph(resume.job_title, title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=SAFFRON, spaceAfter=10))

    # Left col (main) and Right col (sidebar)
    left = []
    right = []

    if resume.summary:
        left.append(Paragraph('EXECUTIVE SUMMARY', section_style))
        left.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceAfter=4))
        left.append(Paragraph(resume.summary, body_style))

    for exp in resume.get_experience():
        if not left or left[-1] != Paragraph('EXPERIENCE', section_style):
            left.append(Paragraph('EXPERIENCE', section_style))
            left.append(HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceAfter=4))
        left.append(Paragraph(f"<b>{exp.get('role','')}</b>", subhead_style))
        left.append(Paragraph(f"{exp.get('company','')} | {exp.get('dates','')}", meta_style))
        for line in (exp.get('description') or '').split('\n'):
            line = line.strip()
            if line: left.append(Paragraph(f"• {line.lstrip('•-').strip()}", bullet_style))
        left.append(Spacer(1, 4))

    # Sidebar: contact, skills, education, certs
    right.append(Paragraph('CONTACT', sidebar_section))
    for item in [resume.email, resume.phone, resume.location, resume.linkedin]:
        if item: right.append(Paragraph(item, sidebar_body))

    skills = resume.get_skills()
    if skills:
        right.append(Paragraph('SKILLS', sidebar_section))
        for s in skills:
            right.append(Paragraph(f"▸ {s}", sidebar_body))

    for edu in resume.get_education():
        right.append(Paragraph('EDUCATION', sidebar_section))
        right.append(Paragraph(f"<b>{edu.get('degree','')}</b>", ParagraphStyle('x', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE, spaceAfter=1)))
        right.append(Paragraph(f"{edu.get('school','')} {edu.get('year','')}", sidebar_body))

    for c in resume.get_certifications():
        right.append(Paragraph('CERTIFICATIONS', sidebar_section))
        right.append(Paragraph(f"{c.get('name','')} – {c.get('issuer','')}", sidebar_body))
        break

    # Build two-col table
    left_cells = [[item] for item in left]
    right_cells = [[item] for item in right]

    # Pad to same length
    max_len = max(len(left_cells), len(right_cells))
    while len(left_cells) < max_len: left_cells.append([Spacer(1, 1)])
    while len(right_cells) < max_len: right_cells.append([Spacer(1, 1)])

    table_data = [[left_cells[i][0], right_cells[i][0]] for i in range(max_len)]
    t = Table(table_data, colWidths=[12.5*cm, 5.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (1, 0), (1, -1), NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, -1), 14),
        ('LEFTPADDING', (1, 0), (1, -1), 12),
        ('RIGHTPADDING', (1, 0), (1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    return story
