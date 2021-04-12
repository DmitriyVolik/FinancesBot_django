import Bot.bot_models.currency as cur
from Bot.models import User
from Bot.models import Subscribe
from Bot.bot_models.bot import bot


def check():
    currency = cur.currency()

    users_id = User.objects.all()

    for i in users_id:

        message_to_user = ""

        message_to_user += currency.check_subscribes(Subscribe.objects.filter(user=i))

        if message_to_user != "":
            bot.send_message(i.chat_id, message_to_user)
