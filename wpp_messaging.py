from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def wpp_messaging(phones_list,driver,message,file_path=None):
    """
    Envía mensajes via whatsapp web a una lista de números que se le pasa.
    Datos de entrada:
    - Lista de numeros
    - Driver o configuración del navegador abierto con selenium
    - El mensaje a enviar
    - La ruta de una imagen si se desea agregar que debe tener como raiz de la dirección la carpeta de imagenes

    La salida de la función devuelve una lista de dos elementos que consiste en un valor verdadero o falso 
    según si se envió o no correctamente el mensaje y un valor de 0 o 1 dependiendo de si el número ingresado
    tiene o no tiene whatsapp.
    """
    numbers = phones_list
    total_number = len(numbers)
    wpp_existence = 0
    delay = 10

    for idx, number in enumerate(numbers):
        number = number.strip()
        if number == "":
            pass
        print('{}/{} => enviando mensaje a: {}'.format((idx+1), total_number, number))
        try:
            if message == '':
                url = 'https://web.whatsapp.com/send?phone=57' + number + '&text'
            else:
                url = 'https://web.whatsapp.com/send?phone=57' + number + '&text=' + message
            sent = False
            for i in range(3):
                if not sent:
                    driver.get(url)
                    try:
                        if message == '':
                            click_btn = WebDriverWait(driver, delay).until(
                                EC.element_to_be_clickable((By.XPATH, '//div[@title = "Adjuntar"]')))
                        else:
                            click_btn = WebDriverWait(driver, delay).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, '_4sWnG')))
                        sleep(1)
                    except Exception as e:
                        if driver.find_element_by_class_name('_2Nr6U').get_attribute('innerHTML') == "El número de teléfono compartido a través de la dirección URL es inválido":
                            wpp_existence = 1
                            break
                        print(
                            f"Algo salio mal...\n Falló el enviode mensaje a: {number}, reintentando ({i+1}/3)")
                        print(
                            "Asegurese de que su computador y celular estan conectados a internet.")
                        print("Si hay una alerta de whatsapp, Por favor descartelo.")
                        pass
                    else:
                        if file_path != None:
                            print(file_path)
                            attachment_box = driver.find_element_by_xpath('//div[@title = "Adjuntar"]')
                            attachment_box.click()
                            image_box = driver.find_element_by_xpath(
                                '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
                            image_box.send_keys(file_path)
                            click_btn = WebDriverWait(driver, delay).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, '_1w1m1')))
                        else:
                            sleep(4)
                        click_btn.click()
                        sent = True
                        sleep(2)
                        print('Mensaje enviado a: ' + number)
        except Exception as e:
            print('Fallo enviando mensaje a ' + number + str(e))
            pass

    return [sent,wpp_existence]
