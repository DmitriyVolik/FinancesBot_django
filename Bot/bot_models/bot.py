from Bot.bot_models.bot_key_local import TOKEN
from Bot.bot_models.states.state_provider import *
import Bot.bot_models.keyboards as kb
from Bot.bot_models.bot_helper import helper

day_timer = 86400

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_command(message):  # Проверяем команды от пользователя
    provider = state_provider(bot)
    current_state = provider.get_state_for_user_id(user_id=message.from_user.id)
    new_state = default_state(bot, current_state.user)
    bot.send_message(message.from_user.id, "Привіт! Обери пункт меню щоб розпочати роботу",
                     reply_markup=kb.user_keyboard)
    provider.set_state(new_state)


@bot.callback_query_handler(lambda call: True)
def process_callback_button(call):
    bot.answer_callback_query(callback_query_id=call.id)
    provider = state_provider(bot)
    current_state = provider.get_state_for_user_id(call.from_user.id)
    new_state = current_state.handle_callable(call)
    provider.set_state(new_state)


@bot.message_handler(content_types=['text'])  # Проверяем текст от пользователя
def handle_text(message):
    chat_id = message.from_user.id
    provider = state_provider(bot)
    current_state = provider.get_state_for_user_id(chat_id)
    new_state = None

    if message.text == kb.menu["SUBSCRIBE"]:
        new_state = subscribe_menu_state(bot, current_state.user)
    elif message.text == kb.menu["EXCHANGE_RATE"]:
        new_state = show_exchange_rate_state(bot, current_state.user)
    elif message.text == kb.menu["CURRENCY_CONVERTER"]:
        new_state = currency_converter_state(bot, current_state.user)
    elif message.text == kb.menu["DEPOSIT_CALCULATOR"]:
        new_state = deposit_state(bot, current_state.user)
    else:
        new_state = current_state.handle_message(message)

    if new_state != None:
        provider.set_state(new_state)

