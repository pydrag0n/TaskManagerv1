from aiogram import Router, F
from aiogram.filters.command import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.enums.content_type import ContentType
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import encode_payload, decode_payload, create_start_link
from .gen_link_key import generate_key
import time
from keyboards.inline_kb import admin_upd_key, tasks_list_btn, task_create_done
from keyboards.reply_kb import admin_Panel, user_panel, cancel_btn, cancel_task_photo_btn, next_task_state
import loader
from states.state import CreateTaskState
import keyboards
import loader
import my_filters
import db



router = Router()

last_update_time = 0
# admin handlers
@router.message(my_filters.isAdmin(), CommandStart())
async def startBot(message: Message):
    await message.answer("Активация админ-панели...", reply_markup=admin_Panel())

@router.message(my_filters.isAdmin(), StateFilter(None), F.text.lower()=="создать задачу")
async def createtask(message: Message, state: FSMContext):
    await message.answer("Введите текст задачи: ", reply_markup=cancel_btn())
    await state.set_state(CreateTaskState.task_text)

@router.message(F.text.lower()=="отмена")
async def cancelf(message: Message, state: FSMContext):
    await message.answer("Отмена...", reply_markup=admin_Panel())
    await state.clear()


@router.message(my_filters.isAdmin(), StateFilter(CreateTaskState.task_text), F.text)
async def gettasktext(message: Message, state: FSMContext):
    # await state.update_data(task_text=message.text)
    await message.answer("Отправьте фото задачи (необязательно)", reply_markup=cancel_task_photo_btn())
    await state.update_data(task_text=message.text)
    await state.set_state(CreateTaskState.task_photo)


@router.message(my_filters.isAdmin(), StateFilter(CreateTaskState.task_photo), F.text | F.photo)
async def gettaskphoto(message: Message, state: FSMContext):
            
    if message.content_type==ContentType.PHOTO:
        file_id = message.photo[0].file_id
        await state.update_data(photo=file_id)
        await state.set_state(CreateTaskState.create_task)
        await message.answer("Проверьте и подтвердите", reply_markup=next_task_state())
    elif message.text.lower()=='без фото':
        await state.update_data(photo=None)
        await state.set_state(CreateTaskState.create_task)
        await message.answer("Проверьте и подтвердите", reply_markup=next_task_state())
    else:
        await message.answer("Ошибка...")
        
@router.message(my_filters.isAdmin(), StateFilter(CreateTaskState.create_task))
async def createtas_Done(message: Message, state: FSMContext):
    data = await state.get_data()
    task_text = data.get("task_text")
    task_photo = data.get("photo")
    
    if task_photo is None:
        await message.answer(f"Ваша задача:\n**фото**: __без фото__\n**текст**: __{task_text}__", reply_markup=task_create_done())
    else: 
        await message.answer(f"Ваша задача:\n**фото**: __с фото__\n**текст**: __{task_text}__", reply_markup=task_create_done())

@router.callback_query(F.data=="task_create_done")
async def task_create_done_cb(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer("данные сохранены в базу...", reply_markup=admin_Panel())
    data = await state.get_data()
    task_text = data.get("task_text")
    task_photo = data.get("task_photo")
    print(task_text, task_photo)
    db.create_task(task_text, task_photo)
    
    await state.clear()


@router.message(my_filters.isAdmin(), F.text.lower()=="пригласить пользователя")
async def startBot(message: Message):
    key = await generate_key()
    db.create_or_update_deep_link(key)
    link = await create_start_link(loader.bot, key, encode=True)
    await message.answer(text=f"Отправьте ссылку пользователю которого хотите добавить: `{link}`", reply_markup=admin_upd_key())


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
        await cb.bot.edit_message_text(chat_id=cb.message.chat.id, message_id=cb.message.message_id, text=f"Отправьте ссылку пользователю которого хотите добавить: `{link}`", reply_markup=admin_upd_key())

        await cb.answer(text="Ссылка обновлена...")
        
        # Обновляем время последнего обновления ссылки
        last_update_time = current_time
    else:
        await cb.answer(text="Пожалуйста, подождите 1 минуту перед следующим обновлением ссылки.", show_alert=True)

# ===================================


@router.message(my_filters.isUser(), CommandStart(deep_link=True))
async def upddeeplink(message: Message, command: CommandObject):
    args = command.args
    payload = decode_payload(args)
    
    secret_key = db.get_deep_link()
    # print(payload, secret_key)
    user_id = message.from_user.id
    if payload == secret_key:
        if not db.check_user_exists(user_id):
            db.add_user(user_id=user_id, user_nickname=message.from_user.full_name, user_username=message.from_user.username)
        await message.answer(f"Connect key: {payload}", reply_markup=user_panel())    
    else:
        await message.answer("Ссылка устарела")

@router.message(my_filters.isUser(), my_filters.isExistsUser(), F.text.lower()=="список задач")
async def show_task_list(message: Message):
    await message.answer("TASKS: ", reply_markup=tasks_list_btn())


