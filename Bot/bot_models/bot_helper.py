import telebot
from telebot import apihelper
from Bot.bot_models.bot_key_local import TOKEN

from Bot.models import User


class helper:

    @staticmethod
    def del_last_keyboard(user: User):
        if user.last_keyboard != None:
            try:
                apihelper.delete_message(TOKEN, user.chat_id, user.last_keyboard)
                # bot.edit_message_reply_markup(user.chat_id, user.last_keyboard, reply_markup=None)
                user.last_keyboard = None
            except:
                pass

    @staticmethod
    def create_subs_str(subs):

        res = "Введіть номер для для видалення\n\n"
        number = 1

        for i in subs:
            res += str(number) + ")"
            if i.currency == "Buy":
                res += "Купівля "
            else:
                res += "Продаж "
            res += i.currency + " " + i.condition + " " + str(i.threshold) + "\n"
            number += 1

        return res
