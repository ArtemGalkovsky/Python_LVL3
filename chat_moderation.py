from asyncio import run, sleep
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command, StateFilter, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import Message, InlineKeyboardButton, \
    InlineKeyboardMarkup, FSInputFile, CallbackQuery, ChatMemberUpdated
from aiogram.enums import ParseMode
from requests import get
from os import getcwd, mkdir, remove, listdir, path
from commands import set_commands
from databases import databases
from states import CaptchaState
from string import ascii_letters, digits
from random import choice

dp = Dispatcher()

TOKEN = get("").text
OWNERS = []

assert OWNERS, "PLEASE ADD OWNER"

CHAT_NEEDS_MODERATION = -1002028496800
IS_BLACK_LIST_ON = False
IS_ANTI_SPAM_ON = False
ANTISPAM_TIME = 0

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER), StateFilter(None))
async def on_join(event: ChatMemberUpdated, state: FSMContext):
    await state.set_state(CaptchaState.CAPTCHA)

    captcha = "".join((choice(ascii_letters + digits) for _ in range(5)))
    await state.set_data({"captcha": captcha, "times": 3})

    await sleep(60)
    if await state.get_state() == CaptchaState.CAPTCHA:
        await bot.ban_chat_member(event.chat.id, event.from_user.id)
        await bot.unban_chat_member(event.chat.id, event.from_user.id)


@dp.message(StateFilter(CaptchaState.CAPTCHA))
async def enter_captcha(message: Message, state: FSMContext):
    captcha_dict = await state.get_data()

    if message.text and message.text.strip() == captcha_dict["captcha"]:
        await state.set_state(None)
        await message.answer("Поздравляю, вы можете общаться!")
        return
    elif captcha_dict["times"] < 1:
        await bot.ban_chat_member(message.chat.id, message.from_user.id)
        await bot.unban_chat_member(message.chat.id, message.from_user.id)
        return

    await message.answer(
        f"Введите капчу {captcha_dict['captcha']}, у вас осталось {captcha_dict['times']} попытки(а): ")
    await state.update_data({"times": captcha_dict["times"] - 1})


@dp.message(Command("add_admin"), F.from_user.id.in_(OWNERS))
async def add_admin(message: Message):
    telegram_user_id = message.text.replace("/add_admin", "").strip()
    if telegram_user_id.isnumeric():
        databases.admins.add_admin(telegram_user_id)
        await message.answer("Админ добавлен!")
        return

    await message.answer("Введите айди пользователя тегерама: [Пример: 9348393749]")


@dp.message(Command("remove_admin"), F.from_user.id.in_(OWNERS))
async def remove_admin(message: Message):
    telegram_user_id = message.text.replace("/remove_admin", "").strip()
    if telegram_user_id.isnumeric():
        if databases.admins.is_user_admin(telegram_user_id):
            databases.admins.remove_admin(telegram_user_id)
            await message.answer("Админ испепелён!")
            return

        await message.answer("Такого админа нет!")
        return

    await message.answer("Введите айди пользователя тегерама: [Пример: 9348393749]")


@dp.message(Command("blacklist_on"))
async def turn_on_blacklist(message: Message):
    from_user_id = message.from_user.id

    if databases.admins.is_user_admin(from_user_id) or from_user_id in OWNERS:
        with open("is_blacklist_on", "w+") as fl:
            fl.write("ikdhnflkhdfnndf")

        global IS_BLACK_LIST_ON
        IS_BLACK_LIST_ON = True
        await message.answer("Блэклист включён!")
        return

    await message.answer("Вы бесправный :)")


@dp.message(Command("blacklist_off"))
async def turn_on_blacklist(message: Message):
    from_user_id = message.from_user.id

    if databases.admins.is_user_admin(from_user_id) or from_user_id in OWNERS:
        with open("is_blacklist_on", "w+") as fl:
            fl.write("")

        global IS_BLACK_LIST_ON
        IS_BLACK_LIST_ON = False
        await message.answer("Блэклист выключен!")
        return

    await message.answer("Вы бесправный :)")


@dp.message(Command("blacklist_add"))
async def add_word_to_blacklist(message: Message):
    from_user_id = message.from_user.id
    word = message.text.replace("/blacklist_add", "").strip()

    if databases.admins.is_user_admin(from_user_id) or from_user_id in OWNERS:
        databases.blacklist.add_word(word.lower())
        await message.answer("Слово добавлено в чёрный список!")
        return

    await message.answer("Вы бесправный :)")


