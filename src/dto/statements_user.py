from aiogram.fsm.state import StatesGroup, State

class States(StatesGroup):
    telegram_id = State()
    username = State()
    first_name = State()
    create_couple = State()