from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from modules.database import connect

def generate_pdf(filepath="static/report.pdf"):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT image, result, confidence, timestamp FROM violations")
    data = cur.fetchall()

    conn.close()

    doc = SimpleDocTemplate(filepath, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("iDetector Violation Report", styles['Title']))

    table_data = [["Image", "Result", "Confidence", "Time"]]

    for row in data:
        table_data.append([
            row[0],
            row[1],
            f"{row[2]:.2f}",
            row[3]
        ])

    table = Table(table_data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ]))

    elements.append(table)

    doc.build(elements)

    return filepath