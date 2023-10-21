import os
import fitz  # PyMuPDF
import qrcode

# Carpeta que contiene los archivos PDF
pdf_folder = './invoice_upload'

# Lee el contenido de una página del PDF
def extract_text_from_pdf(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    text = page.get_text()
    return text

# Genera un código QR y guarda la imagen
def generate_qr_code(pdf_content, output_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(pdf_content)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(output_path)

# Procesa todos los archivos PDF en la carpeta
for root, dirs, files in os.walk(pdf_folder):
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_path = os.path.join(root, file)

            pdf_reader = fitz.open(pdf_path)

            for page_num in range(pdf_reader.page_count):
                pdf_content = extract_text_from_pdf(pdf_path, page_num)
                print(f"Contenido de la página {page_num + 1} en '{pdf_path}':\n")
                print(pdf_content)
                print("\n" + "-" * 50 + "\n")

                # Genera un código QR para cada página y guarda la imagen
                qr_code_output = os.path.splitext(pdf_path)[0] + f'_page_{page_num + 1}_qr.png'
                generate_qr_code(pdf_content, qr_code_output)

                # Crear un PDF temporal para esta página
                temp_pdf = fitz.open()
                temp_pdf.insert_pdf(pdf_reader, from_page=page_num, to_page=page_num)
                temp_pdf_output = os.path.splitext(pdf_path)[0] + f'_page_{page_num + 1}.pdf'
                temp_pdf.save(temp_pdf_output)

print("Proceso completado.")
