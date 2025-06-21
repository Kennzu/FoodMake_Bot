from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Выбрать блюдо", callback_data="change_food")],
    [InlineKeyboardButton(text="Добавить блюдо", callback_data="add_food")],
])

time_dinner_button = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Завтрак", callback_data="breakfast")],
    [InlineKeyboardButton(text="Обед", callback_data="lanch")],
    [InlineKeyboardButton(text="Ужин", callback_data="dinner")],
])

go_button = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Начать", callback_data="go")]
])

type_of_food_button = [
    [KeyboardButton(text="Завтрак")],
    [KeyboardButton(text="Обед")],
    [KeyboardButton(text="Ужин")],
]

skip_button = [
    [KeyboardButton(text="Пропустить")],
]

approve_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить", callback_data="approve")],
    [InlineKeyboardButton(text="Начать заново", callback_data="go")],
])

back_button = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Вернутся в меню", callback_data="menu")]
])

back_button_breakfats = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Назад", callback_data="breakfast")]
])

back_button_lanch = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Назад", callback_data="lanch")]
])

back_button_dinner = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Назад", callback_data="dinner")]
])

change_button_breakfast = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Выбрать", callback_data="change_dish")],
    [InlineKeyboardButton(text="Назад", callback_data="breakfast")],
])
change_button_lanch = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Выбрать", callback_data="change_dish")],
    [InlineKeyboardButton(text="Назад", callback_data="lanch")],
])
change_button_dinner = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Выбрать", callback_data="change_dish")],
    [InlineKeyboardButton(text="Назад", callback_data="dinner")],
])

approve_cookie_button = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Принять запрос", callback_data="approve_cookie")],
    [InlineKeyboardButton(text="Отклонить запрос", callback_data="reject_cookie")],
])

send_message_button = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Отправить", callback_data="send_msg")]
])

registration_button = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Регистрация", callback_data="reg")]
])

do_button_couple = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать взаимодействовать!", callback_data="menu")],
    [InlineKeyboardButton(text="Выйти из пары", callback_data="out_couple")],
])

create_couple_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Создать пару", callback_data="initiate_couple")]
])

approve_couple_button = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Принять запрос", callback_data="approve_couple")],
    [InlineKeyboardButton(text="Отклонить запрос", callback_data="reject_couple")],
])