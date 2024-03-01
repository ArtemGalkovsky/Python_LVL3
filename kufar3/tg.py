from asyncio import run
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, InlineKeyboardButton, \
    InlineKeyboardMarkup, FSInputFile, CallbackQuery
from aiogram.enums import ParseMode
from commands import set_commands
from requests import get
from os import getcwd, mkdir, remove, listdir, path
from aiogram.utils.media_group import MediaGroupBuilder
from states import RegistrationStates, PostCreationStates, PostEditingStates
from keyboards import (CONTACT_TYPES, create_print_n_posts_keyboard,
                       create_post_edit_keyboard, create_editing_post_keyboard)
from db import database
from time import time
from re import compile, fullmatch

dp = Dispatcher()

TOKEN = get("https://artemgalkovsky.pythonanywhere.com/GA9831").text
KUFAR_CHANNEL_ID = -1002116198639
IMAGES_FOLDER = f"{getcwd()}/images/"
TITLE_MAX_SIZE = 40
LIMIT_POSTS_COMMAND = 10

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


# def is_mail_valid(email: str) -> bool:
#     regex = compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
#     if fullmatch(regex, email):
#         return True
#     else:
#         return False


@dp.message(Command("start"), StateFilter(None))
async def start(message: Message, state: FSMContext):
    await state.set_state(RegistrationStates.END)
    if database.users_db.get_user_data_by_telegram_id(message.from_user.id):
        await message.answer("Вы уже зарегистрированы, для помощи напишите: <b>/help</b>")
        await state.set_state(RegistrationStates.END)
        return

    await message.answer("Здравствуйте, я бот-барахольщик! Для начала, давайте познакомимся!\n<b>Как вас зовут?</b>")
    await state.set_state(RegistrationStates.NICKNAME)


@dp.callback_query(F.data == "restore_nickname", StateFilter(RegistrationStates.CONTACTS))
async def change_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationStates.NICKNAME)
    await callback.message.answer("<b>Введите своё имя:</b>")


@dp.message(StateFilter(RegistrationStates.NICKNAME))
async def enter_name(message: Message, state: FSMContext):
    name = message.text.strip()

    if name:
        await state.set_state(RegistrationStates.CONTACTS)
        await state.set_data({"name": name})
        await message.reply(f"Очень приятно, {name}!\nКак с вами можно связаться?",
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=CONTACT_TYPES))
    else:
        await message.reply("<b>Не понимаю!!!</b> Пожалуйста, введите своё имя!")


@dp.callback_query(F.data == "restore_contacts", StateFilter(RegistrationStates.END))
async def change_contacts(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationStates.CONTACTS)

    name = (await state.get_data())["name"]
    await state.set_data({"name": name})
    await callback.message.answer("<b>Введите свои контакты:</b>",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=CONTACT_TYPES))

    database.users_db.remove_user(callback.message.chat.id)


@dp.callback_query(F.data == "contacts_email", StateFilter(RegistrationStates.CONTACTS))
async def enter_email(callback: CallbackQuery, state: FSMContext):
    await state.update_data({"contact_type": "email"})
    await callback.message.reply("<b>Введите свою электронную почту:</b>")


@dp.callback_query(F.data == "contacts_phone", StateFilter(RegistrationStates.CONTACTS))
async def enter_phone(callback: CallbackQuery, state: FSMContext):
    await state.update_data({"contact_type": "phone"})
    await callback.message.reply("<b>Введите свой номер телефона:</b>")


@dp.callback_query(F.data == "contacts_telegram", StateFilter(RegistrationStates.CONTACTS))
async def enter_telegram(callback: CallbackQuery, state: FSMContext):
    await state.update_data({"contact_type": "telegram"})
    await callback.message.reply("<b>Введите @ник телеграма, по которому стоит обращаться по товару:</b>")


