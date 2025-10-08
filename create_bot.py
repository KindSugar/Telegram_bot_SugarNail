from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import os
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
load_dotenv()  # Загружает переменные из .env файла

storage = MemoryStorage()

# Проверяем токен
TOKEN = os.getenv('BOT_TOKEN', '5229907022:AAEdqvhkr5LqyXmQd8eN5LNXMojE52hbHRs')

if not TOKEN:
    print("❌ Токен не найден!")
    exit(1)

# Проверяем формат токена
if ":" not in TOKEN:
    print("❌ Неверный формат токена!")
    exit(1)

print(f"✅ Токен получен: {TOKEN[:10]}...")

bot = Bot(token=TOKEN, default=DefaultBotProperties())
dp = Dispatcher(storage=storage)

print("✅ Бот инициализирован успешно!")
