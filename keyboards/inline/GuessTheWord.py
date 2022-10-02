from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

reveal = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Look up', callback_data='lookup')]])

options = InlineKeyboardMarkup(row_width=1)
options.insert(InlineKeyboardButton(text="😃", callback_data="2"))
options.insert(InlineKeyboardButton(text="😅", callback_data="1"))
options.insert(InlineKeyboardButton(text="😐", callback_data="0"))