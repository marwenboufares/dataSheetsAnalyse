import os
import fitz  # Importer PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Définir un style pour les titres des PDF
title_style = getSampleStyleSheet()['Heading1'].clone('TitleStyle')
title_style.textColor = colors.red

def extract_description(pdf_path):
    # Fonction pour extraire la description d'un PDF
    doc = fitz.open(pdf_path)
    description = None
    for page in doc:
        text = page.get_text()
        if "Description" in text:
            description = text.split("Description", 1)[1].strip()
            break
    return description if description else "Description not found"

def generate_output_pdf(pdf_folder, output_file):
    # Fonction pour générer le PDF de sortie avec toutes les descriptions
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    description_list = []

    # Supprimer le fichier de sortie s'il existe déjà
    if os.path.exists(output_file):
        os.remove(output_file)

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            # Ignorer le PDF généré
            if pdf_file == output_file:
                continue
            pdf_path = os.path.join(pdf_folder, pdf_file)
            description = extract_description(pdf_path)
            description_list.append((pdf_file, description))

    elements = []
    for index, (pdf_file, description) in enumerate(description_list, start=1):
        elements.append(Paragraph(f"{index}. ", title_style))  # Titre PDF en rouge
        elements.append(Paragraph(pdf_file, styles['Normal']))  # Titre PDF
        elements.append(Paragraph(description, styles['Normal']))  # Description
        elements.append(Paragraph("<br/><br/>", styles['Normal']))  # Retour à la ligne
        elements.append(Paragraph("<br/><br/>", styles['Normal']))  # Saut de ligne

    doc.build(elements)


def main(input_folder, output_file):
    # Fonction principale pour parcourir tous les PDF dans un dossier et générer le PDF de sortie
    generate_output_pdf(input_folder, output_file)

# Utilisation
if __name__ == "__main__":
    input_folder = "C:\\Users\\mboufares\\Desktop\\datasheet"
    output_file = "descriptionExtracted.pdf"
    main(input_folder, output_file)
