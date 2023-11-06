import fitz  # PyMuPDF
import qrcode
from PIL import Image
import tempfile
import os

# Ruta al archivo PDF
pdf_file = './invoice_upload/Document_20230411_0001.pdf'

# Lee el contenido de una página del PDF
def extract_text_from_page(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    if page_num < doc.page_count:
        page = doc[page_num]
        text = page.get_text()
        return text

# Genera el código QR para una página específica y guarda la imagen
def generate_qr_for_page(pdf_path, page_num):
    text = extract_text_from_page(pdf_path, page_num)
    if text:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        return qr_img

# Guarda la imagen del código QR para cada página en archivos temporales
def save_qr_images_for_all_pages(pdf_path):
    doc = fitz.open(pdf_path)
    qr_images = []
    for page_num in range(doc.page_count):
        qr_img = generate_qr_for_page(pdf_path, page_num)
        if qr_img:
            # Crear un archivo temporal para la imagen del código QR
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                qr_img.save(temp_file.name)
                qr_images.append(temp_file.name)
    return qr_images

# Llama a la función para generar y guardar códigos QR por página
qr_image_files = save_qr_images_for_all_pages(pdf_file)

# Ahora puedes procesar cada página y su código QR correspondiente
for page_num, qr_image_file in enumerate(qr_image_files):
    print(f"Procesando página {page_num + 1} y su código QR:")
    text = extract_text_from_page(pdf_file, page_num)
    print(f"Contenido de la página:\n{text}")
    print(f"Ruta del archivo del código QR: {qr_image_file}")
    print("\n" + "-" * 50 + "\n")

# Limpia los archivos temporales de los códigos QR
