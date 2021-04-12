import telebot

from Bot.bot_models.states.default_state import default_state
from Bot.bot_models.states.state import state
import Bot.bot_models.keyboards as kb
from Bot.bot_models.currency import currency


class currency_converter_state(state):
    DEFAULT_PARAMS = {"currencies": ""}
    currency = currency()

    def get_uid(self) -> str:
        return 'currency_converter'

    def display(self):
        if self.get_param('currencies') == "":
            msg = self.bot.send_message(self.user.chat_id,
                                        "Оберіть:",
                                        reply_markup=kb.chose_currency_convert)
            self.user.last_keyboard = msg.message_id

        else:
            self.bot.send_message(self.user.chat_id, "Введіть суму для конвертації:")

        return self

    def handle_callable(self, callable: telebot.types.CallbackQuery):
        self.bot.edit_message_reply_markup(
            chat_id=callable.message.chat.id,
            message_id=callable.message.message_id,
            reply_markup=None)
        self.user.last_keyboard = None

        if self.get_param('currencies') == '':
            self.set_param('currencies', callable.data)
            return self

    def handle_message(self, message: telebot.types.Message):
        text = message.text

        if self.get_param('currencies') != "":
            try:
                float(text)
                self.bot.send_message(self.user.chat_id, self.currency.convertor(self.get_param('currencies'), text),
                                      parse_mode="Markdown")
                return default_state(self.bot, self.user)
            except:
                self.bot.send_message(self.user.chat_id, "Некорекне значення!")
        return self
