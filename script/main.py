import subprocess
import time
comando = "pip install pandas"
comando1 = "pip install selenium"
comando5="pip install PyMuPDF qrcode opencv-python"
try:
    subprocess.call(comando, shell=True)
    print("installing pandas")
    subprocess.call(comando1, shell=True)
    print("installing selenium")
    print("installing  pillow")
    subprocess.call(comando5,shell=True)
    print("installing  pdf2image")
    time.sleep(1)
    print("Dependencies installed correctly.")
except subprocess.CalledProcessError as e:
    print("Error  installing all dependencies:", e)
    
import os    

from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import fitz  # PyMuPDF
import qrcode
import io
from PIL import Image

import fitz  # PyMuPDF
import cv2
import qrcode

def extract_qr_codes_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    qr_codes = []

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_data = base_image["image"]

            # Guarda la imagen en un archivo temporal
            with open(f'temp_image_{page_number}_{img_index}.jpg', 'wb') as temp_image:
                temp_image.write(image_data)

            # Cargamos la imagen con OpenCV para procesarla
            image = cv2.imread(f'temp_image_{page_number}_{img_index}.jpg')

            # Utilizamos un detector de QR para encontrar el código QR en la imagen
            detector = cv2.QRCodeDetector()
            scaled_image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            
            retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(scaled_image)
            print(decoded_info)
            if retval:
                qr_codes.extend(decoded_info)

    pdf_document.close()

    return qr_codes

def process_pdf_files_in_folder(folder_path):
    folder_path = os.path.abspath(folder_path)

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name.endswith('.pdf'):
            qr_codes = extract_qr_codes_from_pdf(file_path)
        
            print(len(qr_codes))
            for qr_code in qr_codes:
                print(f'Código QR encontrado en {file_name}: {qr_code}')

# Carpeta que contiene los archivos PDF
input_folder = "../invoice_upload"

# Procesa archivos PDF en la carpeta
process_pdf_files_in_folder(input_folder)

def find_and_decode_qr_codes():
    for img_file in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_file)
        #img = Image.open(img_path)
        img = cv2.imread(img_path)
        det = cv2.QRCodeDetector()
        valorQRLeido, box_coordinates, st_code = det.detectAndDecode(img)
        if box_coordinates is  None:
            print("no hay codigo qr en la imagen")
               
        else:
            print("El valor del QR leído es: ", valorQRLeido)
    for img_file in os.listdir(image_folder):
        img_path = os.path.join(image_folder, img_file)
        os.remove(img_path)
        qr_codes = []
    return qr_codes

folder_path = "../invoice_upload"
# Define la función para leer datos desde un archivo Excel


