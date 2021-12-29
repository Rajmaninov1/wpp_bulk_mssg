import re
from extractPhones import pHones
from wpp_messaging import wpp_messaging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from urllib.parse import quote

print("Seleccione la hoja de calculo de Google que se usará para extraer números: ")
search_list = pHones(sheet_number=input())

for number in search_list:
    text = str(number[0])
    aproved = number[1]
    numbers_list = re.findall(".*?(\(?3\d{2}\D{0,3}\d{3}\D{0,3}\d{4}).*?",text)

    for i,match in enumerate(numbers_list):
        try:
            if aproved == '1':
                print("aprobado por Gustavo: ",match)
                wpp_messaging.wpp_messaging(match)
            else:
                print("no aprobado")
        except:
            print("Ha ocurrido un error")
        last_record = i