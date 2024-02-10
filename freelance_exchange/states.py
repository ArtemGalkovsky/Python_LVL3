from aiogram.fsm.state import State, StatesGroup


class NewTaskStates(StatesGroup):
    TITLE = State()
    LANGS = State()
    DESCRIPTION = State()
    CONTACTS = State()
