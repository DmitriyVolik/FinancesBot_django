from Bot.bot_models.bot_helper import helper
from Bot.bot_models.states.default_state import default_state
from Bot.bot_models.states.state import state
from Bot.bot_models.currency import currency
import telebot
import Bot.bot_models.keyboards as kb
import Bot.bot_models.predicates as pd
from Bot.models import Keyboards


class show_exchange_rate_state(state):
    currency = currency()

    def get_uid(self) -> str:
        return 'show_exchange_rate'

    def handle_callable(self, callable: telebot.types.CallbackQuery):
        self.bot.edit_message_reply_markup(
            chat_id=callable.message.chat.id,
            message_id=callable.message.message_id,
            reply_markup=None)
        self.user.last_keyboard = None

        if pd.is_currency(callable.data):
            self.bot.send_message(self.user.chat_id, self.currency.get_exc_rate(callable.data), parse_mode="Markdown")
            return default_state(self.bot, self.user)

    def display(self):
        msg = self.bot.send_message(self.user.chat_id, "Оберіть валюту", reply_markup=kb.chose_currency)
        self.user.last_keyboard = msg.message_id
