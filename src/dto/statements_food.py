from aiogram.fsm.state import StatesGroup, State

class States(StatesGroup):
    type_food = State()
    name_food = State()
    description_food = State()
    calories_food = State()
    photo_food = State()