from aiogram import types
from aiogram.types import ReplyKeyboardMarkup


def initial_keyboard():
    start_buttons = ['👶Указать возраст']

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    return keyboard


def main_keyboard():
    first_line = ['Профиль', 'Библиотека']
    second_line = ['Помочь советом', 'Связь']

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*first_line).add(*second_line)

    return keyboard


def profile_keyboard():
    first_line = ['Изменить имя', 'Изменить дату рождения']
    second_line = ['Назад']

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*first_line).add(*second_line)

    return keyboard

def change_name_keyboard():
    first_line = ['Изменить имя', 'Назад']

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*first_line)