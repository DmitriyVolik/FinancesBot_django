import telebot
import keyboards as kb
import sqlite as db
import currency
import calculations as calc
import predicates as pd
import time
import threading
import predicates as pd


class Handler:

    timer = 86400

    def __init__(self, bot, db):

        self.__bot = bot
        self.__db = db
        self.currency = currency.Currency()
        self.dep_calc = calc.Deposit()

    def create_subs_str(self, user_id):

        subs = self.__db.get_subscriptions(user_id)

        if len(subs) == 0:
            return "У вас немає жодної підписки!"

        res = "Введіть номер для для видалення\n\n"
        number = 1

        for i in subs:
            res += str(number)+")"
            if i[2] == "Buy":
                res += "Купівля "
            else:
                res += "Продаж "
            res += i[3]+" "+i[4]+" "+str(i[5])+"\n"
            number += 1

        self.__db.set_state(user_id, "get_sub_for_del")
        return res

    def start_handler(self, message):
        # Записываем id пользователя в базу данных
        self.__db.clear()
        self.__db.add_user(message.from_user.id)
        self.__bot.send_message(
            message.from_user.id, "Привіт! Обери пункт меню щоб розпочати роботу", reply_markup=kb.user_keyboard)

    def handle_text(self, message):
        id = message.from_user.id
        self.__db.add_user(id)
        state = self.__db.get_state(id)

        if message.text == 'Курс валют':
            self.__db.set_state(
                id, 'show_exchange_rate')
            self.__bot.send_message(id, "Оберіть валюту",
                                    reply_markup=kb.chose_currency)

        elif message.text == 'Конвертер валют':
            self.__bot.send_message(id, "Оберіть:",
                                    reply_markup=kb.chose_currency_convert)
            self.__db.set_state(
                id, 'сurrency_сonverter')

        elif message.text == 'Підписка на курс':
            self.__db.clear()
            self.__bot.send_message(id, "Оберіть",
                                    reply_markup=kb.chose_add_or_dell)
            self.__db.set_state(
                id, "chose_add_or_dell")

        elif message.text == "Депозитний калькулятор":
            self.__db.set_state(
                id, 'get_deposit_amount')
            self.__bot.send_message(
                id, "Введіть суму вкладу")

        elif state == 'сurrency_сonverter':
            self.__bot.send_message(id, self.currency.сurrency_сonverter(
                self.__db.get_converter(id), message.text), parse_mode="Markdown")

        elif state == "subscribe_currency_4":

            if pd.is_exc_rate(message.text):
                self.__db.set_exc_rate_sub(id, message.text)
                self.__bot.send_message(
                    id, "Підписка успішно додана!")
                self.__db.set_state(id, "")
            else:
                self.__bot.send_message(id,
                                        "Помилка, перевірте чи правильно введені дані!")

        elif state == "get_sub_for_del":

            subs = self.__db.get_subscriptions(id)

            try:
                number = int(message.text)-1
            except Exception:
                self.__bot.send_message(id, "Некорректний номер!")
                return

            if number < len(subs) and number >= 0:
                self.__db.del_sub(subs[number][0])
                self.__bot.send_message(id, "Підписку видалено!")
                message_ = self.create_subs_str(id)
                self.__bot.send_message(id, message_)
                return
            self.__bot.send_message(id, "Введений неіснуючий номер!")

        elif state == 'get_deposit_amount' or state == 'get_percent':
            try:
                if state == 'get_deposit_amount':
                    self.__db.set_deposit_amount(id, float(message.text))
                    self.__db.set_state(
                        id, 'get_percent')
                    self.__bot.send_message(
                        id, "Введіть річний відсоток(без урахування податку):")
                else:
                    self.__db.set_deposit_percent(id, float(message.text))
                    self.__db.set_state(
                        id, 'get_type_deposit')
                    self.__bot.send_message(
                        id, "Оберіть тип нарахування відсотка:", reply_markup=kb.chose_deposit_type)
            except Exception:
                self.__bot.send_message(
                    id, "Некоректні дані!")

        elif state == "term_of_deposit":
            try:
                term = int(message.text)
                if term < 0:
                    term *= -1
                self.__bot.send_message(id, self.dep_calc.calculation_deposit(
                    self.__db.get_deposit_percent(id), self.__db.get_deposit_amount(id), term, self.__db.get_deposit_type(id)))
                self.__db.set_state(id, "")
            except Exception:
                self.__bot.send_message(
                    id, "Некоректні дані!")

    def button_handler(self, call):

        id = call.from_user.id

        state = self.__db.get_state(id)

        if state == 'show_exchange_rate':
            self.__bot.send_message(id, self.currency.get_exc_rate(
                call.data, None, True), parse_mode="Markdown")

        elif state == 'subscribe_currency_2' and (pd.is_type(call.data)):
            self.__db.set_sub_type(id, call.data)
            self.__db.set_state(
                id, "subscribe_currency_3")
            self.__bot.send_message(id, "При обиранні  \"*>*\" вам прийде повідомлення в разі перевищення зазначеного вами курсу\n\nПри обиранні  \"*<*\" вам прийде повідомлення коли курс стане менше зазначеного вами\n\nПри обиранні\"*=*\" вам прийде повідомлення коли курс стане тим який ви вказали",
                                    parse_mode="Markdown", reply_markup=kb.chose_currency_subscribe_use)

        elif state == 'сurrency_сonverter':
            self.__db.set_converter(id, call.data)
            self.__bot.send_message(
                id, "Введіть суму, яку хочете перевести:")

        elif state == "subscribe_currency" and pd.is_currency(call.data):
            self.__db.set_currency_sub(id, call.data)
            self.__db.set_state(
                id, "subscribe_currency_2")
            self.__bot.send_message(
                id, "Оберіть тип курса:", reply_markup=kb.chose_buy_or_sell)

        elif state == "subscribe_currency_3" and pd.is_use(call.data):
            self.__db.set_sign_sub(id, call.data)
            self.__db.set_state(
                id, "subscribe_currency_4")
            self.__bot.send_message(
                id, "Введіть курс валюти, з 2 цифрами після точки\n\nПриклад: 10.25")

        elif state == "chose_add_or_dell" and call.data == "add":
            self.__db.set_state(id, 'subscribe_currency')
            self.__bot.send_message(
                id, "Коли валюта досягне обраного вами курсу, вам прийде повідомлення, оберіть валюту на яку хочете підписатися:", reply_markup=kb.chose_currency)

        elif state == "chose_add_or_dell" and call.data == "del":

            message_ = self.create_subs_str(id)
            self.__bot.send_message(id, message_)

        elif state == 'get_type_deposit' and pd.is_type_deposit(call.data):
            self.__bot.send_message(
                id, "Введіть термін вкладу (в місяцях)")
            self.__db.set_deposit_type(id, call.data)
            self.__db.set_state(id, 'term_of_deposit')
