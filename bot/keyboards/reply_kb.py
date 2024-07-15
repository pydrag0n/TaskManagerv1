from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# For admins
def admin_Panel() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Создать задачу"))
    builder.add(KeyboardButton(text="1"))
    builder.add(KeyboardButton(text="2"))
    builder.add(KeyboardButton(text="Пригласить пользователя"))

    builder.adjust(1, 2, 1)
    return builder.as_markup(resize_keyboard=True)

# For users


