from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

TOKEN = "ТВОЙ_ТОКЕН"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# user_data хранит пользователей
# Формат: {user_id: {"name": username, "total": число}}
user_data = {}


@dp.message(Command("add"))
async def add_amount(message: Message):
    parts = message.text.split()

    if len(parts) < 2:
        return await message.answer("Используй формат: /add 1500")

    try:
        amount = int(parts[1])
    except ValueError:
        return await message.answer("Сумма должна быть числом. Пример: /add 1500")

    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name

    # Добавляем нового пользователя если его нет
    if user_id not in user_data:
        user_data[user_id] = {"name": username, "total": 0}

    # Обновляем сумму
    user_data[user_id]["total"] += amount

    # Собираем текст для всех участников
    lines = []
    total_sum = 0

    for u in user_data.values():
        lines.append(f"@{u['name']} — всего: {u['total']}₽")
        total_sum += u["total"]

    # Итоговое сообщение
    text = (
        f"@{username} закинул бабки в общий доход — {amount}₽\n"
        + "\n".join(lines)
        + f"\nОбщая сумма: {total_sum}₽"
    )

    await message.answer(text)


@dp.message(Command("total"))
async def total(message: Message):
    if not user_data:
        return await message.answer("Пока никто ничего не добавил.")

    total_sum = sum(u["total"] for u in user_data.values())
    await message.answer(f"Общая сумма всех участников: {total_sum}₽")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
