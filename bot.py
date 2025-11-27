import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Твой токен
TOKEN = "8523590707:AAF7hd66xppfiBeDveh-nw0lxSQrvWFiyxk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}
ADMIN_ID = 123456789  # <- твой ID

# Здесь идут все обработчики
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет!")

@dp.message(Command("add"))
async def add_amount(message: Message):
    ...

# Остальные команды...

async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print("Ошибка бота:", e)

if __name__ == "__main__":
    asyncio.run(main())
