from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import src.services.users_couples as ucdb
import src.services.users_db as udb
import src.buttons.buttons as btn
import src.dto.statements_user as sttsu

import logging
import uuid
from main import bot

def register_couple_handlers(dp: Dispatcher):
    @dp.message(Command("view_couple"))
    async def view_couple_users(msg: Message):
        user_id = msg.from_user.id
        couple = ucdb.check_couples(user_id)
        check_user = udb.check_user(user_id)
        if check_user == False:
            await msg.answer("Предлагаю сначала пройти регистрацию - /start")
        else:
            match couple:
                case True:
                    select_user = udb.select_user(user_id)
                    for i in select_user:
                        await msg.reply(f'''
<b>Ваша пара:</b>
<pre>Имя: {i[3]}\ntelegram_id {i[1]}</pre>

Хотите выйти из пары или начнете взаимодействие?)
        ''', reply_markup=btn.do_button_couple, parse_mode=ParseMode.HTML)
                case False:
                    await msg.reply("""
У вас нет пары 😭
Хотите стать инициатором пары?
    """, reply_markup=btn.create_couple_button)
                    
    @dp.callback_query(F.data == "initiate_couple")
    async def init_couple(callback: CallbackQuery, state: FSMContext):
        await state.set_state(sttsu.States.create_couple)
        await callback.message.answer("""
Окей, начнем создавать пару! 🫡

<b>Давай начнем с инструкции (ниже описание стэка действий):</b>

<pre>
1. Человек должен пройти регистрацию
2. После регистрации необходимо ввести следующую команду - /view_id
3. Далее, человек должен отправить данный id тебе)
4. Вносишь id сюда и следуете инструкциям далее)))
</pre>
                            
А теперь - введите telegram_id человека, с которым вы хотите создать пару
""", parse_mode=ParseMode.HTML)
        
    @dp.message(sttsu.States.create_couple)
    async def set_couple(msg: Message, state: FSMContext):
        try:
            partner2 = msg.text
            partner1 = msg.from_user.id
            
            # Проверяем, что partner2 - это число
            try:
                partner2 = int(partner2)
            except ValueError:
                await msg.reply("Некорректный ID пользователя. Введите числовой ID.")
                return
                
            check_user = udb.check_user(partner2)
            select_user = udb.select_user(partner1)
            
            if not select_user:
                await msg.reply("Ошибка: ваш профиль не найден в системе")
                return
                
            if partner1 == partner2:
                await msg.reply("Вы не можете создать пару с самим собой!")
            elif not check_user:
                await msg.reply("Вы не можете создать пару с незарегистрированным человеком!")
            else:
                await state.update_data(partner2=partner2)
                
                # Отправляем запрос второму пользователю
                try:
                    ucdb.pending_status_couple(partner1, partner2)
                    logging.info("Запрос был отправлен! Статус пары - pending")
                    await bot.send_message(
                        chat_id=partner2,
                        text=f'''С вами хотят создать пару! 

<pre>
Login - {select_user[0][2]}
Name - {select_user[0][3]}
Telegram_id = {select_user[0][1]}
</pre>

(Если вы не знаете кто вам предлагает создать пару, отклоните запрос)''',
                        reply_markup=btn.approve_cookie_button,
                        parse_mode=ParseMode.HTML
                    )

                except Exception as e:
                    logging.error(f"Ошибка при отправке запроса на создание пары: {e}")
                    await msg.answer(
                        "Не удалось отправить запрос на создание пары. "
                        "Попробуйте позже.",
                        reply_markup=btn.create_couple_button
                    )
            
        except Exception as e:
            logging.error(f"Ошибка в обработчике set_couple: {e}")
            await msg.answer(
                "Упс! Что-то пошло не так при создании пары(\n"
                "Попробуйте создать пару заново",
                reply_markup=btn.create_couple_button
            )
        finally:
            await state.clear()

    @dp.callback_query(F.data == "approve_couple")
    async def couple_accepted(callback: CallbackQuery):
        receiver_id = callback.from_user.id
        gen_uuid = str(uuid.uuid4())
        logging.info(f"Был сгенерирован uuid {gen_uuid} для пары")
        sender_id = ucdb.accepted_status_couple(receiver_id, gen_uuid)
        


        if sender_id:
            # Уведомляем обоих
            await callback.message.answer("Пара успешно создана! 💖 Можете начать добавлять блюда друг другу!", reply_markup=btn.start_button)
            await bot.send_message(
                chat_id=sender_id,
                text="Ура! Вас приняли в пару ❤️ Можете начинать взаимодействовать!",
                reply_markup=btn.start_button
            )
        else:
            await callback.message.answer("Упс... Похоже, нет активного запроса на создание пары.")