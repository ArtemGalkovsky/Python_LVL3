from asyncio import run
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from requests import get
from langs_buttons import LANGS_KEYBOARD
from openpyxl import load_workbook


def is_age(string: str) -> bool:
    split_string = string.split(".")
    if string.replace(".", "").isnumeric() and len(split_string) == 3 and \
            len(split_string[0]) == 2 and len(split_string[1]) == 2 and len(split_string[2]) == 4:
        return True

    return False


def add_to_excel(data: dict[str: str]) -> None:
    wb = load_workbook("form.xlsx")
    sheet = wb.active

    sheet.append(tuple(data.values()))

    wb.save("form.xlsx")


class InterviewStages(StatesGroup):
    NAME_SURNAME = State()
    BIRTHDAY = State()
    PROGRAMMING_LANGS = State()
    WORK_BACKGROUND_IN_AGES = State()
    LANG_TECHNOLOGIES = State()
    PHONE_NUMBER = State()


dp = Dispatcher()
TOKEN = get("https://artemgalkovsky.pythonanywhere.com/GA1234567").text


@dp.message(StateFilter(None), Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("Введите ФИО:")
    await state.set_state(InterviewStages.NAME_SURNAME)


@dp.message(InterviewStages.NAME_SURNAME)
async def enter_name(message: Message, state: FSMContext):
    if len(message.text.split()) < 2:
        await message.reply("Введите полное ФИО")
    else:
        await state.set_state(InterviewStages.BIRTHDAY)
        await state.update_data(name=message.text)
        await message.answer("Введите возраст (дд.мм.гггг):")


@dp.message(InterviewStages.BIRTHDAY)
async def enter_birthday(message: Message, state: FSMContext):
    if not is_age(message.text):
        await message.reply("Введите возраст (дд.мм.гггг)")
    else:
        await state.set_state(InterviewStages.PROGRAMMING_LANGS)
        await state.update_data(birthday=message.text)
        await message.answer("Введите любимые языки программирования:",
                             reply_markup=ReplyKeyboardMarkup(
                                 keyboard=LANGS_KEYBOARD,
                                 resize_keyboard=True,
                                 one_time_keyboard=True)
                             )


@dp.message(InterviewStages.PROGRAMMING_LANGS)
async def enter_langs(message: Message, state: FSMContext):
    await state.set_state(InterviewStages.LANG_TECHNOLOGIES)
    await state.update_data(program_langs=message.text)
    await message.answer("Введите технологии с которыми вы работали:")


@dp.message(InterviewStages.LANG_TECHNOLOGIES)
async def enter_technologies(message: Message, state: FSMContext):
    await state.set_state(InterviewStages.PHONE_NUMBER)
    await state.update_data(technologies=message.text)
    await message.answer("Введите номер телефона:")


@dp.message(InterviewStages.PHONE_NUMBER)
async def enter_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    add_to_excel(await state.get_data())
    await state.clear()
    await message.answer("THX")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
