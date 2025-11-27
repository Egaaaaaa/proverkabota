from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
# Source - https://stackoverflow.com/a
# Posted by Greg, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-27, License - CC BY-SA 3.0

from subprocess import Popen
from win32process import DETACHED_PROCESS

pid = Popen(["C:\python24\python.exe", "long_run.py"],creationflags=DETACHED_PROCESS,shell=True).pid
print(pid)
print('done')

#I can now close the console or anything I want and long_run.py continues!


TOKEN = "8523590707:AAF7hd66xppfiBeDveh-nw0lxSQrvWFiyxk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! 👋\n"
        "Отправь сумму в формате:\n"
        "/add 1500\n\n"
        "Команды:\n"
        "/add <сумма> — добавить заработок\n"
        "/total — посмотреть общий заработок"
    )

@dp.message(Command("add"))
async def add_amount(message: Message):
    parts = message.text.split()

    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("Используй формат: /add 1500")

    amount = int(parts[1])
    user_id = message.from_user.id

    user_data[user_id] = user_data.get(user_id, 0) + amount

    await message.answer(f"Добавлено: {amount}₸\nТвой итог: {user_data[user_id]}₸")

@dp.message(Command("total"))
async def total(message: Message):
    if not user_data:
        return await message.answer("Пока никто ничего не добавил.")

    total_sum = sum(user_data.values())
    await message.answer(f"Общий заработок всех участников: {total_sum}₸")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
