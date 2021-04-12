import telebot
from telebot import types

translate = {
    'Exchange rate':  'Курс валют'
}

menu = {
    "EXCHANGE_RATE" : translate["Exchange rate"],
    "SUBSCRIBE" : 'Підписка на курс',
    "CURRENCY_CONVERTER" : 'Конвертер валют',
    "DEPOSIT_CALCULATOR" : 'Депозитний калькулятор',

}

user_keyboard = telebot.types.ReplyKeyboardMarkup(
    True, True)  # Все кнопки в меню

# Основная клавиатура пользователя:
user_keyboard.row(menu["EXCHANGE_RATE"], menu["SUBSCRIBE"])
user_keyboard.row(menu["CURRENCY_CONVERTER"], menu["DEPOSIT_CALCULATOR"])

# Строчная клавиатура для выбора валюты
chose_currency = types.InlineKeyboardMarkup(row_width=2)
chose_currency.add(types.InlineKeyboardButton(text='USD', callback_data='USD'),
                   types.InlineKeyboardButton(text='RUR', callback_data='RUR'),
                   types.InlineKeyboardButton(text='EUR', callback_data='EUR'),
                   types.InlineKeyboardButton(text='BTC', callback_data='BTC'))

# Строчная клавиатура для выбора валют для конвертера
chose_currency_convert = types.InlineKeyboardMarkup(row_width=2)
chose_currency_convert.add(types.InlineKeyboardButton(text='UAH🇺🇦👉USD🇺🇸', callback_data='UAH USD'),
                           types.InlineKeyboardButton(
                               text='UAH🇺🇦👉RUR🇷🇺', callback_data='UAH RUR'),
                           types.InlineKeyboardButton(
                               text='UAH🇺🇦👉EUR🇪🇺', callback_data='UAH EUR'),
                           types.InlineKeyboardButton(
                               text='BTC💳👉USD🇺🇸', callback_data='BTC USD'),
                           types.InlineKeyboardButton(
                               text='USD🇺🇸👉UAH🇺🇦', callback_data='USD UAH'),
                           types.InlineKeyboardButton(
                               text='RUR🇷🇺👉UAH🇺🇦', callback_data='RUR UAH'),
                           types.InlineKeyboardButton(
                               text='EUR🇪🇺👉UAH🇺🇦', callback_data='EUR UAH'),
                           types.InlineKeyboardButton(text='USD🇺🇸👉BTC💳', callback_data='USD BTC'))

# Строчная клавиатура для выбора использования подписки на валюту
chose_currency_subscribe_use = types.InlineKeyboardMarkup(row_width=3)
chose_currency_subscribe_use.add(types.InlineKeyboardButton(text='>', callback_data='>'),
                                 types.InlineKeyboardButton(
                                     text='<', callback_data='<'),
                                 types.InlineKeyboardButton(text='=', callback_data='='))



# Строчная клавиатура для выбора покупки или продажи валюты
chose_buy_or_sell = types.InlineKeyboardMarkup(row_width=1)
chose_buy_or_sell.add(types.InlineKeyboardButton(text='Купівля', callback_data='Buy'),
                      types.InlineKeyboardButton(text='Продаж', callback_data='Sell'))

# Строчная клавиатура для выбора удаление или добавление подписки
chose_add_or_dell = types.InlineKeyboardMarkup(row_width=1)
chose_add_or_dell.add(types.InlineKeyboardButton(text='Додати', callback_data='add'),
                      types.InlineKeyboardButton(text='Видалити', callback_data='del'))

# Строчная клавиатура для выбора тип зачисления депозита
chose_deposit_type = types.InlineKeyboardMarkup(row_width=1)
chose_deposit_type.add(types.InlineKeyboardButton(text='Зарахування на депозитний рахунок', callback_data='on_deposit'),
                       types.InlineKeyboardButton(text='Зарахування на карту', callback_data='on_acc'))

add_sub_only=types.InlineKeyboardMarkup(row_width=1)
add_sub_only.add(types.InlineKeyboardButton(text='Додати', callback_data='add'))
