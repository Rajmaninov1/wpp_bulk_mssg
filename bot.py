import re
from spreadsheets import pHones,message_sended
from wpp_messaging import wpp_messaging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
from unicodedata import normalize
from urllib.parse import quote

# Opens the message to send
f = open("message.txt", "r")
message = f.read()
f.close()
message = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", message), 0, re.I
    )
message = quote(message)

# Selects the spreadsheet to read
print("Seleccione la hoja de calculo de Google que se usará para extraer números: ")
sheet_number = int(input())
search_list = pHones(sheet_number=sheet_number)

# Uses the options to use default user configuration in the browser
options = Options()
options.add_argument(r"user-data-dir=C:/Users/tolos/AppData/Local/Google/Chrome/User Data")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Opens the webdriver and goes to whatsapp web
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
print('Una vez su navegador inicie ingresará a whatsapp web')
driver.get('https://web.whatsapp.com')
sleep(20)

# list of comprobation to 
wpp_comprobation = []

for number in search_list:
    text = str(number[0]).replace(' ','')
    aproved = number[1]
    mssg_sended = number[2]
    numbers_list = re.findall(".*?(\(?3\d{2}\D{0,3}\d{3}\D{0,3}\d{4}).*?",text)
    sent = False
    print(numbers_list)

    for i,match in enumerate(numbers_list):
        try:
            if aproved == 1 and int(mssg_sended) != 1:
                sent = wpp_messaging([match],driver,message)
            else:
                print("no aprobado")
        except:
            print("Ha ocurrido un error")
    
    if sent == True or mssg_sended == 1:
        wpp_comprobation.append([1])
    else:
        wpp_comprobation.append([0])

message_sended(sheet_number,wpp_comprobation,'E2:E')
driver.close()