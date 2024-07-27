import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import asyncio
import logging
import loader
from handlers import handler

logging.basicConfig(level=logging.INFO,
                    # filename=loader.cfg.LOGFILE,
                    # filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

async def start():
    loader.dp.include_router(handler.router)
    await loader.bot.delete_webhook(drop_pending_updates=True)
    await loader.dp.start_polling(loader.bot)


if __name__=="__main__":
    asyncio.run(start())