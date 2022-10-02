from aiogram.dispatcher.filters.state import StatesGroup, State


class VocabularyState(StatesGroup):
    firstPage = State()
    secondPage = State()
