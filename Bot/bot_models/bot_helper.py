import telebot
from django.core.exceptions import ObjectDoesNotExist

from Bot.models import User
from Bot.models import Subscribe


class helper:

    @staticmethod
    def del_last_keyboard(bot: telebot,user: User):
        if user.last_keyboard != None:
            try:
                bot.edit_message_reply_markup(user.chat_id, user.last_keyboard, reply_markup=None)
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
