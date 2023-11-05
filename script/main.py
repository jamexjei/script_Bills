# -----------------------------imports ------------------------------
import subprocess
import time
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium_recaptcha_solver import RecaptchaSolver
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
# --------------------------imports ---------------------------------

#--------------------customizable area -----------------------------
poppler_path = "../poppler/bin"                                     #
pdf_folder = "../invoice_upload"                                    #
image_folder = "../invoice_images"                                  #
route_txt = '../Not processed/log.txt'                              #
username = "auxfacturacion@ayura.co"                                #
password = "4Kqx/v&$nv7W+7#"                                        #
#--------------------customizable area -----------------------------

#------------------- options chrome driver -------------------------
extension_path = '../extension/buster_captcha_resolver.crx'
options = webdriver.ChromeOptions()
options.add_extension(extension_path)#
options.add_argument('--no-sandbox')                                #
options.add_argument("--enable-extensions")                        #
list_facturas=[]                                                    #
today=datetime.datetime.now()                                       #
# -------------------options chrome driver -------------------------


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
        
        x, y = 3, 3
        sw=0
        img_path = os.path.join(image_folder, img_file)
        img = cv2.imread(img_path)
        percentage=10
        loading=f" loading {percentage}%"
        data={}
        itera=''
        while x < 7 and y < 7:
            
            scaled_image = cv2.resize(img, None, fx=x, fy=y, interpolation=cv2.INTER_CUBIC)
            retval, decoded_info, points, straight_qrcode = det.detectAndDecodeMulti(scaled_image)
            
            if len(decoded_info) > 0 and decoded_info[0]!='':
                itera=decoded_info[0]
                sw=1    
                print(f"Código QR encontrado en {img_file} ")
                print("----------------------------")
                lineas = itera.strip().split('\n')


                data = {}


                for linea in lineas:
                    if ':' in linea:
                        clave, valor = re.split(r':', linea, maxsplit=1)
                        data[clave] = valor
                    else:
        
                        data["URL"] = linea


                json_data = json.dumps(data, indent=4)
                list_facturas.append(json_data)

                x=1
                y=1
                break

            x += 3
            y += 3
            
            
            
        if sw==0:
            print("usando metodo 2 de deteccion")
            data, bbox, straight_qrcode = det.detectAndDecode(img)
            if len(data)>0 and data[0]!='':
                print(f"Código QR encontrado en {img_file} ")
                print("----------------------------")
                print(data)
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
                            lineas = x.code_text.strip().split('\n')

                            data = {}


                            for linea in lineas:
                                if ':' in linea:
                                    clave, valor = re.split(r':', linea, maxsplit=1)
                                    data[clave] = valor
      
                                    data["URL"] = linea


                            json_data = json.dumps(data, indent=4)

                            list_facturas.append(json_data)
                            
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



# ---------------------------------main class ------------------------------------------------------------------------------
class FacturasBot:
    print("comienza proceso de facturas")
    def __init__(self, username, password):
        self.username = username
        self.password = password
             
        chromedriver_path = '../chromedriver.exe'

        # Configura el servicio de ChromeDriver
        chrome_service = webdriver.chrome.service.Service(executable_path=chromedriver_path,chrome_options=options)

        # Inicializa el controlador de Chrome
        self.driver = webdriver.Chrome(service=chrome_service)
        self.driver.maximize_window()
        
#-------------------------- function login and resolve captcha -------------------
    def login(self):
        self.driver.get("https://cenf.cen.biz/site/")
        time.sleep(4)
        print("Sign in ")
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys(self.username)

        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(self.password)
        
        #self.driver.switch_to.frame(0)
        time.sleep(1)
        recaptcha_iframe = self.driver.find_element(By.XPATH, '//*[@id="captcha_paragraph"]/div/div/div/iframe')
        time.sleep(2)
        solver = RecaptchaSolver(driver=self.driver)
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        
        time.sleep(4)
        self.driver.switch_to.default_content()
        password_input.send_keys(Keys.ENTER)
        
        print("Sign in successfully!!")
# -------------------------end function ---------------------------------------------
#--------------------------end class ------------------------------------------------

#--------------------- call class and function area ---------------------------------
generate_pdf_to_image()                                                             #
find_and_decode_qr_codes()                                                          #
bot = FacturasBot(username, password)                                               #
bot.login()                                                                         #
#---------------------call class and function area ----------------------------------
