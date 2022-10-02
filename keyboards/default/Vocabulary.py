from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

VocabularySection = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Guessing Word")],
        [KeyboardButton(text="back")]
    ], resize_keyboard=True)
