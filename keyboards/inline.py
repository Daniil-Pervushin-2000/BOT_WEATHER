from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_questionnare(dt_request, user_id):
    inline = InlineKeyboardMarkup()
    inline.add(
        InlineKeyboardButton(text='Правильно', callback_data=f'true_{dt_request}_{user_id}'),
        InlineKeyboardButton(text='Неправильно', callback_data=f'false_{dt_request}_{user_id}')
    )
    return inline


def inline_menu(user_id, message_id):
    inline = InlineKeyboardMarkup()
    inline.add(
      InlineKeyboardButton(text='Удалить все запросы', callback_data=f'delete_{user_id},_{message_id}'),
      InlineKeyboardButton(text='Назад', callback_data='back')
    )
    return inline