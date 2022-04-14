from aiogram import types, Dispatcher 
from create_bot import dp, bot 
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db

# @dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
	try:
	    await bot.send_message(message.from_user.id, 'Добро пожаловать!', reply_markup=kb_client)
	    await message.delete()
	except:
		await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Sugar_NailBot')

# @dp.message_handler(commands=['Режим_работы'])
async def nail_open_command(message : types.Message):
	await bot.send_message(message.from_user.id, 'Пн-Пт с 9:00 до 22:00, Сб-Вс с 10:00 до 22:00')
		
# @dp.message_handler(commands=['Расположение'])
async def nail_place_command(message : types.Message):
	await bot.send_message(message.from_user.id, 'ул. Ленина 26, вход со стороны улицы Ленина')

# @dp.message_handler(commands=['Контакты'])
async def nail_insta_command(message : types.Message):
	await bot.send_message(message.from_user.id, ' \nhttps://instagram.com/sugarnail_khv, \n 8-914-545-36-19')


@dp.message_handler(commands=['Прайс'])
async def nail_price_command(message : types.Message):
	await sqlite_db.sql_read(message)
	
def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(command_start, commands=['start', 'help'])
	dp.register_message_handler(nail_open_command, commands=['Режим_работы'])
	dp.register_message_handler(nail_place_command, commands=['Расположение'])
	dp.register_message_handler(nail_insta_command, commands=['Контакты'])
	dp.register_message_handler(nail_price_command, commands=['Прайс'] )


