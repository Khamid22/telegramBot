from aiogram.types import Message, CallbackQuery
from keyboards.default.Vocabulary import VocabularySection
from states.Vocabulary import VocabularyState
from aiogram.dispatcher import FSMContext
from handlers.users.start import bot_start
import numpy as np
import pandas as pd
from loader import dp


@dp.message_handler(text="Vocabulary", state="*")
async def send_categories(message: Message, state: FSMContext):
    await message.answer("Hi! here you can improve your vocabulary by exercising!\n"
                         "Choose one of the categories", reply_markup=VocabularySection)
    await VocabularyState.secondPage.set()


@dp.callback_query_handler(text="Guessing Word", state="*")
async def start_the_game(call: CallbackQuery, state: FSMContext):
    game_state = True
    while state:
        voc = pd.read_csv('voc.csv')
        a = np.array(voc['word'])
        b = np.array(voc['meaning'])
        c = np.zeros(len(a))
        f = 0
        game_engine = True
        while game_engine:
            for i in a:
                if np.sum(c) == (len(a) * 2):
                    n = await call.message.answer("this is the end, you want to start all over again?")
                    if call.message.text == "yes":
                        await start_the_game()
                    if call.message.text == "no":
                        game_engine = False
                    else:
                        game_engine = False
                        game_state = False
                if c[f] == 0 or c[f] == 1:
                    await call.message.answer("Score " + i + "\n Meaning: " + b[i])
                    rate = int(await call.message.answer("rate: \n --i did not know-- 😐 \n --now i know, ask me "
                                                         "again-- 😅 \n -- i knew it, dont ask me again -- 😃"))
                    if rate == 0:
                        c[f] = 0
                    elif rate == 1:
                        c[f] = 1
                    elif rate == 2:
                        c[f] = 2
                    await call.message.answer(c)
                    f += 1
                else:
                    f += 1
                    continue
            await call.message.answer("result", c)
            f = 0
        else:
            state = False


@dp.message_handler(text="back", state="*")
async def get_back_main_menu(message: Message, state: FSMContext):
    await bot_start(message, state)