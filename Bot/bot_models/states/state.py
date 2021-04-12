from abc import abstractmethod, ABC

import telebot
from Bot.models import User

class state(ABC):
    params = {}
    bot: telebot
    user: User

    def __init__(self, bot: telebot, user: User, params=None):
        self.user = user
        self.bot = bot
        if (params != None):
            self.params = params

    @abstractmethod
    def get_uid(self) -> str:
        pass

    def get_param(self, name: str):
        try:
            return self.params[name]
        except:
            return ""

    def set_param(self, name: str, value):
        self.params[name] = value

    def display(self):
        pass

    def handle_message(self, message: telebot.types.Message):
        return self

    def handle_callable(self, callable: telebot.types.CallbackQuery):
        return self
