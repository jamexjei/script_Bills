import subprocess
import time
comando = "pip install PyMuPDF"
comando1 = "pip install pyzbar"
comando5="pip install Pillow"
comando6="pip install pyzbar"
comando7="pip install aspose-barcode-for-python-via-net"

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
    print("installing aspose ")
    time.sleep(1)
    print("Dependencies installed correctly.")
except subprocess.CalledProcessError as e:
    print("Error  installing all dependencies:", e)


