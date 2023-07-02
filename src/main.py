#main module
import json
import os
import time
from time import sleep, time
from datetime import datetime, timedelta
from requests import get
#telegram --------
from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
#----------------
""" импортируем наши модули """
# import modules.Emergency as Emergency
# import handlers.utils as utils
import keyboards
import database

from dotenv import load_dotenv
import telebot

load_dotenv()
bot_tokken = os.getenv('tokken')
Bot = telebot.TeleBot(bot_tokken)

@Bot.message_handler(commands=['id'])
def send_id(message):
    """ Обрабатываем текстовые сообщения '/id'. """
    if message.chat.type != 'private':
        Bot.send_message(message.chat.id, f"ID чата: {message.chat.id}")
    else:
        Bot.send_message(message.from_user.id, f"Ваш ID: {message.from_user.id}")

# Объявили ветку, в которой прописываем логику на тот случай, если пользователь решит прислать номер телефона :)
@Bot.message_handler(content_types=['contact'])
def contact(message):
    keybor
    user_id = message.from_user.id
    if get_status(user_id) == 0:  # Если status 0
        user_name = str(message.from_user.first_name)
        time_start = time()
        if message.contact is not None:  # Если присланный объект <strong>contact</strong> не равен нулю
            phone_num = message.contact.phone_number
            # print ("Ваш номер: " + phone_num) #debug
            my_number = utils.mob_format(phone_num)
            # Записываем данные в таблицу
            DataBase.set_user_id(user_id, user_name, my_number)
            text = f"Спасибо\nМы отправили СМС 📨 с кодом авторизации на \nВаш номер: {phone_num}"
            Bot.send_message(user_id, text, reply_markup=keyboard("DONE"))
            Bot.send_message(user_id, "Пожалуйста введите полученный код")
            my_data, my_log = USERauth.send_sms(phone_num, bot_name)
            try:
                data = json.loads(my_data)
            except ValueError as my_error:
                print(f"Ошибка: {my_error}")  # debug
                Bot.send_message(
                    user_id, "Что-то пошло не так!\nНажмите /start и начните сначала")
                time_stop = time()
                set_log(my_log, time_stop - time_start, user_id)  # log
                set_log_error(user_id,
                              message.from_user.full_name, my_log,
                              str(my_error), phone_num,
                              "my_data, my_log = USERauth.send_sms(phone_num, bot_name)",
                              time_stop - time_start)  # logError
                DataBase.set_flood(user_id, 0)  # возвращаем flood на 0
                return

            if data["success"] == False:
                Bot.send_message(user_id, data["message"])  # отправялем ошибку

            set_status(user_id, 1)  # Ставим статус 1 смс отправлен
            time_stop = time()
            set_log(my_log, time_stop - time_start, user_id)  # log
    else:
        Bot.send_message(user_id, "Я уже знаю ваш номер :)")

