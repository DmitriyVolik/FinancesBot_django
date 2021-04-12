
import re


def is_exc_rate(text):
    try:
        round(float(text), 2)
        return True
    except Exception:
        return False


def is_currency(text):
    return (text == "USD" or text == "RUR" or text == "EUR" or text == "BTC")


def is_use(text):
    return (text == ">" or text == "<" or text == "=")


def is_type(text):
    return (text == "Buy" or text == "Sell")


def is_type_deposit(text):
    return (text == "on_deposit" or text == "on_acc")



def is_correct_converter_button(call):
   buttons=["UAH USD", "UAH RUR", "UAH EUR","BTC USD","USD UAH","RUR UAH",'EUR UAH', 'USD BTC']
   for i in buttons:
       if call.data==i:
           return True
   return False


