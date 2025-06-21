import logging

from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import src.dto.statements_user as sttsu
import src.services.users_db as udb
import src.buttons.buttons as btn


def register_registration_handlers(dp: Dispatcher):
    @dp.callback_query(F.data == "reg")
    async def begin_registration_user(callback: CallbackQuery, state: FSMContext):
        await callback.message.answer(
    '''
Отлично!
Начнем с твоего логина.
Введи свой логин:
    ''')
        await state.set_state(sttsu.States.username)

    @dp.message(sttsu.States.username)
    async def add_first_name(msg: Message, state: FSMContext):
        login = msg.text  # пользователь ввел логин

        # Сохраняем логин в FSMContext
        await state.update_data(username=login)

        check = udb.check_login(login)

        match check:
            case True:
                await msg.answer("Такой логин уже существует. Попробуйте заново", reply_markup=btn.registration_button)
            case False:
                await state.set_state(sttsu.States.first_name)
                await msg.answer(
    '''
Теперь, введи свое имя. 
Оно понадобится для отображения в сообщениях между парами)
    '''
    )

        
    @dp.message(sttsu.States.first_name)
    async def end_reg_user(msg: Message, state: FSMContext):
        telegram_id = msg.from_user.id
        first_name = msg.text

        # Сохраняем имя в FSMContext
        await state.update_data(first_name=first_name)

        data_r = await state.get_data()

        add_user_data = {
            "login": data_r.get("username"),
            "name": data_r.get("first_name"),
        }
        logging.info(f"Данные для регистрации {add_user_data['login']}, {add_user_data['name']}")
        
        try:
            add_user = udb.create_user(telegram_id, add_user_data['login'], add_user_data['name'])
            logging.info(f"Добавление {add_user} успешно!")
            await msg.answer("""
Вы успешно прошли регистрацию!
Предлагаю следующий стэк действий:
Для начала проверьте, находитесь ли вы в паре - нажми на 
/view_couple
Если у вас все хорошо, то можете перейти к основному - 
/menu 
или нажмите на кнопку ниже сообщения) """, reply_markup=btn.start_button)
            await state.clear()
            
        except Exception as e:
            logging.error("Ошибка добаления данных юзера: %s", str(e))