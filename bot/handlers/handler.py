from aiogram import Router, F
from aiogram.filters.command import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import encode_payload, decode_payload, create_start_link
from .gen_link_key import generate_key
import time
from keyboards.inline_kb import admin_upd_key
import loader
import states.state 
import keyboards
import loader
import filters 
from keyboards.reply_kb import admin_Panel
import db



router = Router()

last_update_time = 0
# admin handlers
@router.message(filters.isAdmin(), CommandStart())
async def startBot(message: Message):
    await message.answer("Активация админ-панели...", reply_markup=admin_Panel())

@router.message(filters.isAdmin(), F.text=="Создать задачу")
async def startBot(message: Message):
    await message.answer("получено достижение создатель задач")

@router.message(filters.isAdmin(), F.text=="1")
async def startBot(message: Message):
    await message.answer("получено достижение 1")

@router.message(filters.isAdmin(), F.text=="2")
async def startBot(message: Message):
    await message.answer("получено достижение 2")

@router.message(filters.isAdmin(), F.text=="Пригласить пользователя")
async def startBot(message: Message):
    key = await generate_key()
    db.create_or_update_deep_link(key)
    link = await create_start_link(loader.bot, key, encode=True)
    await message.answer(text=f"Отправьте ссылку пользователю которого хотите добавить: {link}", reply_markup=admin_upd_key())

@router.callback_query(F.data=="admin_upd_secret_key")
async def upd_secret_key(cb: CallbackQuery):
    global last_update_time
    
    # Получить текущее время в секундах
    current_time = time.time()
    
    # Проверить, прошло ли уже больше минуты с момента последнего обновления ссылки
    if current_time - last_update_time >= 60:
        key = await generate_key()
        db.create_or_update_deep_link(key)
        link = await create_start_link(loader.bot, key, encode=True)

        # Обновляем текст сообщения с новой ссылкой
        await cb.bot.edit_message_text(chat_id=cb.message.chat.id, message_id=cb.message.message_id, text=f"Отправьте ссылку пользователю которого хотите добавить: {link}", reply_markup=admin_upd_key())

        await cb.answer(text="Ссылка обновлена...")
        
        # Обновляем время последнего обновления ссылки
        last_update_time = current_time
    else:
        await cb.answer(text="Пожалуйста, подождите 1 минуту перед следующим обновлением ссылки.", show_alert=True)

# ===================================


@router.message(filters.isUser(), CommandStart(deep_link=True))
async def handler(message: Message, command: CommandObject):
    args = command.args
    payload = decode_payload(args)
    
    secret_key = ""
    print(payload, secret_key)
    if payload == secret_key:
        await message.answer(f"Connect key: {payload}")
    else:
        await message.answer("Ссылка устарела")