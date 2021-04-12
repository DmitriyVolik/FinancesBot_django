import requests
from Bot.bot_models.config import currency_url
from Bot.models import Subscribe

class currency:
    __response = 0  # Поле для Json с курсами валют

    def get_exc_rate(self, text, rate_type=None):
        # Получаем Json от приватбанка
        self.__response = requests.get(currency_url).json()

        currency_sec = "UAH"

        for coin in self.__response:
            if (text == coin['ccy']):
                buy = round(float(coin['buy']), 2)
                sell = round(float(coin['sale']), 2)
                if rate_type == "Buy":
                    return buy
                elif rate_type == "Sell":
                    return sell
                else:
                    try:
                        if text == "BTC":
                            currency_sec = "USD"
                        return "💰 Курс купівлі " + text + ": " + "*" + str(
                            buy) + "* " + currency_sec + "\n" + "💰" + " Курс продажу " + text + ": " + "*" + str(
                            sell) + "* " + currency_sec
                    except Exception:  # Если что-то пошло не так, тправляем ошибку
                        return "Не вдалося отримати дані"

    def convertor(self, text, amount):

        try:

            lst = text.split()

            amont = float(amount)

            round_quantity = 2

            if lst[1] == "UAH" or lst[0] == "BTC":
                result = round(
                    amont * float(self.get_exc_rate(lst[0], "Buy")), round_quantity)
                sec_currency = lst[1]
            else:
                if lst[1] == "BTC":
                    round_quantity = 15
                result = round(
                    amont / float(self.get_exc_rate(lst[1], "Sell")), round_quantity)
                sec_currency = lst[1]
            return "💰*" + str(result) + "* " + sec_currency
        except:
            return "Не вдалося отримати дані"

    def check_subscribes(self, subs):

        result = ""

        for i in subs:

            exc = self.get_exc_rate(i.currency, i.rate_type)

            if (i.condition == ">" and exc > float(i.threshold)):
                result += "💰Курс " + i.currency + " став більше ніж " + \
                          str(i.threshold) + "!!!\n💰Поточний курс:" + str(exc) + "\n\n"

            elif (i.condition == "<" and exc < float(i.threshold)):
                result += "💰Курс " + i.currency + " став менше ніж " + \
                          str(i.threshold) + "!!!\n💰Поточний курс:" + str(exc) + "\n\n"

            elif (i.condition == "=" and exc == float(i.threshold)):
                result += "💰Курс " + i.currency + " дорівнює " + \
                          str(i.threshold) + "!!!\n💰Поточний курс:" + str(exc) + "\n\n"

        return result
