from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(name, score, total):
    doc = SimpleDocTemplate("attestation.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph(f"Étudiant: {name}", styles["Title"]))
    content.append(Paragraph(f"Score: {score}/{total}", styles["Normal"]))

    doc.build(content)
    return "attestation.pdf"