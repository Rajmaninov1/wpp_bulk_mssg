def wpp_messaging(phones_list,driver,message):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from time import sleep
    from selenium.webdriver.common.keys import Keys


    numbers = phones_list
    total_number = len(numbers)
    delay = 10

    for idx, number in enumerate(numbers):
        number = number.strip()
        if number == "":
            continue
        print('{}/{} => enviando mensaje a: {}'.format((idx+1), total_number, number))
        try:
            number = number.replace(' ','')
            url = 'https://web.whatsapp.com/send?phone=+57' + number + '&text=a'
            print(url)
            sent = False
            for i in range(3):
                if not sent:
                    driver.get(url)
                    sleep(1)
                    try:
                        input = WebDriverWait(driver, delay).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div')))
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
                        sleep(1)
                        input.click()
                        sleep(0.5)
                        input.send_keys(Keys.BACKSPACE)
                        sleep(0.2)
                        input.send_keys(message)
                        sleep(0.5)
                        driver.get_element('._4sWnG').click()
                        sent = True
                        sleep(4)
                        print('Mensaje enviado a: ' + number)
        except Exception as e:
            print('Fallo enviando mensaje a ' + number + str(e))
            pass

    return sent
