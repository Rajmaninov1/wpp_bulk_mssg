import re
from spreadsheets import get_information,get_sheets_names, sheet_update
from wpp_messaging import wpp_messaging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
from urllib.parse import quote
from datetime import datetime


# Opens the message to send
f = open("message.txt", "r")
message = f.read()
f.close()
message = quote(message)

# Selects the spreadsheet to read
sheet_number = get_sheets_names('MarkeBot')
search_list = get_information(sheet_number=sheet_number)

# Uses the options to use default user configuration in the browser
options = Options()
options.add_argument(r"user-data-dir=C:/Users/tolos/AppData/Local/Google/Chrome/User Data")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Opens the webdriver and goes to whatsapp web
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
print('Una vez su navegador inicie ingresará a whatsapp web')
driver.get('https://web.whatsapp.com')
sleep(15)

# list of comprobation to 
wpp_comprobation = []
date_mssg = []
today = str(datetime.today().strftime('%Y-%m-%d'))

for number in search_list:
    text = str(number[0]).replace(' ','')
    aproved = number[1]
    mssg_sended = number[2]
    date_sended = number[3]
    numbers_list = re.findall(".*?(\(?3\d{2}\D{0,3}\d{3}\D{0,3}\d{4}).*?",text)
    sent = False
    print(numbers_list)

    for i,match in enumerate(numbers_list):
        try:
            if aproved == 1 and str(mssg_sended) != '1':
                sent = wpp_messaging([match],driver,message)
            else:
                print("no aprobado")
        except:
            print("Ha ocurrido un error")
    
    if sent == True or mssg_sended == 1:
        wpp_comprobation.append([1])
    else:
        wpp_comprobation.append([0])
    if str(date_sended) == '':
        date_mssg.append([today])
    else:
        date_mssg.append([date_sended])


sheet_update(sheet_number,wpp_comprobation,'E2:E')
sheet_update(sheet_number,date_mssg,'F2:F')

driver.close()

print("""la ejecución del programa se ha completado sin errores. 
Puede comprobar la información registrada tras este proceso 
en la hoja de calculo asociada.""")