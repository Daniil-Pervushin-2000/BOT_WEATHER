from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from database.for_users import search_tg_user

def start_menu(tg_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    user = search_tg_user(tg_id)
    if user is not None:
        markup.add(
            KeyboardButton(text='Узнать погоду'),
            KeyboardButton(text='История запросов')
        )
    else:
        markup.add(
            KeyboardButton(text='Регистрация')
    )
    return markup


def send_contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(text='Поделиться контактом', request_contact=True)
    )
    return markup