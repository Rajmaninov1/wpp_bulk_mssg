import re
from os import getenv
from time import sleep
from urllib.parse import quote
from datetime import datetime
import ctypes.wintypes

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from spreadsheets import get_information,get_sheets_names, sheet_update
from wpp_messaging import wpp_messaging


# Get windows username and images path
user = getenv('username')
CSIDL_MYPICTURES = 39
buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_MYPICTURES, 0, 0, buf)
pictures_path = buf.value + '\\'

# Opens the message to send
f = open("message.txt", "r")
message = f.read().encode('raw_unicode_escape')
f.close()
message = quote(message)

# Selects the spreadsheet to read
sheet_number = get_sheets_names('MarkeBot')
search_list = get_information(sheet_number=sheet_number)

# Selects the image to send in the message. It might be in images folder
want_image = True if input("¿Desea añadir una imagen? s/n: \n").lower() == 's' else False
file_path = None
if want_image:
    file_path = pictures_path + open("image.txt", "r").read().replace('\n','')

# Uses the options to use default user configuration in the browser
options = Options()
options.add_argument("user-data-dir=C:/Users/"+ user +"/AppData/Local/Google/Chrome/User Data")
#options.add_argument("profile-directory=")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Opens the webdriver and goes to whatsapp web
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
print('Una vez su navegador inicie ingresará a whatsapp web')
driver.get('https://web.whatsapp.com')
sleep(15)

# list of comprobation to 
wpp_comprobation = []
date_mssg = []
wpp_exists = []
today = str(datetime.today().strftime('%Y-%m-%d'))

try:
    for row in search_list:
        text = str(row[0]).replace(' ','')
        # Representa si el numero ha sido aprobado manualmente para ser contactado
        aproved = row[1]
        # Representa si el numero ha sido enviado
        mssg_sended = row[2]
        # Representa la fecha en que el mensaje ha sido enviado
        date_sended = row[3]
        # Representa si el numero al que se enviará el mensaje tiene o no whatsapp
        wpp_existence = row[4]
        # Representa la lista de numeros encontrados para enviar mensajes
        numbers_list = re.findall(".*?(\(?3\d{2}\D{0,3}\d{3}\D{0,3}\d{4}).*?",text)
        # Representa si el mensaje ha sido enviado o no
        enviado = False
        # Representa el estado por defecto de un envio de mensaje
        sent = [enviado,wpp_existence]
        print(numbers_list)

        for i,match in enumerate(numbers_list):
            try:
                if aproved == 1 and str(mssg_sended) != '1' and wpp_existence != 1:
                    sent = wpp_messaging([match],driver,message,file_path)
                else:
                    print("no aprobado")
            except:
                print("Ha ocurrido un error")
        
        date_sended = date_sended.replace("'","")
        if sent[0] == True or mssg_sended == 1:
            wpp_comprobation.append([1])
            # Revisa el formato de la fecha
            if re.match('\d{2,4}[-/\ ]\d{2}[-/\ ]\d{2,4}',str(date_sended)):
                date_mssg.append([date_sended])
            else:
                date_mssg.append([today])
        else:
            wpp_comprobation.append([0])
            date_mssg.append([date_sended])
        wpp_exists.append([sent[1]])

    sheet_update(sheet_number,wpp_comprobation,'E2:E')
    sheet_update(sheet_number,date_mssg,'F2:F')
    sheet_update(sheet_number,wpp_exists,'H2:H')

    print("la ejecución del programa se ha completado sin errores. Puede comprobar la información registrada tras este proceso en la hoja de calculo asociada.")
except Exception as e:
    print("Ha ocurrido un error inesperado:\n")
    print(e)

driver.close()
