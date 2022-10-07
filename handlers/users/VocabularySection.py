from aiogram.types import Message, CallbackQuery
from keyboards.default.Vocabulary import VocabularySection
from states.Vocabulary import VocabularyState
from aiogram.dispatcher import FSMContext
from keyboards.inline.GuessTheWord import options, reveal
from handlers.users.start import bot_start
import numpy as np
import pandas as pd
from loader import dp

voc = pd.read_csv('voc.csv')
words = np.array(voc['word'])
definitions = np.array(voc['meaning'])
learnt_words = np.zeros(len(words))


@dp.message_handler(text="Vocabulary", state=VocabularyState.firstPage)
async def send_categories(message: Message, state: FSMContext):
    await message.answer("Hi! here you can improve your vocabulary by exercising!\n"
                         "Choose one of the categories", reply_markup=VocabularySection)
    await VocabularyState.secondPage.set()


@dp.message_handler(text="Guessing Word", state=VocabularyState.secondPage)
async def start_the_game(message: Message, state: FSMContext):
    game_state = True
    f = 0
    game_engine = True
    while game_engine:
        for word in words:
            if np.sum(learnt_words) == (len(words) * 2):
                await message.answer("this is the end, you want to start all over again?", reply_markup=options)
                if message.text == "yes":
                    await start_the_game()
                if message.text == "no":
                    game_engine = False
            if learnt_words[f] == 0 or learnt_words[f] == 1:
                await message.bot.send_message(message.from_user.id, f'word : {word}', reply_markup=reveal)
                async with state.proxy() as data:
                    data['definitions[f]'] = definitions[f]
                    data['f'] = f
                await reveal_the_answer()
                await choose_one_option()


@dp.message_handler(text="back", state="*")
async def get_back_main_menu(message: Message, state: FSMContext):
    await bot_start(message, state)


@dp.callback_query_handler(text="lookup", state='*')
async def reveal_the_answer(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        word = data['definitions[f]']
    await call.message.answer(f'Definition: {word}\n'
                              "rate: \n --i did not know-- 😐 \n --now i know, ask me "
                              "again-- 😅 \n -- i knew it, dont ak me again -- 😃", reply_markup=options)
    await call.answer(cache_time=60)
    await VocabularyState.thirdPage.set()


@dp.callback_query_handler(state=VocabularyState.thirdPage)
async def choose_one_option(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    async with state.proxy() as data:
        f = data['f']
    answer = call.data
    if answer == "0":
        learnt_words[f] = 0
    elif answer == "1":
        learnt_words[f] = 1
    elif answer == "2":
        learnt_words[f] = 2
        f += 1
    else:
        f += 1
    await call.bot.send_message(call.from_user.id, f'Result {learnt_words}')

