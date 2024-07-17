from typing import List
from peewee import *
import config

db = SqliteDatabase(config.DATABASE)

class BaseModel(Model):
    class Meta:
        database = db

class DeepLinkModel(BaseModel):
    link = CharField()
    
class UserModel(BaseModel):
    user_id = IntegerField()
    user_username = CharField(max_length=35)
    user_nickname = CharField(max_length=130)

class TaskModel(BaseModel):
    task_text = CharField()
    task_photo = CharField(null=True)
    task_state = IntegerField(default=0)
    user_task_id = IntegerField(null=True)


db.create_tables([DeepLinkModel, UserModel, TaskModel])

def create_or_update_deep_link(new_link: str):
    existing_link = DeepLinkModel.select().first()

    if existing_link:
        existing_link.link = new_link
        existing_link.save()
    else:
        DeepLinkModel(link=new_link).save()
    
def get_deep_link(deep_link_id:int=1):
    deep_link = DeepLinkModel.get(DeepLinkModel.id == deep_link_id)
    
    if deep_link:
        return deep_link.link
    else:
        return None


def check_user_exists(user_id) -> bool:
    user_exists = UserModel.select().where(UserModel.user_id == user_id).exists()
    return user_exists


def add_user(user_id: int | str, user_nickname: str, user_username: str):
    UserModel(user_id=user_id, user_username=user_username, user_nickname=user_nickname).save()

def create_task(task_text: str, task_photo: str):
    TaskModel(task_text=task_text, task_photo=task_photo).save()

def set_task_state(task_id: int | str, task_state: int):
    task = TaskModel.get_by_id(task_id)
    task.task_state = task_state
    task.save()
    
def get_tasks_list() -> List[List[str | int]]:
    tasks = TaskModel.select()
    data = []
    
    for task in tasks:
        data.append([task.id, task.task_text, task.task_photo, task.task_state])
    
    return data

def get_task_state(task_id: int):
    task = TaskModel.get_by_id(task_id)
    return task.task_state

def get_task_data(task_id: int) -> List[str | str | int]:
    task = TaskModel.get_by_id(task_id)
    data = []
    data.append(task.task_text)
    data.append(task.task_photo)
    data.append(task.task_state)
    return data

def set_user_task_id(task_id, user_id):
    task = TaskModel.get_by_id(task_id)
    task.user_task_id = user_id
    task.save()

def del_user_task_id(task_id):
    task = TaskModel.get_by_id(task_id)
    task.user_task_id = None
    task.save()

def user_task_id_exist(task_id):
    task = TaskModel.get_by_id(task_id)
    return task.user_task_id

    