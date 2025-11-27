import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiohttp import web

TOKEN = "ТВОЙ_ТОКЕН"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://proverkabota-production.up.railway.app" + WEBHOOK_PATH

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Бот работает через вебхук! 🚀")


async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(app):
    await bot.delete_webhook()


def main():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Получение вебхука
    app.router.add_post(WEBHOOK_PATH, dp.middleware.webhook_handler(bot))

    # Railway даёт порт через переменную окружения
    port = int(os.getenv("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
$PORT
