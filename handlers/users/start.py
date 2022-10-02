from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
import states.Vocabulary
from keyboards.default.bot_menu import botMenu
from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Welcome, {message.from_user.full_name}!", reply_markup=botMenu)
    await states.Vocabulary.VocabularyState.firstPage.set()
