import re
from extractPhones import pHones
from wpp_messaging import wpp_messaging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
from urllib.parse import quote,urlparse


f = open("message.txt", "r")
message = f.read()
f.close()
message = quote(urlparse(message.encode('UTF-8')))

print("Seleccione la hoja de calculo de Google que se usará para extraer números: ")
search_list = pHones(sheet_number=int(input()))
options = Options()
options.add_argument(r"user-data-dir=C:/Users/tolos/AppData/Local/Google/Chrome/User Data")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
print('Una vez su navegador inicie ingresará a whatsapp web')
driver.get('https://web.whatsapp.com')
sleep(7)

for number in search_list:
    print(number)
    text = str(number[0]).replace(' ','')
    aproved = number[1]
    numbers_list = re.findall(".*?(\(?3\d{2}\D{0,3}\d{3}\D{0,3}\d{4}).*?",text)

    for i,match in enumerate(numbers_list):
        try:
            if aproved == 1:
                print("aprobado por Gustavo: ",match)
                wpp_messaging([match],driver,message)
            else:
                print("no aprobado")
        except:
            print("Ha ocurrido un error")
        last_record = i

driver.close()