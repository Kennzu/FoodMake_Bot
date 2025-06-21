from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import logging

import src.services.users_couples as ucdb
import src.services.food_list_db as fld
import src.buttons.buttons as btn


def register_breakfast_handler(dp: Dispatcher):
    @dp.callback_query(F.data == "breakfast")
    async def choice_breakfast(callback: CallbackQuery, state: FSMContext):
        try:
            user_id = callback.from_user.id
            get_uuid = ucdb.get_uuid(user_id)

            if get_uuid != False:
                fld.db_manager.connect_db()
                breakfasts = fld.db_manager.select_breakfast(get_uuid) # Вот тут ты навоял изменения в метро. Сделал везде бигинт по couple_id а также кароч сделал более лучшее создание таблиц
                
                if not breakfasts:
                    await callback.message.answer("Пока нет блюд на завтрак", reply_markup=btn.back_button)
                    return

                builder = InlineKeyboardBuilder()

                for name_dish in breakfasts:
                    builder.add(InlineKeyboardButton(
                        text = name_dish['name'],
                        callback_data = f"btype_{name_dish['id']}"
                    ))
                    builder.adjust(3)

                await callback.message.answer("🍳 Доступные завтраки:", reply_markup=builder.as_markup())
            
            elif get_uuid == False:
                await callback.message.answer('''Упс... У вас еще нет пары (
Попробуйте сначала команду - /view_couple''')
        except Exception as e:
            logging.error(f"Ошибка: {e}")
            await callback.message.answer("Ошибка отображения", reply_markup=btn.back_button)
        finally:
            fld.db_manager.close()

    @dp.callback_query(F.data.startswith("btype_"))
    async def show_info_breakfast(callback: CallbackQuery):
        try:
            fld.db_manager.connect_db()
            type_id = int(callback.data.split("_")[1])
            logging.info(f"Тайпа какая-то при брекфасте{type_id}")
            table = "food_breakfast"
            dishes = fld.db_manager.one_dish_table(type_id, table)

            for item in dishes:
                dish_text = (
                    f"• {item['name']}\n"
                    f"Описание: {item.get('description', 'Не указано')}\n"
                    f"Калории: {item.get('calories', 'Не указано')}"
                )
                
                if item.get('image'):
                    try:
                        await callback.message.answer_photo(
                            item['image'],
                            caption=dish_text,
                            reply_markup=btn.change_button_breakfast
                        )
                    except Exception as e:
                        logging.error(f"Ошибка отправки фото завтрака: {e}")
                        await callback.message.answer(dish_text, reply_markup=btn.back_button_breakfast)
                else:
                    await callback.message.answer(dish_text, reply_markup=btn.change_button_breakfast)
                    
        except Exception as e:
            logging.error(f"Ошибка в show_info_breakfast: {e}")
            await callback.message.answer("Произошла ошибка при отображении завтрака")
        finally:
            fld.db_manager.close()