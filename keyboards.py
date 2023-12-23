from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

categories_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="<-",
            callback_data="category_back"
        ),
        InlineKeyboardButton(
            text="->",
            callback_data="category_next"
        )
    ]
])
