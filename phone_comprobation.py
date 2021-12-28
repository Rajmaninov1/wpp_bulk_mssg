import phonenumbers
from phonenumbers import carrier, geocoder
import re
from extractPhones import pHones

search_list = pHones()

for number in search_list:
    text = str(number)
    numbers_list = re.findall(".*?(\(?3\d{2}\D{0,3}\d{3}\D{0,3}\d{4}).*?",text)

    for match in numbers_list:
        try:
            phonenumber = phonenumbers.parse(match,"CO")
            print("\n",phonenumber)
            possible_number = phonenumbers.is_possible_number(phonenumber)
            if possible_number == True:
                print("¿El número es válido? ",'Sí' if phonenumbers.is_valid_number(phonenumber) == True else 'No')
                if carrier.name_for_valid_number(phonenumber, "en") != '':
                    print("País del código: ", geocoder.description_for_number(phonenumber, "en"))
                    print("Su operador es: ", carrier.name_for_valid_number(phonenumber, "en"))
                    print("-> El número está en uso <-")
                else:
                    print("El numero no está en uso")
            else:
                print("No es un número posible")
        except (phonenumbers.phonenumberutil.NumberParseException, phonenumbers.phonenumberutil.NumberParseException, AttributeError) as exception:
            print(exception)
        print("____________________________________________")
