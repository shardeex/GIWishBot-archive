from aiogram.dispatcher.filters.state import State, StatesGroup


class ShowcaseEdit(StatesGroup):
    character = State()
    weapon = State()
