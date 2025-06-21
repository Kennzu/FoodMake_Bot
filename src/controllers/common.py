from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode

import src.services.food_list_db as fld
import src.buttons.buttons as btn
import src.services.users_db as udb

def register_common_handlers(dp: Dispatcher):
    @dp.message(Command("view_id"))
    async def view_id_users(msg: Message):
        user_id = msg.from_user.id
        await msg.answer(f'''
Это твой ID 
<pre>{user_id}</pre>
Отправь его тому, кто попросил тебя узнать чтобы создать пару)''', parse_mode=ParseMode.HTML)
        
    @dp.message(Command("start"))
    async def start_message(msg: Message):
        fld.db_manager.connect_db()
        user_now = msg.from_user.id
        users = udb.check_user(user_now)

        if users == True:
            await msg.answer(
    '''
Ты уже зарегистрирован)
Проверь при помощи команды /view_couple есть ли у тебя пара. 
    ''')
        else:
        # fld.db_manager.create_table()
        # fld.db_manager.close()
            await msg.answer(
    '''Привет! Я бот, который поможет вам с выбором для будущей трапезы!
Давай для начала пройдем регистрацию)
    ''', reply_markup=btn.registration_button)
        fld.db_manager.close()

    @dp.message(Command("menu"))
    async def menu_message(msg: Message):
        await msg.answer(
    '''
Появилось какое-то новое блюдо?)
Или сегодня что-то из списка?)
    ''', reply_markup=btn.start_button)
    
    @dp.callback_query(F.data == "menu")
    async def menu_message(callback: CallbackQuery):
        await callback.message.edit_text(
    '''
Появилось какое-то новое блюдо?)
Или сегодня что-то из списка?)
    ''', reply_markup=btn.start_button)
        
    @dp.callback_query(F.data == "change_food")
    async def change_time(callback: CallbackQuery):
        await callback.message.answer(
    '''Отлично!
Давай для начала выберем когда мы хотим это блюдо
    ''', reply_markup=btn.time_dinner_button)
