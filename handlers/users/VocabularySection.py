from aiogram.types import Message, CallbackQuery
from keyboards.default.Vocabulary import VocabularySection
from states.Vocabulary import VocabularyState
from aiogram.dispatcher import FSMContext
from keyboards.inline.GuessTheWord import options
from handlers.users.start import bot_start
import numpy as np
import pandas as pd
from loader import dp


@dp.message_handler(text="Vocabulary", state=VocabularyState.firstPage)
async def send_categories(message: Message, state: FSMContext):
    await message.answer("Hi! here you can improve your vocabulary by exercising!\n"
                         "Choose one of the categories", reply_markup=VocabularySection)
    await VocabularyState.secondPage.set()


@dp.message_handler(text="Guessing Word", state=VocabularyState.secondPage)
async def start_the_game(message: Message, state: FSMContext):
    game_state = True
    while game_state:
        voc = pd.read_csv('voc.csv')
        words = np.array(voc['word'])
        definitions = np.array(voc['meaning'])
        learnt_words = np.zeros(len(words))
        f = 0
        game_engine = True
        while game_engine:
            for word in words:
                if learnt_words[f] == 0 or learnt_words[f] == 1:
                    await message.answer("Score \n Meaning: ", definitions[f])
                    await message.answer("rate: \n --i did not know-- 😐 \n --now i know, ask me "
                                         "again-- 😅 \n -- i knew it, dont ask me again -- 😃")
                    answer = message.text
                    if answer == "0":
                        learnt_words[f] = 0
                    elif answer == "1":
                        learnt_words[f] = 1
                    elif answer == "2":
                        learnt_words[f] = 2
                    await message.answer(learnt_words)
                    f += 1
                else:
                    f += 1
                    continue
            await message.answer("result", learnt_words)
            f = 0
            if np.sum(learnt_words) == (len(words) * 2):
                await message.answer("this is the end, you want to start all over again?", reply_markup=options)
                if message.text == "yes":
                    await start_the_game()
                if message.text == "no":
                    game_engine = False
        else:
            game_state = False


@dp.message_handler(text="back", state="*")
async def get_back_main_menu(message: Message, state: FSMContext):
    await bot_start(message, state)
