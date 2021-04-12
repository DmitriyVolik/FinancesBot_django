from Bot.bot_models.states.currency_converter_state import currency_converter_state
from Bot.bot_models.states.default_state import default_state
from Bot.bot_models.states.state import state
from Bot.bot_models.states.subscribe_delete_state import subscribe_delete_state
from Bot.bot_models.states.subscribe_state import subscribe_state
import telebot
from Bot.models import User
from django.core.exceptions import ObjectDoesNotExist
import json
from Bot.bot_models.states.subscribe_menu_state import subscribe_menu_state
from Bot.bot_models.states.show_exchange_rate_state import show_exchange_rate_state
from Bot.bot_models.states.deposit_state import deposit_state


class state_provider:
    bot: telebot

    def __init__(self, bot: telebot):
        self.bot = bot

    def get_state_for_user_id(self, user_id) -> state:
        try:
            u = User.objects.get(chat_id=user_id)
        except ObjectDoesNotExist:
            u = User(chat_id=user_id, state='default')
            u.save()

        if (u.state == 'default'):
            return default_state(self.bot, u)
        if (u.state == 'subscribe_menu'):
            return subscribe_menu_state(self.bot, u)
        if (u.state == 'subscribe'):
            return subscribe_state(self.bot, u, json.loads(u.state_params))
        if (u.state == 'subscribe_delete'):
            return subscribe_delete_state(self.bot, u)
        if (u.state == 'show_exchange_rate'):
            return show_exchange_rate_state(self.bot, u)
        if (u.state == 'currency_converter'):
            return currency_converter_state(self.bot, u,  json.loads(u.state_params))
        if (u.state == 'deposit'):
            return deposit_state(self.bot, u,  json.loads(u.state_params))


    def set_state(self, new_state: state):
        new_state.display()
        new_state.user.state = new_state.get_uid()
        new_state.user.state_params = json.dumps(new_state.params)
        new_state.user.save()
