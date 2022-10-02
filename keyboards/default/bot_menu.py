from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

botMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Vocabulary")],
        [KeyboardButton(text="About us")]
    ], resize_keyboard=True
)
back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="back")]], resize_keyboard=True)
