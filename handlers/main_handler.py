import time
import requests
from telebot.types import Message, ReplyKeyboardRemove

from config import bot, URL, parameters
from database import add_data_user, add_data_request_user, search_tg_user, get_requests
from keyboards.default import start_menu, send_contact
from keyboards.inline import inline_questionnare, inline_menu


@bot.message_handler(commands=['start'])
def react_start(message: Message):
    chat_id = message.chat.id
    user_nickname = message.from_user.first_name
    bot.send_message(chat_id, f'Привет {user_nickname}, я бот, который поможет узнать погоду',
                     reply_markup=start_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == 'Регистрация')
def react_register(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Для регистрации, нужно ввести ФИО')
    bot.register_next_step_handler(message, get_fio)


def get_fio(message: Message):
    chat_id = message.chat.id
    fio = message.text
    bot.send_message(chat_id, 'Я получил ваше ФИО. Теперь отправьте свой контакт', reply_markup=send_contact())
    bot.register_next_step_handler(message, get_phone, fio)


def get_phone(message: Message, fio):
    chat_id = message.chat.id
    phone = message.contact.phone_number
    add_data_user(fio, phone, chat_id)
    bot.send_message(chat_id, 'Регистрация прошла успешно', reply_markup=start_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == 'Узнать погоду')
def react_btn_weather(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Введите имя города, у которого хотите узнать погоду')
    bot.register_next_step_handler(message, show_weather)


def show_weather(message: Message):
    chat_id = message.chat.id
    city_name = message.text
    try:
        parameters['q'] = city_name
        content = requests.get(url=URL, params=parameters).json()
        temp = content['main']['temp']
        temp_min = content['main']['temp_min']
        temp_max = content['main']['temp_max']
        feels_like = content['main']['feels_like']
        unix_time = time.time()
        request_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(unix_time))
        user_id = search_tg_user(chat_id)

        add_data_request_user(city_name, temp, temp_min, temp_max, feels_like, request_time, user_id[0])
        bot.send_message(chat_id, f'''
    В городе {city_name}
    Температура - {temp}
    Мин Температура - {temp_min}
    Макс Температура - {temp_max}
    По ощущениям - {feels_like}
    ''', reply_markup=inline_questionnare(request_time, user_id[0]))
    except Exception as error:
        print(error)
        bot.reply_to(message, f'Вы ввели неправильный город: {city_name}')


@bot.message_handler(func=lambda msg: msg.text == 'История запросов')
def react_btn_show_requests(message: Message):
    chat_id = message.chat.id
    user_id = search_tg_user(chat_id)
    message_id = message.message_id
    bot.send_message(chat_id, 'Ваши запросы', reply_markup=ReplyKeyboardRemove)
    text = 'Запросы \n'
    data = get_requests(user_id[0])
    for item in data:
        text += f'''
__________________
Номер: {item[0]}
В городе: {item[1]}
Температура: {item[2]}
Мин температура: {item[3]}
Макс температура: {item[4]}
По ощущениям температура: {item[5]}    
'''
    bot.send_message(chat_id, text, reply_markup=inline_menu(user_id[0], message_id))



