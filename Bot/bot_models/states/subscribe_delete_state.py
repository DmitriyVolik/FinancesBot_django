import telebot
from Bot.bot_models.states.state import state
from Bot.bot_models.bot_helper import helper
import Bot.bot_models.keyboards as kb
from Bot.bot_models.states.subscribe_state import subscribe_state

from Bot.models import Subscribe


class subscribe_delete_state(state):

    def get_uid(self) -> str:
        return 'subscribe_delete'

    def display(self):
        if self.get_uid() == "subscribe_delete":

            subs = Subscribe.objects.filter(user=self.user)

            if len(subs) == 0:
                self.bot.send_message(self.user.chat_id, "У вас немає жодної підписки!", reply_markup=kb.add_sub_only)
                return self

            self.bot.send_message(self.user.chat_id, helper.create_subs_str(subs))
            return self

    def handle_message(self, message: telebot.types.Message):
        try:
            number = int(message.text) - 1
        except Exception:
            self.bot.send_message(self.user.chat_id, "Некорректний номер!")
            return self

        subs = Subscribe.objects.filter(user=self.user)

        if number < len(subs) and number >= 0:
            Subscribe.objects.filter(id=subs[number].id).delete()

            self.bot.send_message(self.user.chat_id, "Підписку видалено!")
        else:
            self.bot.send_message(self.user.chat_id, "Введений неіснуючий номер!")
        return self

    def handle_callable(self, callable: telebot.types.CallbackQuery):
        self.bot.edit_message_reply_markup(
            chat_id=callable.message.chat.id,
            message_id=callable.message.message_id,
            reply_markup=None)
        self.user.last_keyboard = None

        if callable.data == 'add':
            return subscribe_state(self.bot, self.user)
