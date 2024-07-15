from typing import List
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

def admin_upd_key() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Обновить ссылку 🔁",
        callback_data="admin_upd_secret_key")
    )
    return builder.as_markup()

def tasks_list_btn(data: List[List[int, str, str, int]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for d in data:
        builder.add(InlineKeyboardButton(text=d[1], callback_data=f"task_{d[0]}_{d[3]}"))
    return builder.as_markup()

def cancel_task_photo_btn() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="без фото",
        callback_data="cancel_task_photo")
    )
    return builder.as_markup()
    
def task_create_done() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Подтвердить", callback_data="task_create_done"))
    return builder.as_markup()

    
    
    