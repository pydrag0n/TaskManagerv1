from typing import List
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
import db

def admin_upd_key() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Обновить ссылку 🔁",
        callback_data="admin_upd_secret_key")
    )
    return builder.as_markup()

def tasks_list_btn() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for d in db.get_tasks_list():
        state = "*0*" # не занято
        if d[3]==1:
            state = "*1*" # занято
        elif d[3]==2:
            state = "*2*" # выполенно
        elif d[3]==3:
            state = "*3*" # не выполненно
        builder.add(InlineKeyboardButton(text=f"{d[1][:15]} {state}", callback_data=f"task_{d[0]}"))
        builder.adjust(1)
    return builder.as_markup()

def cancel_task_photo_btn() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="без фото",
        callback_data="cancel_task_photo")
    )
    return builder.as_markup()
    
# def task_create_done() -> InlineKeyboardMarkup:
#     builder = InlineKeyboardBuilder()
#     builder.add(InlineKeyboardButton(text="Подтвердить", callback_data="task_create_done"))
#     return builder.as_markup()

def change_task_state(task_id: int, task_state: int) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()
    if task_state==0:
        builder.add(InlineKeyboardButton(text="взять", callback_data=f"statechange_{task_id}_1"))
    elif task_state==1:
        builder.add(InlineKeyboardButton(text="завершить", callback_data=f"statechange_{task_id}_2"))
        builder.add(InlineKeyboardButton(text="отмена", callback_data=f"statechange_{task_id}_0"))
    elif task_state==2:
        builder.add(InlineKeyboardButton(text="отмена", callback_data=f"statechange_{task_id}_0"))
        
    return builder.as_markup()
    