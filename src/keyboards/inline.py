""" Модуль для клавиатуры БОТа """
from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton)

def inline_button(key_type):
    markup = InlineKeyboardMarkup()
    #markup.row_width = 1
    if key_type == "change_city":
        markup.add(InlineKeyboardButton(
                   "⚙️ Сменить Город обслуживания ", callback_data="edit-city_nocoordinates"))
    elif key_type == "start":
        markup.add(InlineKeyboardButton(
                   "⬅️ Вернутся в главное меню", callback_data="start_start"))
    elif key_type == "edit":
        markup.add(InlineKeyboardButton(
                   "⚙️ Редактировать", callback_data="edit_edit"))
    elif key_type =="select_brand":
        markup.add(InlineKeyboardButton(
                   "Выбрать из всех возможных", callback_data="select_brand"))
    elif key_type == "yes_no":
        markup.row_width = 2
        markup.add(
            InlineKeyboardButton("Да", callback_data="cb_yes"),
            InlineKeyboardButton("Нет", callback_data="cb_no")
        )
    return markup