@dp.message(StateFilter(RegistrationStates.CONTACTS))
async def enter_contacts(message: Message, state: FSMContext):
    data = await state.get_data()
    contact = message.text.strip()

    if data["contact_type"] == "email":
        ...
        # if not is_mail_valid(contact):
        #     await message.reply("Некорректный почтовый адрес! <b>Введите ещё раз:</b>",
        #                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        #                             [InlineKeyboardButton(text="Отмена", callback_data="restore_contacts")]
        #                         ]))
        #     return
    elif data["contact_type"] == "phone":
        ...

    await state.set_state(RegistrationStates.END)
    await message.answer(f"Вы успешно зарегистрировались как {data['name']} и {contact}!\n <b>/help</b>",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text="Отмена", callback_data="restore_contacts")]
                         ]))

    database.users_db.add_user(message.from_user.id, data["name"], contact)


@dp.message(Command("unreg"), StateFilter(RegistrationStates.END))
async def unregister(message: Message, state: FSMContext):
    await state.set_state(RegistrationStates.NICKNAME)
    await message.answer("<b>Введите своё имя:</b>")

    database.users_db.remove_user(message.from_user.id)


@dp.message(Command("post"), StateFilter(RegistrationStates.END))
async def post_help(message: Message, state: FSMContext):
    await message.answer("Для начала создания поста напишите <b>/create</b>")


@dp.callback_query(F.data == "cancel_post_creation", StateFilter(PostCreationStates.TITLE))
async def cancel_post_creation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationStates.END)
    await state.update_data({"post_title": None, "post_text": None, "post_media_path": None})

    await callback.message.answer("<b>Создание поста отменено!</b>")


@dp.message(Command("create"), StateFilter(RegistrationStates.END))
async def enter_post_name(message: Message, state: FSMContext):
    await message.answer(f"<b>Введите название товара (Не более {TITLE_MAX_SIZE} символов):</b>",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text="Отмена создания поста", callback_data="cancel_post_creation")]
                         ]))
    await state.set_state(PostCreationStates.TITLE)


@dp.callback_query(F.data == "back_to_title", StateFilter(PostCreationStates.DESCRIPTION))
async def back_to_title(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PostCreationStates.TITLE)
    await callback.message.answer(f"<b>Введите название товара (Не более {TITLE_MAX_SIZE} символов):</b>",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                      [InlineKeyboardButton(text="Отмена создания поста",
                                                            callback_data="cancel_post_creation")]
                                  ]))


@dp.message(StateFilter(PostCreationStates.TITLE))
async def enter_title(message: Message, state: FSMContext):
    title = message.text.strip()

    if len(title) > TITLE_MAX_SIZE:
        await message.reply(f"<b>Превышена длина названия! Введите название товара "
                            f"(Не более {TITLE_MAX_SIZE} символов):</b>",
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text="Отмена создания поста",
                                                      callback_data="cancel_post_creation")]
                            ]))
        return

    await state.set_data({"title": title})
    await state.set_state(PostCreationStates.DESCRIPTION)

    await message.answer("<b>Введите описание товара (Не более 3500 символов):</b>",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text="Назад к созданию названия",
                                                   callback_data="back_to_title")]
                         ]))


@dp.callback_query(F.data == "back_to_description", StateFilter(PostCreationStates.MEDIA))
async def back_to_description(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PostCreationStates.DESCRIPTION)
    await callback.message.answer("<b>Введите описание товара (Не более 3500 символов):</b>",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                      [InlineKeyboardButton(text="Назад к созданию названия",
                                                            callback_data="back_to_title")]
                                  ]))


@dp.message(StateFilter(PostCreationStates.DESCRIPTION))
async def enter_description(message: Message, state: FSMContext):
    description = message.text.strip()

    if len(description) > 3500:
        await message.reply("<b>Превышена максимальная длина! Введите описание товара (Не более 3500 символов):</b>",
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text="Назад к созданию названия",
                                                      callback_data="back_to_title")]
                            ]))
        return

    await state.update_data({"description": description})
    await state.set_state(PostCreationStates.MEDIA)

    await message.answer("<b>Создайте сообщение содержащее фото товара с текстом /media:</b>",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text="Назад к созданию описания",
                                                   callback_data="back_to_description")]
                         ]))


