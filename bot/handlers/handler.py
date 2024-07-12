from aiogram import Router, F
from aiogram.filters.command import CommandStart, Command
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def startBot(message: Message):
    pass

