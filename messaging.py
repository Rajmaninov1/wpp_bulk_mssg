import pywhatkit

number = ""
mssg = "Este es un mensaje de prueba del bot, por favor ignorar."
wait_time = 15
tab_close = False
close_time = 5

#Sends mssg instantly. It can only work with multiple messaging using multithreading
pywhatkit.sendwhatmsg_instantly(phone_no=number, message=mssg, wait_time=wait_time, tab_close=tab_close, close_time=close_time)
