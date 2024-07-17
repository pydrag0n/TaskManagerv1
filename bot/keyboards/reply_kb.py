from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# For admins
def admin_Panel() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Создать задачу"))
    builder.add(KeyboardButton(text="Список задач"))
    builder.add(KeyboardButton(text="Пригласить пользователя"))
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

# For users

def user_panel() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Список задач"))
    builder.add(KeyboardButton(text="Помощь"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def cancel_btn() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Отмена"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def cancel_task_photo_btn():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Без фото"))
    builder.add(KeyboardButton(text="Отмена"))
    
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def next_task_state():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Подтвердить"))
    builder.add(KeyboardButton(text="Отмена"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)