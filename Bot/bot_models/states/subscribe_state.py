import telebot
from Bot.models import Subscribe
from Bot.bot_models.states.state import state
from Bot.bot_models.states.default_state import default_state
import Bot.bot_models.keyboards as kb
import Bot.bot_models.predicates as pd


class subscribe_state(state):
    DEFAULT_PARAMS = {"currency": "", "rate_type": "", "threshold": "", "condition": ""}

    def get_uid(self) -> str:
        return 'subscribe'

    def handle_callable(self, callable: telebot.types.CallbackQuery):
        text = callable.data

        # # Убрать кнопки в сообщении от которого пришел каллбек
        self.bot.edit_message_reply_markup(
            chat_id=callable.message.chat.id,
            message_id=callable.message.message_id,
            reply_markup=None)
        self.user.last_keyboard=None

        if self.get_param('currency') == '':
            self.set_param('currency', text)
            return self

        if self.get_param('rate_type') == '':
            self.set_param('rate_type', text)
            return self

        if self.get_param('condition') == '':
            self.set_param('condition', text)



            rate_type = self.get_param('rate_type')

            s = Subscribe(user_id=self.user.id,
                          currency=self.get_param('currency'),
                          threshold=self.get_param('threshold'),
                          rate_type=rate_type,
                          condition=self.get_param('condition'),
                          )
            s.save()
            self.bot.send_message(self.user.chat_id, "Підписка успішно додана!")
            return default_state(self.bot, self.user)

    def handle_message(self, message: telebot.types.Message):
        text = message.text

        if self.get_param('rate_type') == "" or self.get_param('threshold') != '':
            return self

        if self.get_param('threshold') == '' and self.get_param('rate_type')!="":

            if pd.is_exc_rate(text):
                self.set_param('threshold', str(text))
            else:
                self.bot.send_message(self.user.chat_id, "Некорекне значення!")



        return self

    def display(self):

        if self.get_param('currency') == "":
            msg=self.bot.send_message(self.user.chat_id, "Коли валюта досягне обраного вами курсу, вам прийде повідомлення, оберіть валюту:", reply_markup=kb.chose_currency)
            self.user.last_keyboard=msg.message_id
            return self
        if self.get_param('rate_type') == "":
            msg=self.bot.send_message(self.user.chat_id, "Оберіть тип курсу", reply_markup=kb.chose_buy_or_sell)
            self.user.last_keyboard = msg.message_id
            return self
        if self.get_param('threshold') == "":
            self.bot.send_message(self.user.chat_id, "Введіть курс валюти, з 2 цифрами після точки\n\nПриклад: 10.25")
            return self
        if self.get_param('condition') == "":
            msg=self.bot.send_message(self.user.chat_id, "При обиранні  \">\" вам прийде повідомлення в разі перевищення зазначеного вами курсу\n\nПри обиранні  \"<\" вам прийде повідомлення коли курс стане менше зазначеного вами\n\nПри обиранні\"=\" вам прийде повідомлення коли курс стане тим який ви вказали", reply_markup=kb.chose_currency_subscribe_use)
            self.user.last_keyboard = msg.message_id
            return self
