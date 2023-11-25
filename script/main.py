# -----------------------------imports ------------------------------
import subprocess
import time
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import os
from pdf2image import convert_from_path
import cv2
import aspose.barcode as barcode
import json
import re
import datetime
from datetime import datetime,timedelta
# --------------------------imports ---------------------------------

#--------------------customizable area -----------------------------
poppler_path = "../poppler/bin"                                     #
pdf_folder = "../invoice_upload"                                    #
image_folder = "../invoice_images"                                  #
route_txt = '../Not processed/log.txt'                              #
username = "auxfacturacion@ayura.co"                                #
password = "4Kqx/v&$nv7W+7#"                                        #
#--------------------customizable area -----------------------------

list_facturas=[]
today=datetime.now()
#-------------------- function generate pdf to image -----------------------
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
#-------------------end function ----------------------------------------------
    
# ------------------function decode qr -----------------------------------------
def find_and_decode_qr_codes():
    for img_file in os.listdir(image_folder):
        
        x=2
        y=2
        img_path = os.path.join(image_folder, img_file)
        #img = Image.open(img_path)
        img = cv2.imread(img_path)
        det = cv2.QRCodeDetector()
        

    for img_file in os.listdir(image_folder):
        print(f"procesando--> {img_file} ")
        print(f"decodificando QR... {img_file}")
        
        x, y = 2, 2
        sw=0
        img_path = os.path.join(image_folder, img_file)
        img = cv2.imread(img_path)
        percentage=10
        loading=f" loading {percentage}%"
        data={}
        itera=''
        while x < 10 and y < 10:
            
            scaled_image = cv2.resize(img, None, fx=x, fy=y, interpolation=cv2.INTER_CUBIC)
            retval, decoded_info, points, straight_qrcode = det.detectAndDecodeMulti(scaled_image)
            
            if len(decoded_info) > 0 and decoded_info[0]!='':
                itera=decoded_info[0]
                sw=1    
                print(f"Código QR encontrado en {img_file} ")
                print("----------------------------")
                lineas = itera.strip().split('\n')


                list_facturas.append(decoded_info)

                x=2
                y=2
                break

            x += 2
            y += 2
            
            
            
        if sw==0:
            print("usando metodo 2 de deteccion")
            data, bbox, straight_qrcode = det.detectAndDecode(img)
            if len(data)>0 and data[0]!='':
                print(f"Código QR encontrado en {img_file} ")
                print("----------------------------")
                list_facturas.append(data[0])
            else:
                print("usando metodo 3 de deteccion")
                reader = barcode.barcoderecognition.BarCodeReader(img_path)
                reader.quality_settings.read_tiny_barcodes = True
                reader.quality_settings.allow_incorrect_barcodes = True
                reader.quality_settings.allow_qr_micro_qr_restoration = True
                recognized_results = reader.read_bar_codes()
                if len (recognized_results)>0:
                    print(f"Código QR encontrado en {img_file} ")
                    print("----------------------------")
                    for x in recognized_results:
                        if x.code_text !='':
                           
                            list_facturas.append(x.code_text)
                            
                        break
                else:
                    new_data=f"el archivo{img_file} no fue procesado con exito ya que tiene un QR no legible el dia {today}"
                    with open(route_txt, "a") as archivo:
                        print("write in file")
                        archivo.write(new_data + "\n")
                    print(f"no se encontro QR para {img_file}")
                    print("----------------------------")
            
    for img_file in os.listdir(image_folder):
        img_path = os.path.join(image_folder, img_file)
        os.remove(img_path)
        qr_codes = []
    return qr_codes


#---------------------------------- end function ----------------------------------------------------------------------------


# -------------------------end function ---------------------------------------------
#--------------------------end class ------------------------------------------------

#--------------------- call class and function area ---------------------------------
generate_pdf_to_image()                                                             #
find_and_decode_qr_codes()                                                          #
result = []

def extract_num_fac_nit_fac(text):
    num_fac = None
    nit_fac = None
    fec_fac=None
    lines = text.split('\n')
    for line in lines:
        if 'NumFac:' in line:
            num_fac = line.split('NumFac:')[1].strip()
        if 'NitFac:' in line:
            nit_fac = line.split('NitFac:')[1].strip()
        if 'FecFac' in line:
            fec_fac = line.split('FecFac:')[1].strip()
            
    
    if num_fac and nit_fac and fec_fac:
        return {'NumFac': num_fac, 'NitFac': nit_fac,'FecFac':fec_fac}
    elif num_fac:
        return {'NumFac': num_fac, 'NitFac': None,'FecFac':None}
    elif nit_fac:
        return {'NumFac': None, 'NitFac': nit_fac,'FecFac':None}
    else:
        return None

for item in list_facturas:
    if isinstance(item, (str, tuple, list)):
        if isinstance(item, (list, tuple)):
            for sub_item in item:
                if isinstance(sub_item, str):
                    result_item = extract_num_fac_nit_fac(sub_item)
                    if result_item:
                        result.append(result_item)
        elif isinstance(item, str):
            result_item = extract_num_fac_nit_fac(item)
            if result_item:
                result.append(result_item)




def convertir_a_formato_correcto(fecha_str):
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
        return fecha_obj.strftime('%Y-%m-%d')
    except ValueError:
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y%m%d')
            return fecha_obj.strftime('%Y-%m-%d')
        except ValueError:
            print(f"Error: La fecha {fecha_str} no tiene el formato esperado (YYYY-MM-DD o YYYYMMDD)")
            return None

def encontrar_fechas_mayor_y_menor(diccionarios):
    fechas = [diccionario['FecFac'] for diccionario in diccionarios]

    fechas_obj = []
    for fecha in fechas:
        fecha_convertida = convertir_a_formato_correcto(fecha)
        if fecha_convertida:
            fechas_obj.append(datetime.strptime(fecha_convertida, '%Y-%m-%d'))

    if not fechas_obj:
        print("No hay fechas válidas en la lista.")
        return None, None

    fecha_mayor = max(fechas_obj).strftime('%Y-%m-%d')
    fecha_menor = min(fechas_obj).strftime('%Y-%m-%d')

    return fecha_mayor, fecha_menor



# Encontrar fecha mayor y fecha menor
fecha_mayor, fecha_menor = encontrar_fechas_mayor_y_menor(result)

# Mostrar resultados



def obtener_rango_mes(fecha):
    fecha_datetime = datetime.strptime(fecha, '%Y-%m-%d')
    primer_dia_mes = fecha_datetime.replace(day=1)
    ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    return primer_dia_mes.strftime('%Y/%m/%d'), ultimo_dia_mes.strftime('%Y/%m/%d')

# Procesar la lista de diccionarios
for item in result:
    if 'FecFac' in item:
        fecha_inicial, fecha_final = obtener_rango_mes(item['FecFac'])
        item['fecha_ini'] = fecha_inicial
        item['fecha_fin'] = fecha_final
print(result)
#---------------------call class and function area ----------------------------------

