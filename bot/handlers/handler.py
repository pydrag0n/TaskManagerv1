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
from keyboards.inline_kb import admin_upd_key, tasks_list_btn, change_task_state
from keyboards.reply_kb import admin_Panel, user_panel, cancel_btn, cancel_task_photo_btn, next_task_state
import loader
from states.state import CreateTaskState
# import messages_text as msgtext
import loader
import my_filters
import db
import json
import config
# Load the JSON file
with open(config.MSG_FILE, 'r', encoding="utf-8") as f:
    data = json.load(f)

# Access the data
for_admin = data.get("for-admin")
for_user = data.get("for-user")



router = Router()

last_update_time = 0
# admin handlers
@router.message(my_filters.isAdmin(), CommandStart())
async def startBot(message: Message):
    await message.answer(text=for_admin["activate-panel"], reply_markup=admin_Panel())

@router.message(my_filters.isAdmin(), StateFilter(None), F.text.lower()=="создать задачу")
async def createtask(message: Message, state: FSMContext):
    await message.answer(text=for_admin["create-task-fsm"]["send-task-text"], reply_markup=cancel_btn())
    await state.set_state(CreateTaskState.task_text)

@router.message(F.text.lower()=="отмена")
async def cancelf(message: Message, state: FSMContext):
    await message.answer(text=for_admin["create-task-fsm"]["cancel"], reply_markup=admin_Panel())
    await state.clear()


@router.message(my_filters.isAdmin(), StateFilter(CreateTaskState.task_text), F.text)
async def gettasktext(message: Message, state: FSMContext):
    # await state.update_data(task_text=message.text)
    await message.answer(text=for_admin["create-task-fsm"]["send-task-photo"], reply_markup=cancel_task_photo_btn())
    await state.update_data(task_text=message.text)
    await state.set_state(CreateTaskState.task_photo)


@router.message(my_filters.isAdmin(), StateFilter(CreateTaskState.task_photo), F.text | F.photo)
async def gettaskphoto(message: Message, state: FSMContext):
            
    if message.content_type==ContentType.PHOTO:
        file_id = message.photo[0].file_id
        await state.update_data(photo=file_id)
        await state.set_state(CreateTaskState.create_task)
        await message.answer(text=for_admin["create-task-fsm"]["check-and-confirm"], reply_markup=next_task_state())
    elif message.text.lower()=='без фото':
        await state.update_data(photo=None)
        await state.set_state(CreateTaskState.create_task)
        await message.answer(text=for_admin["create-task-fsm"]["check-and-confirm"], reply_markup=next_task_state())
    else:
        await message.answer(text=for_admin["create-task-fsm"]["error"])
        
@router.message(my_filters.isAdmin(), StateFilter(CreateTaskState.create_task))
async def createtas_Done(message: Message, state: FSMContext):
    data = await state.get_data()
    task_text = data.get("task_text")
    task_photo = data.get("photo")
    # print(task_text, task_photo)
    if task_photo is None:
        await message.answer(text=f"{for_admin['create-task-fsm']['your-task-no-photo']} __{task_text}__")
    else: 
        await message.answer(text=f"{for_admin['create-task-fsm']['your-task-photo']} __{task_text}__")
    db.create_task(task_text, task_photo)
    await message.answer(text=for_admin["create-task-fsm"]["successfully-create-task"], reply_markup=admin_Panel())
    await state.clear()


@router.message(my_filters.isAdmin(), F.text.lower()=="пригласить пользователя")
async def addUserOnLink(message: Message):
    key = await generate_key()
    db.create_or_update_deep_link(key)
    link = await create_start_link(loader.bot, key, encode=True)
    await message.answer(text=f"{for_admin['add-user']} `{link}`", reply_markup=admin_upd_key())


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
        await cb.bot.edit_message_text(chat_id=cb.message.chat.id, message_id=cb.message.message_id, text=f"{for_admin['add-user']} `{link}`", reply_markup=admin_upd_key())

        await cb.answer(text=for_admin["link-update"])
        
        # Обновляем время последнего обновления ссылки
        last_update_time = current_time
    else:
        await cb.answer(text=for_admin["upd-link-timeout"], show_alert=True)

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

@router.message(my_filters.isAdmin(),  F.text.lower()=="список задач")
async def show_task_list(message: Message):
    await message.answer("Задачи: ", reply_markup=tasks_list_btn())



@router.message(my_filters.isUser(), my_filters.isExistsUser(),  F.text.lower()=="список задач")
async def show_task_list(message: Message):
    await message.answer("Задачи: ", reply_markup=tasks_list_btn())


@router.callback_query(F.data.split("_")[0]=="task")
async def task_list_inline_kb(cb: CallbackQuery):
    btn_data = cb.data.split("_")
    task_id = btn_data[1]
    task_data = db.get_task_data(int(task_id))
    task_text = task_data[0]
    task_photo = task_data[1]
    task_state = task_data[2]
    if not task_photo is None:
        await cb.bot.send_photo(chat_id=cb.message.chat.id, 
                          photo=task_photo, 
                          caption=f"ID: `{task_id}`\n{task_text}", reply_markup=change_task_state(task_id, task_state))

    else:
        await cb.bot.send_message(chat_id=cb.message.chat.id, 
                            text=task_text, reply_markup=change_task_state(task_id, task_state))

@router.callback_query(F.data.split("_")[0]=="statechange")
async def setstate_task(cb: CallbackQuery):
    cb_dt = cb.data.split("_")
    task_id = cb_dt[1]
    task_state = int(cb_dt[2])
    user_id = cb.message.chat.id
    user_task_id = db.user_task_id_exist(task_id)
    print(task_state)
    # if db.user_task_id_exist(task_id) == user_id:
    print(user_task_id, user_id)
    
    if task_state==1:
        db.set_user_task_id(task_id, user_id)
        db.set_task_state(task_id, task_state)
    # elif task_state==0:
    #     db.del_user_task_id(task_id)

    elif user_task_id==int(user_id):
        db.set_task_state(task_id, task_state)

    elif user_task_id!=int(user_id):
        await cb.answer(text="Вы не имеете доступа к этой операции", show_alert=True)

    await cb.bot.send_message(chat_id=cb.message.chat.id, text="Данные обновлены, нажмите на: **Список задач**")