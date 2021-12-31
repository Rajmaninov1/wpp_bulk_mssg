def wpp_messaging(phones_list,driver,message):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from time import sleep


    numbers = phones_list
    total_number = len(numbers)
    delay = 10

    for idx, number in enumerate(numbers):
        number = number.strip()
        if number == "":
            pass
        print('{}/{} => enviando mensaje a: {}'.format((idx+1), total_number, number))
        try:
            url = 'https://web.whatsapp.com/send?phone=+57' + number + '&text=' + message
            sent = False
            for i in range(3):
                if not sent:
                    driver.get(url)
                    try:
                        click_btn = WebDriverWait(driver, delay).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, '_4sWnG')))
                        sleep(3)
                    except Exception as e:
                        if driver.find_element('._2Nr6U').get_attribute('innerHTML') == "El número de teléfono compartido a través de la dirección URL es inválido":
                            continue
                        print(
                            f"Algo salio mal...\n Falló el enviode mensaje a: {number}, reintentando ({i+1}/3)")
                        print(
                            "Asegurese de que su computador y celular estan conectados a internet.")
                        print("Si hay una alerta de whatsapp, Por favor descartelo.")
                        pass
                    else:
                        click_btn.click()
                        sent = True
                        sleep(1)
                        print('Mensaje enviado a: ' + number)
        except Exception as e:
            print('Fallo enviando mensaje a ' + number + str(e))
            pass

    return sent
