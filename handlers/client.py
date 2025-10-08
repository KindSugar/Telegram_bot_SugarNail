from aiogram import types, Dispatcher, F
from aiogram.filters import Command, CommandStart
from data_base import sqlite_db
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import ChatMemberUpdated


from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton(text='🕒 Режим работы')
b2 = KeyboardButton(text='📍 Расположение') 
b3 = KeyboardButton(text='📞 Контакты/запись')
b4 = KeyboardButton(text='💅 Прайс')

kb_client = ReplyKeyboardMarkup(
    keyboard=[
        [b1, b2],
        [b3, b4]
        
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder='Выберите действие...'
)

async def command_start(message: types.Message):
    try:
        await message.answer(
            '✨ Добро пожаловать в SugarNail! ✨\n\n'
            'Выберите интересующую вас информацию:', 
            reply_markup=kb_client
        )
    except Exception as e:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Sugar_NailBot')
        
async def test_cenz_command(message: types.Message):
    """Команда для тестирования цензуры"""
    test_info = (
        "🧪 <b>Тест цензуры</b>\n\n"
        "Отправьте любое сообщение с нецензурным словом для проверки.\n"
        "Используйте /test_cenz для подробной информации."
    )
    await message.answer(test_info, parse_mode='HTML')

# КОМАНДА ДЛЯ ПОЛУЧЕНИЯ ID 
async def get_my_id(message: types.Message):
    
    user_info = (
        f"👤 <b>Ваша информация:</b>\n"
        f"🆔 ID: <code>{message.from_user.id}</code>\n"
        f"👤 Имя: {message.from_user.first_name or 'Не указано'}\n"
        f"👥 Фамилия: {message.from_user.last_name or 'Не указана'}\n"
        f"🔗 Username: @{message.from_user.username or 'Не указан'}\n"
        f"💬 Язык: {message.from_user.language_code or 'Не указан'}"
    )
    await message.answer(user_info, parse_mode='HTML')
    await message.answer("📋 Скопируйте ваш ID и вставьте в файл admin.py", reply_markup=kb_client)

# Обработчики для текстовых кнопок
async def nail_open_command(message: types.Message):
    if message.text in ['🕒 Режим работы','🕒 Режим_работы', '/Режим_работы']:
        await message.answer(
            '🕒 <b>Режим работы:</b>\n'
            'Пн-Пт: с 10:00 до 20:00\n'
            'Сб : с 11:00 до 15:00\n'
            'Вс : ВЫХОДНОЙ\n\n'
            'Выберите следующую команду:', 
            reply_markup=kb_client,
            parse_mode='HTML'
        )

async def nail_place_command(message: types.Message):
    if message.text in ['📍 Расположение', '/Расположение']:
        await message.answer(
            '📍 <b>Расположение:</b>\n'
            'ул. Комсомольская 74, офис 305\n\n'
            'Выберите следующую команду:', 
            reply_markup=kb_client,
            parse_mode='HTML'
        )

async def nail_insta_command(message: types.Message):
    if message.text in ['📞 Контакты/запись', '/Контакты/запись']:
        await message.answer(
            '📞 <b>Контакты/запись:</b>\n'
            '📱 Instagram: https://instagram.com/sugarnail_khv\n'
            '☎️ Телефон: 8-914-545-36-19\n\n'
            'Выберите следующую команду:', 
            reply_markup=kb_client,
            parse_mode='HTML'
        )

async def nail_price_command(message: types.Message):
    if message.text in ['💅 Прайс', '/Прайс']:
        await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):

    dp.message.register(command_start, CommandStart())     
    dp.message.register(test_cenz_command, Command('test_cenzura'))
    dp.message.register(get_my_id, Command('myid'))  

    dp.message.register(nail_open_command, F.text.in_(['🕒 Режим работы', '🕒 Режим_работы', 'Режим_работы']))
    dp.message.register(nail_place_command, F.text.in_(['📍 Расположение', 'Расположение']))
    dp.message.register(nail_insta_command, F.text.in_(['📞 Контакты/запись', 'Контакты/запись']))
    dp.message.register(nail_price_command, F.text.in_(['💅 Прайс', 'Прайс']))
    
    dp.message.register(nail_open_command, Command('Режим_работы'))   
    dp.message.register(nail_place_command, Command('Расположение'))
    dp.message.register(nail_insta_command, Command('Контакты/запись'))
    dp.message.register(nail_price_command, Command('Прайс'))
