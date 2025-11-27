import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# ТВОЙ ТОКЕН — вставлен напрямую
TOKEN = "8523590707:AAF7hd66xppfiBeDveh-nw0lxSQrvWFiyxk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}


@dp.message(Command("add"))
async def add_amount(message: Message):
    parts = message.text.split()

    if len(parts) < 2:
        return await message.answer("Используй формат: /add 1500")

    try:
        amount = int(parts[1])
    except ValueError:
        return await message.answer("Сумма должна быть числом.")

    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name

    if user_id not in user_data:
        user_data[user_id] = {"name": username, "total": 0}

    user_data[user_id]["total"] += amount

    lines = []
    total_sum = 0

    for u in user_data.values():
        lines.append(f"@{u['name']} — всего: {u['total']}₽")
        total_sum += u["total"]

    text = (
        f"@{username} закинул бабки в общий доход — {amount}₽\n"
        + "\n".join(lines)
        + f"\nОбщая сумма: {total_sum}₽"
    )

    await message.answer(text)


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
