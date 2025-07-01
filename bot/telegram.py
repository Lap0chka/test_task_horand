from aiogram import Bot
from aiogram import Router, F, types
from aiogram.filters import Command

from bot.parser import pars
from bot.settings import TELEGRAM_BOT_TOKEN


class TestTaskBot:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.router = Router()
        self._register()

    async def send_message(self, text, chat_id, **kwargs):
        await self.bot.send_message(chat_id=chat_id, text=text, **kwargs)

    async def close_session(self):
        await self.bot.session.close()

    def _register(self):
        self.router.message.register(self.say_hello, Command("start"))
        self.router.message.register(self.short_description, Command("about"))
        self.router.message.register(self.run_parser, F.text == "/run")

    @staticmethod
    async def say_hello(message: types.Message):
        await message.reply("Ласкаво просимо")

    @staticmethod
    async def short_description(message: types.Message):
        await message.reply("Коротка iнформацiя про бот ")

    @staticmethod
    async def run_parser(message: types.Message):
        try:
            quotes = pars.start_parser()
            text = "Успішно залогінено. Ось ваші цитати:\n\n"
            for q in quotes:
                text += f"— {q}\n\n"
            await message.reply(text)
        except Exception as e:
            await message.reply(f"Виникла помилка: {e}")


test_task_bot = TestTaskBot()
