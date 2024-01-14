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
from calculator_buttons import CALCULATOR_BUTTONS

dp = Dispatcher()
TOKEN = get("https://artemgalkovsky.pythonanywhere.com/GA1234567").text

user_input = {}


@dp.message(Command("start"))
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=CALCULATOR_BUTTONS, resize_keyboard=True)
    await message.answer("Введите чо угодно, я разрешаю:", reply_markup=keyboard)


@dp.message(F.text == "=")
async def calculate(message: Message):
    expression = user_input.get(message.chat.id, "").replace("=", "")
    user_input[message.chat.id] = ""

    try:
        await message.answer(str(eval(expression)))
    except ZeroDivisionError:
        await message.answer("Делишь на 0, афигев?")
    except Exception as e:
        await message.answer("Что-то пошло не так :(")


@dp.message(F.text == "Clear")
async def clear(message: Message):
    user_input[message.chat.id] = ""
    await message.answer("Всё, тютю")


@dp.message(F.text == "<-")
async def clear(message: Message):
    previous_user_input = user_input[message.chat.id]

    user_input[message.chat.id] = previous_user_input[:-1]

    if previous_user_input:
        await message.answer(f"Удалено предыдущее число/знак - '{previous_user_input[-1]}'")


@dp.message()
async def add(message: Message):
    if message.text in "().+-*/1234567890":
        chat_id = message.chat.id

        if chat_id in user_input:
            user_input[chat_id] += message.text
        else:
            user_input[chat_id] = message.text
    else:
        await message.reply("Чо это :/")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
