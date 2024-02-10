from asyncio import run
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from requests import get
from db import tg_db
from states import NewTaskStates

dp = Dispatcher()

TOKEN = get("https://artemgalkovsky.pythonanywhere.com/GA7439").text
SORTED_STATES = (NewTaskStates.TITLE, NewTaskStates.LANGS, NewTaskStates.DESCRIPTION, NewTaskStates.CONTACTS)

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(Command("start"), StateFilter(None))
async def start(message: Message, state: FSMContext):
    await message.answer("""
        Здравствуйте! Чтобы получать уведомления о новых задачах, нужно задать языки, которые вы используете:
        <b>/selectonly ЯП1, ЯП2, ... ЯП</b>
        
<b>Шаги для создания новой задачи</b>:
        1) Указать заголовок: <b>Напишите /title и ответьте на сообщение с заголовком</b>
        2) Указать требуемые языки программирования: <b>Напишите /langs и ответьте на сообщение с ЯП</b>
        Сообщение должно быть в таком формате!<b>ЯП1, ЯП2, ... ЯП</b>
        3) Указать описание: <b>Напишите /desc и ответьте на сообщение с описанием</b>
        4) Указать контакты: <b>Напишите /cont и ответьте на сообщение с контактами</b>
        5) Создать задачу с помощью команды <b>/done</b>

<b>Чтобы перестать получать уведомления напишите: /delme
Для возобновления работы бота напишите /start</b>
    """, reply_markup=None, parse_mode=ParseMode.HTML)


@dp.message(Command("selectonly"), StateFilter(None))
async def select_only(message: Message, state: FSMContext):
    langs = message.text.replace("/selectonly", "").lower()
    user_id = message.from_user.id

    tg_db.add_user(user_id, langs)

    await message.reply(f"Успешно установлены языки: {langs} для пользователя {user_id}", reply_markup=None)


@dp.message(Command("title"), StateFilter(None))
async def set_task_title(message: Message, state: FSMContext):
    try:
        title = message.reply_to_message.text
        await state.update_data({"title": title})
        await message.reply(f"Заголовок '{title}' успешно задан!")
    except AttributeError:
        await message.reply("Не найдено сообщение с заголовком!")


@dp.message(Command("langs"), StateFilter(None))
async def set_task_langs(message: Message, state: FSMContext):
    try:
        langs = message.reply_to_message.text
        await state.update_data({"langs": langs})
        await message.reply(f"Требуемые языки для выполнения задания '{langs}' успешно заданы!")
    except AttributeError:
        await message.reply("Не найдено сообщение с языками!")


@dp.message(Command("desc"), StateFilter(None))
async def set_task_description(message: Message, state: FSMContext):
    try:
        description = message.reply_to_message.text
        await state.update_data({"description": description})
        await message.reply(f"Описание '{description}' успешно задано!")
    except AttributeError:
        await message.reply("Не найдено сообщение с описанием задания!")


@dp.message(Command("cont"), StateFilter(None))
async def set_task_contacts(message: Message, state: FSMContext):
    try:
        contacts = message.reply_to_message.text
        await state.update_data({"contacts": contacts})
        await message.reply(f"Контакты '{contacts}' успешно заданы!")
    except AttributeError:
        await message.reply("Не найдено сообщение с контактами!")


def validate_task_parts(state_dict):
    return all((state_dict.get("title"), state_dict.get("langs"),
                state_dict.get("description"), state_dict.get("contacts")))


@dp.message(Command("d", "done"), StateFilter(None))
async def create_task(message: Message, state: FSMContext):
    state_data = dict(await state.get_data())

    if state_data:
        await message.reply(str(state_data))
        await state.clear()

        langs = state_data.get("langs")

        task = f"""
<b>{state_data["title"]}</b>
<b>Требуемые знания языков программирования:</b>
{state_data["langs"]}

<b>ТЗ:</b>
{state_data["description"]}

<b>КОНТАКТЫ:</b>
{state_data["contacts"]}
        """

        await send_all(*langs.split(","), task=task)
    else:
        await message.reply("Вы не задали нужные параметры для создания задания!")


async def send_all(*languages, task):
    ids = set()

    for lang in languages:
        lang_ids = tg_db.select_by_lang(lang.lower().strip())

        ids = ids.union(set(lang_ids))

    for id_ in ids:
        await bot.send_message(id_, task)


@dp.message(Command("delme"), StateFilter(None))
async def stop(message: Message, state: FSMContext):
    tg_db.remove_user(message.from_user.id)
    await message.answer("Вы удалены из базы данных!", reply_markup=None)


async def run_bot() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(run_bot())
