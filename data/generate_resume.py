import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "resume.json")
    pdf_path = os.path.join(script_dir, "resume.pdf")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)["candidate"]

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    header_name = ParagraphStyle(
        'HeaderName',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        fontName='Helvetica-Bold',
        spaceAfter=2
    )
    
    header_title = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#D97706'),
        fontName='Helvetica-Bold',
        spaceAfter=4
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#475569')
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        fontName='Helvetica-Bold',
        spaceBefore=8,
        spaceAfter=3
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1E293B')
    )
    
    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        spaceAfter=2
    )

    story = []

    # Name and Title
    story.append(Paragraph(data["name"], header_name))
    story.append(Paragraph(data["title"], header_title))
    
    # Contact info line
    contact_line = f"Email: <b>{data['email']}</b> | Phone: <b>{data['phone']}</b> | Location: <b>{data['location']}</b><br/>LinkedIn: <b>{data['linkedin']}</b> | GitHub: <b>{data['github']}</b>"
    story.append(Paragraph(contact_line, contact_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#D97706'), spaceBefore=2, spaceAfter=6))

    # Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    story.append(Paragraph(data["summary"], body_style))
    story.append(Spacer(1, 4))

    # Core Skills
    story.append(Paragraph("TECHNICAL EXPERTISE", section_heading))
    skills = data["skills"]
    skills_text = (
        f"<b>Languages:</b> {', '.join(skills['programming_languages'])}<br/>"
        f"<b>Frameworks & Backend:</b> {', '.join(skills['frameworks_and_backend'])}<br/>"
        f"<b>AI & Autonomous Agents:</b> {', '.join(skills['ai_and_agents'])}<br/>"
        f"<b>DevOps & Protocols:</b> {', '.join(skills['devops_and_tools'])}"
    )
    story.append(Paragraph(skills_text, body_style))
    story.append(Spacer(1, 4))

    # Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))
    for exp in data["experience"]:
        exp_header = f"<b>{exp['role']}</b> — <i>{exp['company']}</i> <font color='#64748B'>({exp['period']})</font>"
        story.append(Paragraph(exp_header, body_style))
        for h in exp["highlights"]:
            story.append(Paragraph(f"• {h}", bullet_style))
        story.append(Spacer(1, 3))

    # Projects
    story.append(Paragraph("FEATURED PROJECTS", section_heading))
    for proj in data["projects"]:
        proj_header = f"<b>{proj['name']}</b> | <font color='#D97706'>{', '.join(proj['technologies'])}</font>"
        story.append(Paragraph(proj_header, body_style))
        story.append(Paragraph(f"• {proj['description']}", bullet_style))
        story.append(Spacer(1, 3))

    # Education
    story.append(Paragraph("EDUCATION", section_heading))
    for edu in data["education"]:
        edu_header = f"<b>{edu['degree']}</b> — {edu['institution']} ({edu['graduation_year']}) — GPA: <b>{edu['gpa']}</b>"
        story.append(Paragraph(edu_header, body_style))

    doc.build(story)
    print(f"✓ Generated resume PDF successfully at: {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