#обрабатываем нажатие кнопки start
@Bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Обрабатываем текстовые сообщения '/start' или '/help'"""
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name

    #user_status = get_status(user_id)  # получаем статус пользователя
    
    if DataBase.get_flood(user_id) == 111: # если пользователь заблокирован
        now = datetime.now()
        my_date = now.strftime("%d.%m.%Y %H:%M:%S")
        print(f"{my_date} | {user_full_name} | {user_id} | заблокированный пользователь")
        Bot.send_message(user_id, f"| {user_full_name} | Вы заблокированы!", reply_markup=keyboards.keyboard("DONE"))
        return
    
    # Проверяем наличие хоть какой-то дополнительной информации из ссылки
    if " " in message.text:
        referrer_candidate = message.text.split()[1]
        my_referal_cod, my_referrer = DataBase.get_my_referal_cod(
            user_id)  # получаем свой реферальный код

        if my_referal_cod == "Not Found":
            # Пробуем выполнить несколько условий
            try:
                # print (f"Рефералный код: {referer}") # печатает id реферала debug
                # записываем код в базу бота
                DataBase.set_referer_cod(user_id, referrer_candidate)
            except Exception as my_error:
                print(f"Ошибка: {my_error}")  # debug

        elif my_referrer != "0":  # проверяем что у пользователя reverrer пустой
            Bot.send_message(
                user_id,
                "Ошибка: Ранее Вы уже регистрировали реферальный код, повторная регистрация не возможна!"
            )
        else:
            # Пробуем выполнить несколько условий
            try:
                # проверяем, есть ли такой реферер в базе данных
                if my_referal_cod != referrer_candidate and referrer_candidate in DataBase.get_all_referal_cod():
                    referrer = referrer_candidate
                    # print (f"Рефералный код: {referer}") # печатает id реферала debug
                    # записываем код в базу бота
                    DataBase.update_referer_cod(user_id, referrer)
                else:
                    Bot.send_message(
                        user_id, "Ошибка: Такого кода нет либо вы ввели свой реферальный код.")
            except Exception as my_error:
                print(f"Ошибка: {my_error}")  # debug

    if user_status == 1:  # Если status 1, при нажатие на start
        # time_start = time()
        Bot.send_message(user_id, "Рады видеть вас снова!",
                         reply_markup=keyboard())  # Сообщение пользователю
        mob_nomer = DataBase.get_mob(user_id)
        text = f"Мы отправили СМС 📨 с кодом авторизации на \nВаш номер: {mob_nomer}"
        Bot.send_message(user_id, text, reply_markup=keyboard("DONE"))
        Bot.send_message(user_id, "Пожалуйста введите полученный код")
        my_data, my_log = USERauth.send_sms(mob_nomer, bot_name)
        try:
            data = json.loads(my_data)
        except ValueError as my_error:
            print(f"Ошибка: {my_error}")  # debug
            Bot.send_message(
                user_id, "Что-то пошло не так!\nНажмите /start и начните сначала")
            time_stop = time()
            set_log(my_log, time_stop - time_start, user_id)  # log
            set_log_error(
                user_id,
                user_full_name,
                my_log, f"{my_error}", message.contact,
                "my_data, my_log = USERauth.send_sms(mob_nomer, bot_name)",
                time_stop - time_start
            )  # logError
            DataBase.set_flood(user_id, 0)  # возвращаем flood на 0
            return

        time_stop = time()
        set_log(my_log, time_stop - time_start, user_id)  # log

    elif user_status == 2:  # Если status 2
        set_status(user_id, 3)  # устанавливаем статус 3
        Bot.send_message(
            user_id,
            f"Привет, {user_full_name} 👋\nРад видеть вас снова!\nНапишите пожалуйста Ваше ФИО",
            reply_markup=keyboard("Normal")
        )

    elif user_status == 3:  # Если status 3
        Bot.send_message(
            user_id,
            f"Привет, {user_full_name} 👋\nРад видеть вас снова!\nНапишите пожалуйста Ваше ФИО",
            reply_markup=keyboard("Normal")
        )

    elif user_status == 5:  # Если status 5
        Bot.send_message(
            user_id, f"Привет, {user_full_name} 👋\nРад видеть вас снова!")
        Bot.send_message(user_id, "Напишите, пожалуйста, дату рождения\nФормат: 01.01.2000",
                         reply_markup=keyboard("BIRTHDAY"))

    elif user_status >= 6:  # Если status 6 и больше
        if message.chat.type != 'private':
            Bot.send_message(
                message.chat.id, 
                f"Привет, {user_full_name} 👋\nЭто команда в общих чатах не обрабатывается!"
            )
        else:
            # удаляем сообщение пользователя
            Bot.delete_message(user_id, message.message_id)
            my_msg_id = DataBase.get_message_id_temp(
                user_id, 16)  # получаем id сообщений
            if my_msg_id:
                for msg in my_msg_id:
                    Bot.delete_message(user_id, msg)  # удаляем сообщения
            # удаляем все данные пользователя из базы temp
            DataBase.del_all_temp(user_id)
            DataBase.set_flood(user_id, 0)  # обнуляем flood статус
            set_status(user_id, 6)  # устанавливаем статус 6
            # удаляем темп данные автосервисов
            DataBase.del_carservice_info(user_id)
            Bot.send_message(
                user_id, f"Привет, {user_full_name} 👋\nРад видеть вас снова!", reply_markup=keyboard("MAIN"))
    else:
        my_text = (
            f"Здравствуйте, <b>{user_full_name}</b> 👋"
            "\nЯ бот для клиентов Вилгуд! 👻"
            "\nПохоже мы не знакомы 👀"
            "\nСейчас помогу вам зарегистрироваться 🔐"
            "\nНажмите пожалуйста на кнопку <b>Отправить номер</b>\n\n"
            f"Проходя регистрацию я даю согласние на <a href='https://wilgood.ru/upload/pdf/policy.pdf'>обработку персональных данных</a>"
        )
        Bot.send_message(user_id, my_text, reply_markup=keyboard(
            "CONTACT"), parse_mode="HTML")
        Bot.send_message(
            user_id, "Если не видите кнопку то просто нажмите на /send_phone")

# -----------------------------------------------------------------
Bot.delete_my_commands(scope=None, language_code=None)
Bot.set_my_commands(
    commands=[telebot.types.BotCommand("start", "🏠 Главное меню")],
)
# -----------------------------------------------------------------

# работает когда пользователь вводит любой текст НАЧАЛО всего
@Bot.message_handler(content_types=['text'], chat_types=['private'])
def handle_command(message):
    user_id = message.from_user.id
    user_status = get_status(user_id)  # получаем статус
    user_full_name = message.from_user.full_name
    if my_global_debug != 0:
        now = datetime.now()
        my_date = now.strftime("%d.%m.%Y %H:%M:%S")
        set_log_debug(user_id, user_full_name, "Написал", message.text, user_status)  
        print(f"{my_date} | {user_full_name} | {user_id} | Написал | {message.text} | Статус: {user_status}")
    # contact #?
    # MYsql.set_emergency(0) # Если все работает снимаем Emergency
    my_flood = DataBase.get_flood(user_id) # получаем статус flood
    if my_flood == 1:  # если пользователь не дождался предедущей команды
        Bot.send_message(
            user_id,
            "Не спишите пожалуйста, дождитесь выполнения предыдущего запроса!\n"
            "Если вы не отправляли запрос,\nнажмите 👉 /start и вернитесь в главное меню. "
        )
        return
    elif my_flood == 111: # блокируем пользователя
        now = datetime.now()
        my_date = now.strftime("%d.%m.%Y %H:%M:%S")
        print(f"{my_date} | {user_full_name} | {user_id} | заблокированный пользователь")
        Bot.send_message(user_id, f"| {user_full_name} | Вы заблокированы!", reply_markup=keyboard("DONE"))
        return
    
    time_start = time()
    # передаем сообщение пользователя и стартуем время
    #private.smart_reply(Bot, message, time_start, user_status, user_id, user_full_name)
    """ Обработка текстовых сообщений в личном чате с ботом """
    bot_name = Bot.get_me().username
    DataBase.set_flood(user_id, 1)  # устанавливаем защиту
    Bot.send_chat_action(user_id, "typing")  # отправляем акшен

    if message.text == "✅Done":
        Bot.send_message(user_id, "Done with Keyboard", reply_markup=keyboard("DONE"))
    elif message.text == "/test":
        Bot.send_message(user_id, "Все работает!")

# Bot.infinity_polling(timeout=120) #Непрекращающаяся прослушка наших чатов
try:
    # Bot.infinity_polling(timeout=120) #Непрекращающаяся прослушка наших чатов
    Bot.polling(none_stop=True, interval=0,  timeout=120)
except Exception as my_bot_error:
    print(f"Ошибка: {my_bot_error}")  # debug
    print("Bot упал отжался и встал")  # debug
    # отправляем сообщение админу
    Bot.send_message(2964812, f"Ошибка: {my_bot_error}")
    # Bot.send_message(2964812, "Bot упал отжался и встал") # отправляем сообщение админу
    sleep(20)