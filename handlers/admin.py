
from aiogram.filters import Command
from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from data_base import sqlite_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import admin_kb, kb_client

ADMIN_IDS = [879112769]  

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

async def make_changes_command(message: types.Message):
    print(f"🔍 Команда /moderator получена от пользователя {message.from_user.id}")
    print(f"🔍 Разрешенные ID: {ADMIN_IDS}")
    print(f"🔍 Клавиатура админа: {admin_kb.button_case_admin}")
    
    if message.from_user.id in ADMIN_IDS:
        print("✅ Пользователь является админом, показываем клавиатуру")
        try:
            await message.answer(
                '✅ Режим администратора активирован! Выберите действие:', 
                reply_markup=admin_kb.button_case_admin
            ) 
            print("✅ Клавиатура отправлена успешно")
        except Exception as e:
            print(f"❌ Ошибка при отправке клавиатуры: {e}")
            await message.answer('❌ Ошибка при активации админки')
    else:
        print(f"❌ Пользователь {message.from_user.id} не является админом")
        await message.answer('❌ У вас нет прав администратора.')

async def cm_start(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_IDS:
        await state.set_state(FSMAdmin.photo)
        await message.reply('Загрузи фото', reply_markup=admin_kb.button_case_admin)

async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_IDS:
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()
            print(f"🔵 Состояние FSM очищено для пользователя {message.from_user.id}")
        
        # ✅ ВАЖНО: После отмены остаемся в админ-панели
        await message.answer(
            '❌ Действие отменено. Вы в админ-панели.', 
            reply_markup=admin_kb.button_case_admin  # Оставляем админскую клавиатуру
        )
        print(f"🔵 Пользователь {message.from_user.id} остался в админ-панели")

async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_IDS:
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()
            print(f"🔵 Состояние FSM очищено для пользователя {message.from_user.id}")
        
        # ✅ ВАЖНО: После отмены остаемся в админ-панели
        await message.answer(
            '❌ Действие отменено. Вы в админ-панели.', 
            reply_markup=admin_kb.button_case_admin  # Оставляем админскую клавиатуру
        )
        print(f"🔵 Пользователь {message.from_user.id} остался в админ-панели")

async def exit_admin_mode(message: types.Message, state: FSMContext):
    """Выход из админ-панели и возврат к клиентскому меню"""
    if message.from_user.id in ADMIN_IDS:
        await state.clear()
        from keyboards.client_kb import kb_client  # Импортируем клиентскую клавиатуру
        
        await message.answer(
            '👋 Вы вышли из режима администратора. Возврат к основному меню.',
            reply_markup=kb_client
        )
        print(f"🔵 Пользователь {message.from_user.id} вышел из админ-панели")

async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_IDS:
        # Правильно получаем file_id
        file_id = message.photo[-1].file_id  # Берем самое качественное фото
        await state.update_data(photo=file_id)
        await state.set_state(FSMAdmin.name)
        await message.reply("Теперь введи название")

async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_IDS:
        await state.update_data(name=message.text)
        await state.set_state(FSMAdmin.description)
        await message.reply("Введи описание", reply_markup=admin_kb.button_case_admin)

async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_IDS:
        await state.update_data(description=message.text)
        await state.set_state(FSMAdmin.price)
        await message.reply("Укажи цену", reply_markup=admin_kb.button_case_admin)

async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_IDS:
        try:
            await state.update_data(price=message.text)
            data = await state.get_data()
            
            # ✅ Информация о дубликатах (не блокирующая)
            existing_records = await sqlite_db.check_existing_name(data['name'])
            if existing_records:
                await message.answer(
                    f"ℹ️ Уже есть услуга с названием '{data['name']}'\n"
                    f"Добавляем еще одну с таким же названием...",
                    reply_markup=admin_kb.button_case_admin
                )

            # ДЕБАГ: проверяем все данные перед сохранением
            print(f"🎯 Сохраняем в БД:")
            print(f"  📸 Photo: {data.get('photo', 'None')}")
            print(f"  📝 Name: {data.get('name', 'None')}")
            print(f"  📄 Description: {data.get('description', 'None')}")
            print(f"  💰 Price: {data.get('price', 'None')}")

            await sqlite_db.sql_add_command(state)
            await state.clear()
            await message.reply("✅ Услуга добавлена!", reply_markup=admin_kb.button_case_admin)
            
        except Exception as e:
            await message.answer(f"❌ Ошибка при добавлении: {e}", reply_markup=admin_kb.button_case_admin)
            await state.clear()

async def del_callback_run(callback_query: types.CallbackQuery):
    try:
        service_name = callback_query.data.replace('del ', '')
        await sqlite_db.sql_delete_command(service_name)
        await callback_query.answer(
            text=f'✅ Одна из услуг "{service_name}" удалена.',  # Измените текст
            show_alert=True
        )
        
        # Обновляем сообщение
        await callback_query.message.edit_text(
            f"Одна из услуг '{service_name}' была удалена",
            reply_markup=None
        )
        
    except Exception as e:
        await callback_query.answer(
            text=f'❌ Ошибка: {str(e)}', 
            show_alert=True
        )

async def delete_item(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        try:
            read = await sqlite_db.sql_read2()
            
            if not read:
                await message.answer("❌ В прайсе нет услуг для удаления")
                return
                
            for ret in read:
                if ret[0]:  # Если есть валидное фото
                    await message.answer_photo(
                        ret[0], 
                        caption=f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}'
                    )
                else:
                    await message.answer(
                        f'📷 [Изображение недоступно]\n{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}'
                    )
                
                await message.answer(
                    text='^^^', 
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f"Удалить {ret[1]}", callback_data=f'del {ret[1]}')]
                    ])
                )
            
            await message.answer('Выберите дальнейшее действие:', reply_markup=admin_kb.button_case_admin)
            
        except Exception as e:
            print(f"❌ Ошибка при выводе прайса: {e}")
            await message.answer('❌ Ошибка при загрузке списка услуг')

