from peewee import *

db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

class DeepLinkModel(BaseModel):
    link = CharField()
    
class UserModel(BaseModel):
    user_id = IntegerField()
    user_username = CharField(max_length=35)
    user_nickname = CharField(max_length=130)
    user_task_id = IntegerField(null=True)

class TaskModel(BaseModel):
    task_text = CharField()
    task_photo = CharField()
    task_state = IntegerField()

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

def add_user(user_id: int | str, user_nickname: str, user_username: str):
    UserModel(user_id=user_id, user_username=user_username, user_nickname=user_nickname)