async def download_high_resolution_photos(message: Message, destination_folder: str):
    for photo in message.photo:
        await message.bot.download(file=photo.file_id,
                                   destination=f"{destination_folder}/{photo.file_id}.png")

    for index, photo_name in enumerate(listdir(destination_folder), 1):  # removes low quality photos
        if index % 2 == 0 or index % 3 == 0:
            remove(f"{destination_folder}/{photo_name}")


def prepare_post_text(user_telegram_id: int, data: dict):
    user_data = database.users_db.get_user_data_by_telegram_id(user_telegram_id)

    return f"""<b>{data["title"]}</b>

{data["description"]}

<b>КОНТАКТ:</b>
{user_data[2]}, {user_data[1]}
"""


async def create_post(user_telegram_id: int, data: dict, build: bool = True):
    album_builder = MediaGroupBuilder(
        caption=prepare_post_text(user_telegram_id, data)
    )

    images_path = f"{IMAGES_FOLDER}/{data['post_unique_id']}"
    for image_name in listdir(images_path):
        album_builder.add_photo(media=FSInputFile(f"{images_path}/{image_name}"))

    if build:
        return album_builder.build()

    return album_builder


@dp.message(Command("media"), StateFilter(PostCreationStates.MEDIA))
async def enter_media(message: Message, state: FSMContext):
    if not message.photo:
        await message.reply("Сообщение должно содержать хотя бы 1 фото!",
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text="Назад к созданию описания",
                                                      callback_data="back_to_description")]
                            ]))
        return

    post_unique_id = f"{message.chat.id}_{message.message_id}_{round(time() * 1000)}"

    destination_folder = f"{IMAGES_FOLDER}/{post_unique_id}"
    mkdir(destination_folder)

    await download_high_resolution_photos(message, destination_folder=destination_folder)

    await state.update_data({"post_unique_id": post_unique_id})
    await state.set_state(PostCreationStates.SEND)

    await message.answer("<b>Ваш пост будет выглядеть так VVV. Отправлять?</b> (Если пост снизу не появился, нажмите"
                         " на кнопку ниже и пришлите фото с текстом /media ещё раз!")
    await message.answer_media_group(await create_post(message.from_user.id, await state.get_data()))

    await message.answer("<b>Для отправки поста напишите: /done</b>",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text="Назад к загрузке фото", callback_data="cancel_send_operation")]
                         ]))


@dp.callback_query(F.data == "cancel_send_operation", StateFilter(PostCreationStates.SEND))
async def back_to_media(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PostCreationStates.MEDIA)
    await callback.message.answer("<b>Создайте сообщение содержащее фото товара с текстом /media:</b>",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                      [InlineKeyboardButton(text="Назад к созданию описания",
                                                            callback_data="back_to_description")]
                                  ]))


@dp.message(Command("done"), StateFilter(PostCreationStates.SEND))
async def post_creation_done(message: Message, state: FSMContext):
    post_data = await state.get_data()

    messages = await bot.send_media_group(KUFAR_CHANNEL_ID, await create_post(message.from_user.id, post_data))

    database.posts_db.add_post(post_data["post_unique_id"], message.from_user.id,
                               post_data["title"], post_data["description"],
                               messages[-1].chat.id, messages[-1].message_id)
    await state.set_state(RegistrationStates.END)
    await state.set_data({})
    await message.answer("<b>Пост успешно отправлен! (Для удаления напишите /posts и выберете нужный пост!</b>")


@dp.callback_query(F.data.startswith("next_"), StateFilter(RegistrationStates.END))
async def next_n_posts(callback: CallbackQuery, state: StateFilter):
    start_index = int(callback.data.split("_")[2])

    posts = database.posts_db.get_user_posts(callback.message.chat.id, start_index, LIMIT_POSTS_COMMAND + 1)

    next_button = False
    if len(posts) > LIMIT_POSTS_COMMAND:
        next_button = True
        posts = posts[:-1]

    if callback.message.text != "Вот ваши посты:":
        await callback.message.edit_text(text="<b>Вот ваши посты:</b>")

    await callback.message.edit_reply_markup(reply_markup=create_print_n_posts_keyboard(
        start_index,
        posts,
        next_button=next_button,
        back_button=start_index > 0
    ))


