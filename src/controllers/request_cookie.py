from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

# system imports
import logging
from main import bot

# path function imports
import src.buttons.buttons as btn
import src.services.users_db as udb
import src.services.users_couples as ucdb
import src.dto.statements_message as sttsm

def register_request_cookie_handlers(dp: Dispatcher):
    @dp.callback_query(F.data == "change_dish")
    async def change_dish(callback: CallbackQuery):
        user_id = callback.from_user.id
        message = callback.message
        nickname = udb.select_user(user_id)
        get_users_from_couple = ucdb.get_couple(user_id)


        dish_name = message.caption.split('\n')[0][2:] if message.caption else "Неизвестное блюдо"
        dish_description = next((line.split(': ')[1] for line in message.caption.split('\n') 
                                if line.startswith("Описание:")), "Нет описания") if message.caption else "Нет описания"
        dish_calories = next((line.split(': ')[1] for line in message.caption.split('\n') 
                                if line.startswith("Калории:")), "Не указано") if message.caption else "Не указано"


        if callback.from_user.id == get_users_from_couple[2]:
            await callback.message.answer(f"Вы отправили запрос на покушать , скоро ваша вторая половинка увидит!")
            await bot.send_photo(
    chat_id=get_users_from_couple[3], 
    photo=message.photo[-1].file_id,
    caption=f'''{nickname[0][3]} запросил у вас следующее блюдо:

<b>{dish_name}</b>
Описание: {dish_description}
Калории: {dish_calories}

Готовим?
    ''', reply_markup=btn.approve_cookie_button, parse_mode=ParseMode.HTML)
            
        elif callback.from_user.id == get_users_from_couple[3]:
            await callback.message.answer(f"Вы отправили запрос на покушать , скоро ваша вторая половинка увидит!")
            await bot.send_photo(
    chat_id=get_users_from_couple[2], 
    photo=message.photo[-1].file_id,
    caption=f'''{nickname[0][3]} запросил у вас следующее блюдо:

<b>{dish_name}</b>
Описание: {dish_description}
Калории: {dish_calories}

Готовим?
    ''', reply_markup=btn.approve_cookie_button, parse_mode=ParseMode.HTML)
        
    @dp.callback_query(F.data == "approve_cookie")
    async def response_message(callback: CallbackQuery):
        user_id = callback.from_user.id
        nickname = udb.select_user(user_id)
        get_users_from_couple = ucdb.get_couple(user_id)

        if callback.from_user.id == get_users_from_couple[2]:
            await bot.send_message(
                chat_id=get_users_from_couple[3],
                text=f'''{nickname[0][3]} подтвердил запрос'''
            )
            await bot.send_message(
                chat_id=get_users_from_couple[2],
                text='''Вы подтвердили запрос, уведомление отправлено!'''
            )
        elif callback.from_user.id == get_users_from_couple[3]:
            await bot.send_message(
                chat_id=get_users_from_couple[2],
                text=f'''{nickname[0][3]} подтвердил запрос'''
            )
            await bot.send_message(
                chat_id=get_users_from_couple[3],
                text='''Вы подтвердили запрос, уведомление отправлено!'''
            )

    @dp.callback_query(F.data == "reject_cookie")
    async def response_reject_message(callback: CallbackQuery, state: FSMContext):
        await state.set_state(sttsm.States.reject_message)
        await callback.message.reply('''Отправьте сообщение почему вы отказались готовить блюдо: ''')

    @dp.message(sttsm.States.reject_message)
    async def response_reject_user(msg: Message, state: FSMContext):
        # Сначала сохраняем сообщение в state
        await state.update_data(reject_message=msg.text)

        user_id = msg.from_user.id
        nickname = udb.select_user(user_id)
        get_users_from_couple = ucdb.get_couple(user_id)
        
        # Затем получаем данные из state
        data_reject = await state.get_data()
        
        # Отправляем сообщение другому пользователю
        if msg.from_user.id == get_users_from_couple[2]:  # Игорь
            await bot.send_message(
                chat_id=get_users_from_couple[3],  # ID Полины (исправленный номер)
                text=f'''Ваш запрос отменили по следующим причинам:

    {data_reject.get("reject_message", "Причина не указана")}'''
            )
        elif msg.from_user.id == get_users_from_couple[3]:  # Полина (исправленный номер)
            await bot.send_message(
                chat_id=get_users_from_couple[2],  # ID Игоря
                text=f'''Ваш запрос отменили по следующим причинам:

    {data_reject.get("reject_message", "Причина не указана")}'''
            )
        
        await msg.answer("Ваш отказ отправлен")
        await state.clear()