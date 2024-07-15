from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

def admin_upd_key() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Обновить ссылку 🔁",
        callback_data="admin_upd_secret_key")
    )
    return builder.as_markup()