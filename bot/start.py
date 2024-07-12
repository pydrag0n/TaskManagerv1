import asyncio
import logging
from loader import bot, dp, cfg
from handlers import handler

logging.basicConfig(level=logging.INFO, 
                    filename=cfg.LOGFILE, 
                    filemode="w", 
                    format="%(asctime)s %(levelname)s %(message)s")

async def start():
    dp.include_router(handler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__=="__main__":
    asyncio.run(start())