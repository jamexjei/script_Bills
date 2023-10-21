import subprocess
import time
comando = "pip install PyMuPDF"
comando1 = "pip install pyzbar"
comando5="pip install Pillow"
comando6="pip install PyMuPDF qrcode opencv-python"
try:
    subprocess.call(comando, shell=True)
    print("installing PyMuPDF")
    subprocess.call(comando1, shell=True)
    print("installing pyzbar")
    subprocess.call(comando5,shell=True)
    print("installing  Pillow")
    subprocess.call(comando6,shell=True)
    print("installing qr code ")
    time.sleep(1)
    
    print("Dependencies installed correctly.")
except subprocess.CalledProcessError as e:
    print("Error  installing all dependencies:", e)
    
  

from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from pdf2image import convert_from_path
import cv2
poppler_path = "../poppler/bin"
pdf_folder = "../invoice_upload"
image_folder = "../invoice_images"

def generate_pdf_to_image():
    os.makedirs(image_folder, exist_ok=True)

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            image_pages = convert_from_path(pdf_path, poppler_path=poppler_path)

            for page_num, image in enumerate(image_pages):
                image_name = f"{pdf_file}_{page_num + 1}.png"
                image_path = os.path.join(image_folder, image_name)
                image.save(image_path, "PNG")

    print("PDFs convertidos en imágenes")


def find_and_decode_qr_codes():
    for img_file in os.listdir(image_folder):
        
        x=2
        y=2
        img_path = os.path.join(image_folder, img_file)
        #img = Image.open(img_path)
        img = cv2.imread(img_path)
        det = cv2.QRCodeDetector()
        x, y = 1, 1

    for img_file in os.listdir(image_folder):
        img_path = os.path.join(image_folder, img_file)
        img = cv2.imread(img_path)

        while x < 20 and y < 20:
            scaled_image = cv2.resize(img, None, fx=x, fy=y, interpolation=cv2.INTER_CUBIC)
            retval, decoded_info, points, straight_qrcode = det.detectAndDecodeMulti(scaled_image)

            if len(decoded_info) > 0 and decoded_info!="'',":
                print(f"Código QR encontrado en {img_file} a escala {x} x {y}")
                print(decoded_info)
                x=1
                y=1
                break

            x += 2
            y += 2
            print(f"Escala actual: {x} x {y}")
    for img_file in os.listdir(image_folder):
        img_path = os.path.join(image_folder, img_file)
        os.remove(img_path)
        qr_codes = []
    return qr_codes



generate_pdf_to_image()
find_and_decode_qr_codes()
