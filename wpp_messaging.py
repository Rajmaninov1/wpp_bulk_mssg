def wpp_messaging(phones_list):

    f = open("message.txt", "r")
    message = f.read()
    f.close()
    #message = """Buenas tardes... soy """ + nombre + message

    #print("##########################################################")
    #print('Este es su mensaje\n\n')
    #print(message)
    #print("##########################################################")
    #message = quote(message)

    numbers = phones_list
    #f = open("numbers.txt", "r")
    #for line in f.read().splitlines():
    #    if line != "":
    #        numbers.append(line)
    #f.close()
    total_number = len(numbers)
    #print("##########################################################")
    #print('\nEncontramos ' + str(total_number) + ' numeros en el archivo')
    #print("##########################################################")
    #print()
    delay = 30

    driver = webdriver.Chrome(ChromeDriverManager().install())
    print('Una vez su navegador inicie ingresará a whatsapp web')
    driver.get('https://web.whatsapp.com')
    no_wpp_numbers = []
    wpp_numbers = []

    for idx, number in enumerate(numbers):
        number = number.strip()
        if number == "":
            continue
        print('{}/{} => enviando mensaje a: {}.'.format((idx+1), total_number, number))
        try:
            url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
            sent = False
            for i in range(3):
                if not sent:
                    driver.get(url)
                    try:
                        click_btn = WebDriverWait(driver, delay).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, '_4sWnG')))
                        sleep(2)
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
                        click_btn.click()
                        sent = True
                        wpp_numbers.append(number)
                        sleep(2)
                        print('Mensaje enviado a: ' + number)
        except Exception as e:
            no_wpp_numbers.append(number)
            print('Fallo enviando mensaje a ' + number + str(e))
            pass

    print("\nLos numeros a los quese envio mensaje fueron: ",
        len(wpp_numbers), "\n", wpp_numbers)
    print("\nLos numeros sin whatsapp fueron: ",
        len(no_wpp_numbers), "\n", no_wpp_numbers)

    driver.close()