@dp.message(Command("blacklist_remove"))
async def add_word_to_blacklist(message: Message):
    from_user_id = message.from_user.id
    word = message.text.replace("/blacklist_remove", "").strip()

    if databases.admins.is_user_admin(from_user_id) or from_user_id in OWNERS:
        databases.blacklist.remove_word(word.lower())
        await message.answer("Слово удалено из чёрного списка!")
        return

    await message.answer("Вы бесправный :)")


@dp.message(Command("blacklist_clear"))
async def add_word_to_blacklist(message: Message):
    from_user_id = message.from_user.id

    if databases.admins.is_user_admin(from_user_id) or from_user_id in OWNERS:
        databases.blacklist.clear()
        await message.answer("За шо?")
        return

    await message.answer("Вы бесправный :)")


@dp.message(Command("antispam_on"))
async def turn_on_antispam(message: Message):
    from_user_id = message.from_user.id

    if databases.admins.is_user_admin(from_user_id) or from_user_id in OWNERS:
        with open("is_anti_spam_on", "w+") as fl:
            fl.write("ikdhnflkhdfnndf")

        global IS_ANTI_SPAM_ON
        IS_ANTI_SPAM_ON = True
        await message.answer("Антиспам включён!")
        return

    await message.answer("Вы бесправный :)")


@dp.message(Command("antispam_off"))
async def turn_off_antispam(message: Message):
    from_user_id = message.from_user.id

    if databases.admins.is_user_admin(from_user_id) or from_user_id in OWNERS:
        with open("is_anti_spam_on", "w+") as fl:
            fl.write("")

        global IS_ANTI_SPAM_ON
        IS_ANTI_SPAM_ON = False
        await message.answer("Антиспам выключен!")
        return

    await message.answer("Вы бесправный :)")


@dp.message(Command("antispam_time"))
async def turn_off_antispam(message: Message):
    from_user_id = message.from_user.id

    antispam_time = message.text.replace("/antispam_time", "").strip()
    if (databases.admins.is_user_admin(from_user_id) or from_user_id in OWNERS) and antispam_time.isnumeric():
        with open("antispam_time", "w+") as fl:
            fl.write(antispam_time)

        global ANTISPAM_TIME
        ANTISPAM_TIME = int(antispam_time)
        await message.answer("Время установлено!")
        return

    await message.answer("Вы бесправный :)")


@dp.message(Command("message"))
async def send_anonymous_message(message: Message):
    from_user_id = message.from_user.id

    if databases.admins.is_user_admin(from_user_id) or from_user_id in OWNERS:
        message_text = message.text.replace("/message", "").strip()

        if message_text:
            await bot.send_message(CHAT_NEEDS_MODERATION, message_text)
            await message.answer("Сообщение отправлено")
            return

        await message.answer("Сообщение не должно быть пустым!")
        return

    await message.answer("Вы бесправный :)")


@dp.message(StateFilter(None))
async def on_message(message: Message, state: FSMContext):
    if IS_ANTI_SPAM_ON:
        text = message.text

        last_message_with_equal_text = databases.messages.get_last_equal_message_data(text)

        if last_message_with_equal_text and last_message_with_equal_text[0] == message.from_user.id and \
                last_message_with_equal_text[2] + ANTISPAM_TIME >= message.date.timestamp():
            await message.answer("БУБУБУ НЕ ФЛУДИ")
            await message.delete()

    if message.chat.id == CHAT_NEEDS_MODERATION:
        databases.messages.add_message(message)

    if message.text:
        if IS_BLACK_LIST_ON:
            words = message.text.split()
            are_words_in_blacklist = (databases.blacklist.is_word_in_blacklist(word.lower()) for word in words)

            if any(are_words_in_blacklist):
                await message.answer("АТЯТЯ ТАК НЕЗЯ")
                await message.delete()


async def run_bot() -> None:
    global IS_BLACK_LIST_ON, IS_ANTI_SPAM_ON, ANTISPAM_TIME
    with open("is_blacklist_on") as fl:
        if fl.read():
            IS_BLACK_LIST_ON = True

    with open("is_anti_spam_on") as fl:
        if fl.read():
            IS_ANTI_SPAM_ON = True

    with open("antispam_time") as fl:
        ANTISPAM_TIME = int(fl.read())

    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(run_bot())