@dp.callback_query(F.data.startswith("back_"), StateFilter(RegistrationStates.END))
async def next_n_posts(callback: CallbackQuery, state: StateFilter):
    start_index = int(callback.data.split("_")[1]) - LIMIT_POSTS_COMMAND

    posts = database.posts_db.get_user_posts(callback.message.chat.id, start_index, LIMIT_POSTS_COMMAND + 1)

    next_button = False
    if len(posts) > LIMIT_POSTS_COMMAND:
        next_button = True
        posts = posts[:-1]

    await callback.message.edit_reply_markup(reply_markup=create_print_n_posts_keyboard(
        start_index,
        posts,
        next_button=next_button,
        back_button=start_index > 0
    ))


@dp.callback_query(F.data.startswith("selected_post_"), StateFilter(RegistrationStates.END))
async def select_post(callback: CallbackQuery, state: FSMContext):
    split_data = callback.data.split("_", 4)
    start_index, end_index, post_unique_id = split_data[2:]
    start_index, end_index = int(start_index), int(end_index)

    post_data = database.posts_db.get_post_data_by_post_id(post_unique_id)

    data = {
        "title": post_data[2],
        "description": post_data[3],
        "post_unique_id": post_unique_id
    }

    await state.set_data({"selected_post": post_unique_id})
    await callback.message.edit_text(prepare_post_text(callback.message.chat.id, data))
    await callback.message.edit_reply_markup(reply_markup=
                                             create_post_edit_keyboard(start_index, end_index))


@dp.callback_query(F.data.startswith("edit_post"), StateFilter(RegistrationStates.END))
async def edit_post(callback: CallbackQuery, state: FSMContext):
    start_index, end_index = callback.data.split("_")[2:]
    start_index, end_index = int(start_index), int(end_index)

    post_text = callback.message.text

    await state.set_state(PostEditingStates.EDITING)
    await callback.message.edit_text(post_text + """\n\nИзменение поста:
    1) Указание названия: /t <b>Новое название</b>
    2) Указание описания: /d <b>Новое описание</b>Ы
    
    4) Для удаления поста напишите: <b>/delete</b>
    4) После окончания изменения поста напишите: <b>/edited</b> (Не нужно при удалении!!!)
    
    5) Чтобы увидеть изменения нажмите кнопку <b>"Назад"</b> ниже!
    """, reply_markup=create_editing_post_keyboard(start_index, end_index))


async def get_selected_post_unique_id(state: FSMContext):
    return (await state.get_data())["selected_post"]


@dp.message(Command("t"), StateFilter(PostEditingStates.EDITING))
async def change_post_title(message: Message, state: FSMContext):
    title = message.text.replace("/t", "").strip()

    if not title or len(title) > TITLE_MAX_SIZE:
        await message.reply(f"<b>Название не должно быть пустым."
                            f" И должно занимать меньше {TITLE_MAX_SIZE} символов!</b>")
        return

    post_unique_id = await get_selected_post_unique_id(state)
    kufar_channel_message_id = database.posts_db.get_post_data_by_post_id(post_unique_id)[6]
    kufar_channel_id = database.posts_db.get_post_data_by_post_id(post_unique_id)[5]

    post_data = database.posts_db.get_post_data_by_post_id(post_unique_id)

    data = {
        "title": title,
        "description": post_data[3],
        "post_unique_id": post_unique_id
    }

    text = prepare_post_text(message.chat.id, data)

    await bot.edit_message_caption(kufar_channel_id, kufar_channel_message_id, caption=text)
    database.posts_db.update_post_title(post_unique_id, title)
    await message.answer(f"Название успешно изменено на - {title}")


