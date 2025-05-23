from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


sing_up_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='Зарегистрироваться')]
])

in_db_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='Удалить акк')],
    [KeyboardButton(text='Изменить логин'), KeyboardButton(text='Изменить пароль')],
    [KeyboardButton(text='Мой профиль')]
])