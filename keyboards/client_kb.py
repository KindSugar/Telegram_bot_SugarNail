from aiogram import types, Dispatcher 
from aiogram.filters import Command
from create_bot import bot 
from data_base import sqlite_db
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Создаем кнопки
b1 = KeyboardButton(text='🕒 Режим_работы')
b2 = KeyboardButton(text='📍 Расположение')
b3 = KeyboardButton(text='📞Контакты/запись')
b4 = KeyboardButton(text='💅 Прайс')

# Создаем клавиатуру
kb_client = ReplyKeyboardMarkup(
    keyboard=[
        [b1, b2],
        [b3, b4]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


def register_handlers_client(dp: Dispatcher):
    dp.message.register(command_start, Command(commands=['start', 'help']))
    dp.message.register(nail_open_command, Command(commands=['Режим_работы']))
    dp.message.register(nail_place_command, Command(commands=['Расположение']))
    dp.message.register(nail_insta_command, Command(commands=['Контакты/запись']))
    dp.message.register(nail_price_command, Command(commands=['Прайс']))