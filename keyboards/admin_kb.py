from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_case_admin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Загрузить'), KeyboardButton(text='Удалить')],
        [KeyboardButton(text='Список услуг'), KeyboardButton(text='Отмена')],
        [KeyboardButton(text='Выйти из админа')] 
    ],
    resize_keyboard=True
)