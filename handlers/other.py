import asyncio
import json
import string
from aiogram import types, Dispatcher, F
from aiogram.filters import Command

# Загружаем список запрещенных слов
try:
    with open('cenzura.json', 'r', encoding='utf-8') as f:
        BAD_WORDS = set(json.load(f))
    print(f"✅ Загружено {len(BAD_WORDS)} запрещенных слов")
except (FileNotFoundError, json.JSONDecodeError):
    print("❌ Ошибка загрузки cenzura.json")
    BAD_WORDS = set()

async def check_bad_words(message: types.Message):
    # Пропускаем команды (начинаются с /)
    if message.text and message.text.startswith('/'):
        return
    
    # Пропускаем сообщения без текста
    if not message.text:
        return
    
    # ✅ ВАЖНО: Полный список ВСЕХ кнопок бота
    all_bot_buttons = [
        # Клиентские кнопки
        '🕒 Режим работы', '🕒 Режим_работы', 'Режим_работы',
        '📍 Расположение', 'Расположение',
        '📞 Контакты/запись', 'Контакты/запись', 
        '💅 Прайс', 'Прайс',
        # Админские кнопки  
        'Загрузить', 'Удалить', 'Отмена', 'Список услуг', 'Выйти из админа'
    ]
    
    if message.text in all_bot_buttons:
        print(f"🔵 Пропускаем кнопку бота: {message.text}")
        return
    
    # ✅ Также пропускаем сообщения, которые являются ответами на кнопки
    if any(button_text in message.text for button_text in ['Режим работы', 'Расположение', 'Контакты', 'Прайс', 'Загрузить', 'Удалить']):
        print(f"🔵 Пропускаем текст с названием кнопки: {message.text}")
        return
    
    print(f"🔍 Проверяем сообщение на цензуру: {message.text}")
    
    # Остальной код проверки цензуры...
    translator = str.maketrans('', '', string.punctuation + '1234567890')
    clean_text = message.text.translate(translator).lower()
    
    words = clean_text.split()
    found_bad_words = []
    
    for word in words:
        if word in BAD_WORDS:
            found_bad_words.append(word)
    
    for bad_word in BAD_WORDS:
        if bad_word in clean_text and bad_word not in found_bad_words:
            if f" {bad_word} " in f" {clean_text} ":
                found_bad_words.append(bad_word)
    
    if found_bad_words:
        print(f"🚫 Найдены запрещенные слова: {found_bad_words}")
        try:
            await message.delete()
            warning_msg = await message.answer("❌ Использование нецензурной лексики запрещено!")
            await asyncio.sleep(5)
            await warning_msg.delete()
        except Exception as e:
            await message.answer("❌ Сообщение содержит запрещенные слова!")

# Команда для тестирования цензуры
async def test_cenzura(message: types.Message):
    """Тестовая команда для проверки работы цензуры"""
    test_text = "Проверка работы цензуры. Отправьте сообщение с плохим словом для теста."
    
    if BAD_WORDS:
        sample_words = list(BAD_WORDS)[:3]
        test_text += f"\n\nПример запрещенных слов: {', '.join(sample_words)}"
    
    await message.answer(test_text)

async def show_bad_words(message: types.Message):
    """Показать количество запрещенных слов"""
    await message.answer(f"📊 Загружено {len(BAD_WORDS)} запрещенных слов")

def register_handlers_other(dp: Dispatcher):
    # ✅ ВАЖНО: Цензура регистрируется ПОСЛЕДНЕЙ с низким приоритетом
    dp.message.register(check_bad_words, F.text)
    
    # Тестовые команды
    dp.message.register(test_cenzura, Command('test_cenz'))
    dp.message.register(show_bad_words, Command('bad_words'))
    
    print("✅ Хендлеры цензуры зарегистрированы (низкий приоритет)")