@dp.message(Command("d"), StateFilter(PostEditingStates.EDITING))
async def change_post_title(message: Message, state: FSMContext):
    description = message.text.replace("/d", "").strip()

    if not description or len(description) > 3500:
        await message.reply(f"<b>Описание не должно быть пустым. И должно занимать меньше 3500 символов!</b>")
        return

    post_unique_id = await get_selected_post_unique_id(state)
    kufar_channel_message_id = database.posts_db.get_post_data_by_post_id(post_unique_id)[6]
    kufar_channel_id = database.posts_db.get_post_data_by_post_id(post_unique_id)[5]

    post_data = database.posts_db.get_post_data_by_post_id(post_unique_id)

    data = {
        "title": post_data[2],
        "description": description,
        "post_unique_id": post_unique_id
    }

    text = prepare_post_text(message.chat.id, data)

    await bot.edit_message_caption(kufar_channel_id, kufar_channel_message_id, caption=text)
    database.posts_db.update_post_description(post_unique_id, description)
    await message.answer(f"Описание успешно изменено на - {description}")


@dp.message(Command("edited"), StateFilter(PostEditingStates.EDITING))
async def stop_editing(message: Message, state: FSMContext):
    await state.set_state(RegistrationStates.END)
    await message.answer("Вы можете вернуться и <b>посмотреть как выглядит пост</b>, а также использовать другие "
                         "команды: <b>/help</b>")


@dp.message(Command("posts"), StateFilter(RegistrationStates.END))
async def print_n_posts(message: Message, state: FSMContext):
    start_index = 0

    posts = database.posts_db.get_user_posts(message.chat.id, start_index, LIMIT_POSTS_COMMAND + 1)

    next_button = False
    if len(posts) > LIMIT_POSTS_COMMAND:
        next_button = True
        posts = posts[:-1]

    await message.answer("<b>Вот ваши посты:</b>", reply_markup=create_print_n_posts_keyboard(
        start_index,
        posts,
        next_button=next_button,
        back_button=start_index > 0
    ))


@dp.message(Command("delete"), StateFilter(PostEditingStates.EDITING))
async def delete_post(message: Message, state: FSMContext):
    post_unique_id = await get_selected_post_unique_id(state)
    database.posts_db.set_deleted(post_unique_id)

    kufar_channel_message_id = database.posts_db.get_post_data_by_post_id(post_unique_id)[6]
    kufar_channel_id = database.posts_db.get_post_data_by_post_id(post_unique_id)[5]

    await bot.delete_message(kufar_channel_id, kufar_channel_message_id)
    await state.set_state(RegistrationStates.END)
    await message.answer("<b>Пост удалён!</b>")


# OLD ALBUMS CAN'T BE EDITED
# @dp.message(Command("PICTURE_WTF"), StateFilter(PostEditingStates.EDITING))
# async def change_pictures(message: Message, state: FSMContext):
#     raise NotImplementedError
#     post_unique_id = await get_selected_post_unique_id(state)
#
#     destination_folder = f"{IMAGES_FOLDER}/{post_unique_id}"
#     for file in tuple(listdir(destination_folder)):
#         remove(f"{destination_folder}/{file}")
#
#     post_data = database.posts_db.get_post_data_by_post_id(post_unique_id)
#
#     data = {
#         "title": post_data[2],
#         "description": post_data[3],
#         "post_unique_id": post_unique_id
#     }
#
#     kufar_channel_message_id = database.posts_db.get_post_data_by_post_id(post_unique_id)[6]
#     kufar_channel_id = database.posts_db.get_post_data_by_post_id(post_unique_id)[5]
#
#     await download_high_resolution_photos(message, destination_folder)
#     await bot.edit_message_media(
#         await create_post(message.chat.id, data, build=False), kufar_channel_id, kufar_channel_message_id)


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.reply("Для регистрации напишите: <b>/start</b>\n"
                        "Для перерегистрации напишите: <b>/unreg</b>\n"
                        "Для помощи по созданию поста напишите: <b>/post</b>\n"
                        "Для управления и просмотра постов напишите: <b>/posts</b>")


async def run_bot() -> None:
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(run_bot())
