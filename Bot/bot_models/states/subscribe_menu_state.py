from Bot.bot_models.states.state import state
import telebot
import Bot.bot_models.keyboards as kb
from Bot.bot_models.states.subscribe_state import subscribe_state
from Bot.bot_models.states.subscribe_delete_state import subscribe_delete_state


class subscribe_menu_state(state):

    def get_uid(self) -> str:
        return 'subscribe_menu'

    def handle_callable(self, callable: telebot.types.CallbackQuery):
        # Убрать кнопки в сообщении от которого пришел каллбек
        self.bot.edit_message_reply_markup(
            chat_id=callable.message.chat.id,
            message_id=callable.message.message_id,
            reply_markup=None)
        self.user.last_keyboard=None

        if callable.data == 'add':
            return subscribe_state(self.bot, self.user)
        elif callable.data == 'del':
            return subscribe_delete_state(self.bot, self.user)

    def display(self):
        if self.get_uid() == "subscribe_menu" or self.get_uid() == "subscribes_empty":
            msg = self.bot.send_message(self.user.chat_id, "Оберіть пункт меню", reply_markup=kb.chose_add_or_dell)
            self.user.last_keyboard = msg.message_id
            return self

