from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

CONTACT_TYPES = [
    [
        InlineKeyboardButton(text="Почта", callback_data="contacts_email"),
        InlineKeyboardButton(text="Номер телефона", callback_data="contacts_phone"),
        InlineKeyboardButton(text="Telegram", callback_data="contacts_telegram")
    ],
    [
        InlineKeyboardButton(text="Изменить имя", callback_data="restore_nickname")
    ]
]


def create_print_n_posts_keyboard(start_index: int, posts_data: tuple[tuple],
                                   next_button: bool = False, back_button: bool = False):
    keyboard = []
    end_index = start_index + len(posts_data)

    for post_index, post_data in zip(range(start_index, end_index), posts_data):
        keyboard.append([
            InlineKeyboardButton(text=f"{post_index}) {post_data[2]}",
                                 callback_data=f"selected_post_{start_index}_{end_index}_{post_data[0]}")
        ])

    if next_button or back_button:
        keyboard.append([])

    if back_button:
        keyboard[-1].append(InlineKeyboardButton(text="<- Сюда", callback_data=f"back_{start_index}_{end_index}"))
    if next_button:
        keyboard[-1].append(InlineKeyboardButton(text="Туда ->", callback_data=f"next_{start_index}_{end_index}"))

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_post_edit_keyboard(start_index: int, end_index: int):
    offset = end_index - start_index

    keyboard = [
        [
            InlineKeyboardButton(text="Назад",
                                 callback_data=f"next_{start_index - offset}_{end_index - offset}")
        ],
        [
            InlineKeyboardButton(text="Изменить пост",
                                 callback_data=f"edit_post_{start_index}_{end_index}")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_editing_post_keyboard(start_index: int, end_index: int):
    offset = end_index - start_index

    keyboard = [
        [
            InlineKeyboardButton(text="Назад",
                                 callback_data=f"next_{start_index - offset}_{end_index - offset}")
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
