from aiogram.filters import BaseFilter
from aiogram.types import Message
import db 
import config as cfg

class isAdmin(BaseFilter):  
    async def __call__(self, message: Message) -> bool:  
        return message.from_user.id in cfg.ADMINS


class isUser(BaseFilter):  
    async def __call__(self, message: Message) -> bool:  
        return message.from_user.id not in cfg.ADMINS


class isExistsUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return db.check_user_exists(message.from_user.id)