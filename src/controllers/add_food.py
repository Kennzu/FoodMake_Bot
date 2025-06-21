from aiogram import Dispatcher, F
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

# system imports
import logging

# path function imports
import src.buttons.buttons as btn
import src.services.food_list_db as fld
import src.services.users_couples as ucdb
import src.dto.statements_food as stts

def register_add_food_handlers(dp: Dispatcher):
    @dp.callback_query(F.data == "add_food")
    async def add_food(callback: CallbackQuery):
        try:
            user_id = callback.from_user.id
            check_couple = ucdb.check_couples(user_id)

            match check_couple:
                case False:
                    await callback.message.answer('''
Что-то не так с парой! 
Попробуйте для начала команду - /view_couple''')
            await callback.message.answer('''
Отлично! Давай добавим новое блюдо)
Вот инструкция для добавления нового блюда:

Иди строго по следующим шагам:
- Выбери тип блюда (Завтрак, обед, ужин)
- Добавь название блюда
- Добавь описание (Если нужно)
- Добавь Калории (Если нужно)
- Добавь фото

После, данное блюдо появится в выборах!''', reply_markup=btn.go_button)
        
        except Exception as e:
            logging.error(f"Ошибка при выборе добавления блюда {e}")
    
    @dp.callback_query(F.data == "go")
    async def type_of_food(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        kb_type = ReplyKeyboardMarkup(
            keyboard=btn.type_of_food_button,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Выберите тип:"
        )

        await callback.message.answer('''Окей, давай начнем с типа блюда:''', reply_markup=kb_type)
        await state.set_state(stts.States.type_food)

    @dp.message(stts.States.type_food)
    async def name_food(msg: Message, state: FSMContext):
        await msg.answer('''Теперь введите название блюда:''')
        await state.update_data(type_food = msg.text)
        await state.set_state(stts.States.name_food)

    @dp.message(stts.States.name_food)
    async def description_food(msg: Message, state: FSMContext):
        kb_description = ReplyKeyboardMarkup(
            keyboard=btn.skip_button,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Напиши самостоятельно или выбери (Пропустить)"
        )
        await msg.answer('''Найс, давай теперь напишем описание блюда (Необязательное поле)''', reply_markup=kb_description)
        await state.update_data(name_food = msg.text)
        await state.set_state(stts.States.description_food)

    @dp.message(stts.States.description_food, F.text.lower() == "пропустить")
    async def notPS_calories_food(msg: Message, state: FSMContext):
        kb_calories = ReplyKeyboardMarkup(
            keyboard=btn.skip_button,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Напиши самостоятельно или выбери (Пропустить)"
        )
        await msg.answer('''Что ж... Обойдемся без описания! Будешь добавлять калории к блюду? 
Если да, то просто пиши сумму (Необязательное поле)''', reply_markup=kb_calories)
        await state.update_data(description_food = msg.text)
        await state.set_state(stts.States.calories_food)

    @dp.message(stts.States.description_food)
    async def calories_food(msg: Message, state: FSMContext):
        kb_calories = ReplyKeyboardMarkup(
            keyboard=btn.skip_button,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Напиши самостоятельно или выбери (Пропустить)"
        )
        await msg.answer('''Будешь добавлять калории к блюду? 
Если да, то просто пиши сумму (Необязательное поле)''', reply_markup=kb_calories)
        await state.update_data(description_food = msg.text)
        await state.set_state(stts.States.calories_food)

    @dp.message(stts.States.calories_food)
    async def notPS_photo_food(msg: Message, state: FSMContext):
        await msg.answer('''Остался последний шаг! Добавь фото блюда, чтобы слюнки текли от вида)''')
        await state.update_data(calories_food = msg.text)
        await state.set_state(stts.States.photo_food)

    @dp.message(stts.States.calories_food, F.text.lower() == "пропустить")
    async def notPS_photo_food(msg: Message, state: FSMContext):
        await msg.answer('''Ну раз не считаете калории...
Остался последний шаг! Добавь фото блюда, чтобы слюнки текли от вида)''')
        await state.update_data(calories_food = msg.text)
        await state.set_state(stts.States.photo_food)

    @dp.message(stts.States.photo_food, F.photo)
    async def result_add_food(msg: Message, state: FSMContext):
        data = await state.get_data()
        photo_file_id = msg.photo[-1].file_id
        
        # Сохраняем только file_id
        await state.update_data(photo_file_id=photo_file_id)
        
        def format_field(value):
            if value is None or value == "Пропустить":
                return "Не указано"
            return value
        
        response = f"""Вот результат:
Тип: {format_field(data.get('type_food'))}
Название: {format_field(data.get('name_food'))}
Описание: {format_field(data.get('description_food'))}
Калории: {format_field(data.get('calories_food'))}"""
        
        await msg.answer_photo(
            photo_file_id,
            caption=response + "\n\nДобавляем блюдо?",
            reply_markup=btn.approve_button
        )

    @dp.callback_query(F.data == "approve")
    async def add_food_to_db(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        user_id = callback.from_user.id
        get_uuid = ucdb.get_uuid(user_id)

        dish_data = {
            'type': data.get('type_food'),
            'name': data.get('name_food'),
            'description': None if data.get('description_food') in [None, "Пропустить"] else data.get('description_food'),
            'calories': None if data.get('calories_food') in [None, "Пропустить"] else int(data.get('calories_food')),
            'photo': data.get('photo_file_id')  # Только file_id
        }
        
        try:
            fld.db_manager.connect_db()
            if dish_data['type'] == "Завтрак":
                fld.db_manager.add_breakfast(dish_data, get_uuid)
            elif dish_data['type'] == "Обед":
                fld.db_manager.add_lanch(dish_data, get_uuid)
            else:
                fld.db_manager.add_dinner(dish_data, get_uuid)
                
            await callback.message.delete()
            await callback.message.answer("Блюдо успешно добавлено!", reply_markup=btn.back_button)
        except Exception as e:
            logging.error(f"Ошибка при добавлении в БД: {e}")
            await callback.message.answer("Произошла ошибка при сохранении блюда")
        finally:
            fld.db_manager.close()
            await state.clear()
