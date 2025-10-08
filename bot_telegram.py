import asyncio
import logging
from create_bot import bot, dp
from data_base import sqlite_db
from aiogram import Bot, Dispatcher
from handlers import client, admin, other

logging.basicConfig(level=logging.INFO)

async def main():
#     # Инициализация базы данных
    sqlite_db.sql_start()
    
#     # Очистка бинарных данных (закомментируйте если вызывает ошибки)
#     try:
#         await sqlite_db.cleanup_binary_photos()
#     except Exception as e:
#         print(f"⚠️ Ошибка при очистке бинарных данных: {e}")

    print('Бот ONLINE')
    
    print("Регистрируем хендлеры...")

    admin.register_handlers_admin(dp) 
    client.register_handlers_client(dp)
    other.register_handlers_other(dp)

    print("Запускаем бота...")
    
    # Убедитесь, что предыдущий экземпляр бота остановлен
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")