async def show_existing_services(message: types.Message):
    """Показывает существующие услуги"""
    if message.from_user.id in ADMIN_IDS:
        try:
            records = await sqlite_db.sql_read2()
            
            if not records:
                await message.answer("📭 В прайсе пока нет услуг")
                return
            
            services_list = "📋 Существующие услуги:\n\n"
            for i, ret in enumerate(records, 1):
                services_list += f"{i}. {ret[1]} - {ret[3]} руб.\n"
            
            await message.answer(services_list, reply_markup=admin_kb.button_case_admin)
            
        except Exception as e:
            await message.answer(f"❌ Ошибка: {e}")

def register_handlers_admin(dp: Dispatcher):
    dp.message.register(make_changes_command, Command('moderator'))
    dp.message.register(cm_start, F.text == 'Загрузить', F.from_user.id.in_(ADMIN_IDS)) 
    dp.message.register(delete_item, F.text == 'Удалить', F.from_user.id.in_(ADMIN_IDS)) 
    dp.message.register(cancel_handler, F.text.casefold() == 'отмена', F.from_user.id.in_(ADMIN_IDS))
    dp.message.register(load_photo, F.photo, F.from_user.id.in_(ADMIN_IDS), FSMAdmin.photo)
    dp.message.register(load_name, F.from_user.id.in_(ADMIN_IDS), FSMAdmin.name)
    dp.message.register(load_description, F.from_user.id.in_(ADMIN_IDS), FSMAdmin.description)
    dp.message.register(load_price, F.from_user.id.in_(ADMIN_IDS), FSMAdmin.price)
    dp.callback_query.register(del_callback_run, F.data.startswith('del '))
    dp.message.register(show_existing_services, F.text == 'Список услуг', F.from_user.id.in_(ADMIN_IDS))
    dp.message.register(exit_admin_mode, F.text == 'Выйти из админа', F.from_user.id.in_(ADMIN_IDS))
   