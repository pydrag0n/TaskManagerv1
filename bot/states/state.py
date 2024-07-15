from aiogram.fsm.state import StatesGroup, State

class CreateTaskState(StatesGroup):
    task_text = State()
    task_photo = State()
    create_task = State()