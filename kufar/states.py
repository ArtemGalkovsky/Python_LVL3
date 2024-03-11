from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    NICKNAME = State()
    CONTACTS = State()
    END = State()


class PostCreationStates(StatesGroup):
    TITLE = State()
    DESCRIPTION = State()
    MEDIA = State()
    SEND = State()


class PostEditingStates(StatesGroup):
    EDITING = State()

