import asyncio

from aiogram import Dispatcher, Router

from bot.telegram import test_task_bot

router = Router()
dp = Dispatcher()
dp.include_router(test_task_bot.router)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(test_task_bot.bot))
