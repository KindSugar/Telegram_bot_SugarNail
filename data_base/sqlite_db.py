import sqlite3 as sq
import asyncio 

def sql_start():
    global base, cur
    base = sq.connect('nail_cool.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    # Новая структура таблицы с автоинкрементным ID
    base.execute('''
        CREATE TABLE IF NOT EXISTS price(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            img TEXT, 
            name TEXT, 
            description TEXT, 
            price TEXT
        )
    ''')
    base.commit()

async def check_existing_name(name):
    """Проверяет, существует ли услуга с таким названием"""
    try:
        cur.execute('SELECT name FROM price WHERE name = ?', (name,))
        return cur.fetchone() is not None
    except Exception as e:
        print(f"❌ Ошибка при проверке имени: {e}")
        return False

async def sql_add_command(state):
    try:
        data = await state.get_data()
        print(f"🔍 Данные для добавления в БД:")
        print(f"  Photo: {data.get('photo', 'None')}")
        print(f"  Name: {data.get('name', 'None')}") 
        print(f"  Description: {data.get('description', 'None')}")
        print(f"  Price: {data.get('price', 'None')}")
        
        # Извлекаем данные из состояния
        photo = data.get('photo', '')
        name = data.get('name', '')
        description = data.get('description', '')
        price = data.get('price', '')
        
        # Явно указываем порядок колонок при вставке
        cur.execute('INSERT INTO price (img, name, description, price) VALUES (?, ?, ?, ?)', 
                    (photo, name, description, price))
        base.commit()
        print("✅ Данные успешно записаны в БД")
        
    except Exception as e:
        print(f"❌ Ошибка в sql_add_command: {e}")
        raise e
        
async def sql_read(message):
    from create_bot import bot
    from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
    import asyncio
    
    # Создаем клавиатуру
    b1 = KeyboardButton(text='🕒 Режим работы')
    b2 = KeyboardButton(text='📍 Расположение')
    b3 = KeyboardButton(text='📞 Контакты/запись')
    b4 = KeyboardButton(text='💅 Прайс')
    
    kb_menu = ReplyKeyboardMarkup(
        keyboard=[[b1, b2], [b3, b4]], 
        resize_keyboard=True
    )
    
    try:
        records = await sql_read2()
        
        if not records:
            await message.answer('📭 Прайс пуст', reply_markup=kb_menu)
            return
            
        sent_count = 0
        for ret in records:
            try:
                caption = f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[3]}'
                
                if ret[0]:  # Если есть file_id
                    print(f"🖼️ Отправляю фото для: {ret[1]}")
                    await message.answer_photo(ret[0], caption=caption)
                    print(f"✅ Фото отправлено успешно")
                else:
                    # Отправляем только текст
                    print(f"📝 Отправляю текст для: {ret[1]} (нет фото)")
                    await message.answer(f'📷 {caption}')
                
                sent_count += 1
                await asyncio.sleep(0.3)
                
            except Exception as e:
                print(f"❌ Ошибка отправки {ret[1]}: {e}")
                try:
                    await message.answer(f'❌ Ошибка загрузки: {ret[1]}\n{ret[2]}\nЦена: {ret[3]}')
                    sent_count += 1
                except:
                    pass
        
        # if sent_count > 0:
        #     await message.answer(f'✅ Показано услуг: {sent_count}', reply_markup=kb_menu)
        # else:
        #     await message.answer('❌ Не удалось загрузить прайс', reply_markup=kb_menu)
            
    except Exception as e:
        print(f"❌ Общая ошибка при выводе прайса: {e}")
        await message.answer("❌ Произошла ошибка при загрузке прайса", reply_markup=kb_menu)

async def sql_read2():
    """Читает все услуги из базы"""
    try:
        records = cur.execute('SELECT * FROM price').fetchall()
        read_data = []
        
        print(f"📊 Чтение {len(records)} записей из БД:")
        
        for i, ret in enumerate(records):
            print(f"\n🔍 Запись {i+1}:")
            print(f"   ID: {ret[0]}")
            print(f"   Img: {ret[1][:50] if ret[1] else 'None'}...")
            print(f"   Name: {ret[2]}")
            print(f"   Description: {ret[3][:50] if ret[3] else 'None'}...")
            print(f"   Price: {ret[4]}")
            
            try:
                # ПРОСТАЯ ПРОВЕРКА
                photo_data = ret[1] if ret[1] and isinstance(ret[1], str) else None
                
                read_data.append([
                    photo_data,  # img (photo)
                    ret[2] if len(ret) > 2 else '',  # name
                    ret[3] if len(ret) > 3 else '',  # description  
                    ret[4] if len(ret) > 4 else ''   # price
                ])
                
            except Exception as e:
                print(f"⚠️ Ошибка обработки записи: {e}")
                read_data.append([None, ret[2], ret[3], ret[4]])
        
        print(f"\n✅ Итог: {len(read_data)} записей обработано")
        return read_data
        
    except Exception as e:
        print(f"❌ Критическая ошибка при чтении из БД: {e}")
        return []

async def sql_delete_command(name):
    """Удаляет услугу по названию (теперь может быть несколько с одинаковым названием)"""
    try:
        # Проверяем, существует ли такая услуга
        cur.execute('SELECT id FROM price WHERE name = ?', (name,))
        services = cur.fetchall()
        
        if not services:
            raise Exception(f"Услуга с названием '{name}' не найдена!")
        
        if len(services) > 1:
            # Если несколько услуг с таким названием, показываем предупреждение
            print(f"⚠️ Найдено {len(services)} услуг с названием '{name}', удаляем первую")
        
        # Удаляем первую найденную услугу с таким названием
        cur.execute('DELETE FROM price WHERE name = ? LIMIT 1', (name,))
        base.commit()
        print(f"✅ Услуга '{name}' удалена")
        return True
    except Exception as e:
        print(f"❌ Ошибка при удалении: {e}")
        raise e
    
async def cleanup_binary_data():
    """Очищает бинарные данные из базы"""
    try:
        records = cur.execute('SELECT * FROM price').fetchall()
        cleaned_count = 0
        
        for ret in records:
            if ret[0] and (not isinstance(ret[0], str) or len(ret[0]) < 10):
                # Очищаем бинарные данные
                cur.execute('UPDATE price SET img = NULL WHERE name = ?', (ret[1],))
                cleaned_count += 1
                print(f"🧹 Очищена запись: {ret[1]}")
        
        if cleaned_count > 0:
            base.commit()
            print(f"✅ Очищено {cleaned_count} записей с бинарными данными")
        
        return cleaned_count
        
    except Exception as e:
        print(f"❌ Ошибка при очистке бинарных данных: {e}")
        return 0

# Функция для очистки бинарных данных из базы
async def cleanup_binary_photos():
    """Безопасная очистка бинарных данных"""
    try:
        print("🔧 Начало очистки бинарных данных...")
        
        # Просто устанавливаем все фото в NULL
        cur.execute("UPDATE price SET img = NULL WHERE img IS NOT NULL")
        affected = cur.rowcount
        
        base.commit()
        print(f"✅ Очищено {affected} записей с фото")
        
        return affected
    except Exception as e:
        print(f"❌ Ошибка при очистке: {e}")
        return 0