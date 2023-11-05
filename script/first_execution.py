import subprocess
import time
comando = "pip install PyMuPDF"
comando1 = "pip install pyzbar"
comando5="pip install Pillow"
comando6="pip install PyMuPDF qrcode opencv-python"
comando7="pip install selenium-2captcha-solver"

try:
    subprocess.call(comando, shell=True)
    print("installing PyMuPDF")
    subprocess.call(comando1, shell=True)
    print("installing pyzbar")
    subprocess.call(comando5,shell=True)
    print("installing  Pillow")
    subprocess.call(comando6,shell=True)
    print("installing qr code ")
    subprocess.call(comando7,shell=True)
    print("installing undetected-chrome driver ")
    time.sleep(1)
    print("Dependencies installed correctly.")
except subprocess.CalledProcessError as e:
    print("Error  installing all dependencies:", e)


