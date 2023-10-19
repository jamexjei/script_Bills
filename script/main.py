import subprocess
comando = "pip install pandas"
comando1 = "pip install selenium"
comando2="pip install PyMuPDF qrcode"


try:
    subprocess.call(comando, shell=True)
    print("installing pandas")
    subprocess.call(comando1, shell=True)
    print("installing selenium")
    subprocess.call(comando2,shell=True)
    print("installing PyMuPDF qr code")
    print("Dependencies installed correctly.")
except subprocess.CalledProcessError as e:
    print("Error  installing all dependencies:", e)
    
import os    
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import fitz  # PyMuPDF
import qrcode
from io import BytesIO


def extract_images_from_pdf(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]
            images.append(image_data)
    return images

def find_and_decode_qr_codes(images):
    qr_codes = []
    for img_data in images:
        try:
            qr_code = qrcode.make(img_data)
            if qr_code.version <= 40:
                qr_data = qrcode.data.img_scan(qr_code)
                qr_codes.append(qr_data)
        except (qrcode.exceptions.DecodeError, AttributeError):
            pass
    return qr_codes

folder_path = "../invoice_upload"
# Define la función para leer datos desde un archivo Excel
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        print("Procesando factura:", pdf_path)
        
        # Extraer imágenes del PDF
        images = extract_images_from_pdf(pdf_path)

        # Buscar y decodificar códigos QR
        qr_codes = find_and_decode_qr_codes(images)

        # Imprimir los datos de los códigos QR encontrados
        for qr_code in qr_codes:
            print("Código QR encontrado en", pdf_path, ":", qr_code)


class InvoiceBot:
    pass
    #def __init__(self, username, password):
        #self.username = username
        #self.password = password
        #     # Establece la ubicación del ejecutable de ChromeDriver
        #chromedriver_path = './chromedriver.exe'
#
        ## Configura el servicio de ChromeDriver
        #chrome_service = webdriver.chrome.service.Service(executable_path=chromedriver_path)
#
        ## Inicializa el controlador de Chrome
        #self.driver = webdriver.Chrome(service=chrome_service)
        #self.driver.maximize_window()
#
    #def login(self):
    #    self.driver.get("https://www.instagram.com/")
    #    time.sleep(2)
    #    print("Sign in ")
    #    username_input = self.driver.find_element(By.NAME, "username")
    #    username_input.send_keys(self.username)
#
    #    password_input = self.driver.find_element(By.NAME, "password")
    #    password_input.send_keys(self.password)
#
    #    password_input.send_keys(Keys.ENTER)
    #    time.sleep(4)
    #    print("Sign in successfully!!")
    #def extract_followers(self, profile):
    #    self.driver.get(f"https://www.instagram.com/{profile}/followers")
    #    time.sleep(randint(2,4))
    #    followers_a = self.driver.find_elements(By.XPATH, '//div[@class="xt0psk2"]/div/a')
    #    followers=[follower.text for follower in followers_a]
    #    
    #    return followers
    
    
    #def interact_with_users(self, profile):
    #    time.sleep(randint(2,4))
    #    try:
    #        self.driver.get(f"https://www.instagram.com/{profile}")
    #        time.sleep(randint(2,4))
    #        self.like_story()
    #        time.sleep(randint(2,4))
    #        posts = self.driver.find_elements(By.XPATH, '//div[@class="_ac7v  _al3n"][1]/div/a')
    #        links = [post.get_attribute('href') for post in posts]
    #        for link in links:
    #            self.driver.get(link)
    #            try:
    #                like_post = self.driver.find_element(By.XPATH, '//div[@class="x6s0dn4 x78zum5 xdt5ytf xl56j7k"]/span')
    #                like_post.click()
    #            except:
    #                pass
    #    except:
    #        pass
    

    #def like_story(self):
    #    time.sleep(randint(2,4))
    #    try:
    #        story = self.driver.find_element(By.XPATH, '//div[@class="_aarf _aarg"]/span')
    #        story.click()
    #        time.sleep(2)
    #        like_button = self.driver.find_element(By.XPATH, '//div[@class="_abx4"]/span')
    #        like_button.click()
    #        time.sleep(2)
    #        close_btn = self.driver.find_element(By.XPATH, '//div[@class="xjbqb8w x1ypdohk xw7yly9 xktsk01 x1yztbdb x1d52u69 x10l6tqk x13vifvy xds687c"]/div/div')
    #        close_btn.click()
    #    except:
    #        pass
#
    #def run_bot(self, profile_list,histories,data_route):
    #    pass
    #    #iteraction = [self.interact_with_users(user) for user in users]
    #    self.driver.quit()

#Customizable Area
username = "cocina_facil5"  # Write your username here
password = "Salchipapa19"    # Write your password here
  # In this file, the script saves the last history from the user


#bot = InvoiceBot(username, password)
#bot.login()  # Llama al método de inicio de sesión antes de ejecutar el bot
#bot.run_bot()

#Okey, u need.
#and install selenium, but first install python, ok installed, run the script
