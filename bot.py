from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import os

# Токен берём из переменной окружения
TOKEN = os.getenv("TOKEN")
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
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print("Ошибка бота:", e)

if __name__ == "__main__":
    asyncio.run(main())
