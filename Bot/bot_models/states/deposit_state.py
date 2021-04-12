import telebot

from Bot.bot_models.states.default_state import default_state
from Bot.bot_models.states.state import state
import Bot.bot_models.keyboards as kb
from Bot.bot_models.calculations import deposit


class deposit_state(state):
    DEFAULT_PARAMS = {"deposit_percent": "", "deposit_type": "", "deposit_amount": ""}

    deposit = deposit()

    def get_uid(self) -> str:
        return 'deposit'

    def display(self):

        if self.get_param("deposit_amount") == "":
            self.bot.send_message(self.user.chat_id,
                                  "Введіть суму вкладу:",
                                  )
            return self

        if self.get_param("deposit_percent") == "":
            self.bot.send_message(self.user.chat_id, "Введіть річний відсоток(без урахування податку):")
            return self
        if self.get_param("deposit_type") == "":
            msg = self.bot.send_message(self.user.chat_id, "Оберіть тип нарахування відсотка:",
                                        reply_markup=kb.chose_deposit_type)
            self.user.last_keyboard = msg.message_id
            return self




    def handle_callable(self, callable: telebot.types.CallbackQuery):
        self.bot.edit_message_reply_markup(
            chat_id=callable.message.chat.id,
            message_id=callable.message.message_id,
            reply_markup=None)
        self.user.last_keyboard = None

        if self.get_param('deposit_percent')!="":
            self.bot.send_message(self.user.chat_id,"Введіть термін вкладу (в місяцях)")
            self.set_param('deposit_type', callable.data)
            return self





    def handle_message(self, message: telebot.types.Message):
        text = message.text

        if self.get_param('deposit_amount') == "" or self.get_param('deposit_percent') == "":
            try:
                float(text)
                if self.get_param('deposit_amount') == "":
                    self.set_param('deposit_amount', text)
                else:

                    self.set_param('deposit_percent', text)
            except:
                self.bot.send_message(self.user.chat_id, "Некорекне значення!")
            return self

        if self.get_param('deposit_type') != "":
            try:
                term = int(message.text)
                if term < 0:
                    term *= -1
                self.bot.send_message(self.user.chat_id, self.deposit.calculation_deposit(
                    self.get_param("deposit_percent"), self.get_param("deposit_amount") , term,
                    self.get_param("deposit_type")))
                return default_state(self.bot, self.user)
            except Exception:
                self.bot.send_message(
                    self.user.chat_id, "Некоректні дані!")
