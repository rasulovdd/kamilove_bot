""" Модуль для клавиатуры БОТа """
from telebot.types import (KeyboardButton, ReplyKeyboardMarkup, 
                           ReplyKeyboardRemove)

def keyboard(key_type="Normal"):
    """ Функция для создание клавиатуры."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if key_type == "Normal":
        markup.add(KeyboardButton("ℹ Информация"), KeyboardButton("Обновить"))
    elif key_type == "BONUS":
        markup.add(KeyboardButton("История начислений"),
                   KeyboardButton("Перевод бонусов"))
        markup.add(KeyboardButton("⬅️ Главное меню"),
                   KeyboardButton("Получить больше"))
        markup.add(KeyboardButton("Условия бонусной программы"))
    elif key_type == "CANCEL":
        markup.add(KeyboardButton("Отменить"))
    elif key_type == "MAIN":
        markup.add(KeyboardButton("👨‍💻 Обо мне"),
                   KeyboardButton("✍🏻 Запись на сервис"))
        markup.add(KeyboardButton("🎁 Мои бонусы"),
                   KeyboardButton("🚘 Мои авто"))
        markup.add(KeyboardButton("💥 Акции"), KeyboardButton("🏷️ Купоны"))
        markup.add(KeyboardButton("📱 Заказать обратный звонок"))
    elif key_type == "MYAUTO":
        markup.add(KeyboardButton("⬅️ Главное меню"),
                   KeyboardButton("Добавить авто"))
    elif key_type == "ORDERS":
        markup.add(KeyboardButton("Записаться"),
                   KeyboardButton("Текущие записи"))
        markup.add(KeyboardButton("⬅️ Главное меню"),
                   KeyboardButton("История записей"))
    elif key_type == "REG":
        markup.add(KeyboardButton("ℹ Информация"),
                   KeyboardButton("Добавить авто"))
        markup.add(KeyboardButton("Добавить дату рождения"))
    elif key_type == "NOTIFICATIONS":
        markup.add(KeyboardButton("Добавить"),
                   KeyboardButton("Показать список"))
        markup.add(KeyboardButton("Отменить"))
    elif key_type == "CONTACT":
        # button_phone = types.KeyboardButton(
        #     text="Отправить телефон", request_contact=True)
        markup.add(KeyboardButton(
            text="Отправить телефон", request_contact=True))
    elif key_type == "GEO":
        markup.add(KeyboardButton(
            text="Поделиться с местоположением", request_location=True))
    elif key_type == "GEO_NEXT":
        markup.add(KeyboardButton(
            text="📍 Поделиться с местоположением", request_location=True))
        markup.add(KeyboardButton("Пропустить"))
    elif key_type == "BIRTHDAY":
        markup.add(KeyboardButton("❌ Пропустить"))
    elif key_type == "BACK":
        markup.add(KeyboardButton("⬅️ Главное меню"))
    elif key_type == "FEEDBACK":
        markup.add(KeyboardButton("❌ Пропустить"))
    elif key_type == "DONE":
        markup = ReplyKeyboardRemove()
    return markup
