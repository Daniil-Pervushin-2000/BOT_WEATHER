from config import bot

from telebot.types import CallbackQuery, ReplyKeyboardRemove
from database.for_users import update_table_correctly, delete_requests
from keyboards.default import start_menu


@bot.callback_query_handler(func=lambda call: 'true' in call.data)
def react_true(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, dt_request, user_id = callback.data.split('_')
    update_table_correctly(True, dt_request, user_id)
    bot.answer_callback_query(callback.id, 'Рад вам служить')


@bot.callback_query_handler(func=lambda call: 'false' in call.data)
def react_fals(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, dt_request, user_id = callback.data.split('_')
    update_table_correctly(False, dt_request, user_id)
    bot.answer_callback_query(callback.id, 'Прошу меня понять и простить')


@bot.callback_query_handler(func=lambda call: 'delete' in call.data)
def react_delete(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, user_id, message_id = callback.data.split('_')
    delete_requests(int(user_id))
    bot.delete_message(chat_id, message_id=message_id)
    bot.answer_callback_query(callback.id, 'Ваши запросы удалены')


@bot.callback_query_handler(func=lambda call: 'delete' in call.data)
def react_delete(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.send_message(chat_id, 'Хорошо', reply_markup=start_menu(chat_id))