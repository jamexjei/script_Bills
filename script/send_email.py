import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import atexit
import sys
from datetime import datetime


today=datetime.now()
# Ruta de las imágenes
ruta_image = '../invoice_images'

# Nombre del archivo ZIP
nombre_zip = 'not_procesed.zip'

# Configuración del servidor SMTP de Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587



# Ruta de destino para el archivo ZIP
ruta_zip = '../invoice_images/' + nombre_zip

# Lista de archivos en la carpeta de imágenes
archivos = [os.path.join(ruta_image, archivo) for archivo in os.listdir(ruta_image) if os.path.isfile(os.path.join(ruta_image, archivo))]

# Crear el archivo ZIP
with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for archivo in archivos:
        zipf.write(archivo, os.path.basename(archivo))

# Configuración del correo electrónico
from_email = 'notificacionesayura@gmail.com'
password = 'nuua ucsk mpib gilv'  # Usa tu contraseña o contraseña específica de la aplicación
to_email = 'jamexjei@gmail.com' #correo destino 
subject = f'INVOICE NOT PROCESED {today}' #asunto
message = 'a continuacion encontramos las facturas no procesadas '#mensaje

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

# Adjuntar el archivo ZIP al correo electrónico
archivo_adjunto = open(ruta_zip, 'rb')
part = MIMEBase('application', 'octet-stream')
part.set_payload((archivo_adjunto).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % nombre_zip)
msg.attach(part)

# Conectar al servidor SMTP
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(from_email, password)

# Enviar el correo electrónico
texto = msg.as_string()
server.sendmail(from_email, to_email, texto)

# Cerrar el archivo ZIP
try:
    zipf.close()
except Exception as e:
    print(f"Error al cerrar el archivo ZIP: {str(e)}")

def eliminar_imagenes_y_zip():
    try:
        for img_file in os.listdir(ruta_image):
            img_path = os.path.join(ruta_image, img_file)
            os.remove(img_path)
        os.remove(ruta_zip)
    except Exception as e:
        print(f"Error al eliminar las imágenes y el archivo ZIP: {str(e)}")

# Registrar la función para eliminar las imágenes y el archivo ZIP al finalizar el script
atexit.register(eliminar_imagenes_y_zip)
    

sys.exit()
