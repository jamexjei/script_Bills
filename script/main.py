from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import time, sleep

chrome_driver_path = './chromedriver' 
extension_path = './Extension.crx'  

username = 'auxfacturacion@ayura.co'
password = '4Kqx/v&$nv7W+7#'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

options.add_extension(extension_path)

driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

def ir_sitio():
    driver.get('https://cenf.cen.biz/site/')
    sleep(5)
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys(username)
    sleep(1.5)
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)

    sleep(25)
    btn_login = driver.find_element(By.ID,"button-login")
    btn_login.click()
    sleep(70)

ir_sitio()