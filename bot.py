from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

# Токен бота
TOKEN = "ТВОЙ_ТОКЕН"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# История пользователей
# Формат: {user_id: {"name": username, "total": сумма}}
user_data = {}

# Админ ID для команды /reset_all
ADMIN_ID = 123456789  # замени на свой ID

# ===== /add =====
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

    if user_id not in user_data:
        user_data[user_id] = {"name": username, "total": 0}

    user_data[user_id]["total"] += amount

    total_user_amount = user_data[user_id]["total"]
    total_all_users = sum(u["total"] for u in user_data.values())

    # 1️⃣ Кто добавил
    await message.answer(f"@{username} закинул бабки в общий доход — {amount}₽")

    # 2️⃣ Сумма пользователя и общая сумма
    await message.answer(
        f"@{username} — всего: {total_user_amount}₽\n"
        f"Общая сумма: {total_all_users}₽"
    )

# ===== /total =====
@dp.message(Command("total"))
async def total(message: Message):
    if not user_data:
        return await message.answer("Пока никто ничего не добавил.")
    total_sum = sum(u["total"] for u in user_data.values())

    # Форматированный вывод всех пользователей
    lines = [f"@{u['name']} — всего: {u['total']}₽" for u in user_data.values()]
    lines.append(f"Общая сумма: {total_sum}₽")
    await message.answer("\n".join(lines))

# ===== /remove =====
@dp.message(Command("remove"))
async def remove_amount(message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("Используй формат: /remove 1500")

    try:
        amount = int(parts[1])
    except ValueError:
        return await message.answer("Сумма должна быть числом.")

    user_id = message.from_user.id
    if user_id not in user_data or user_data[user_id]["total"] == 0:
        return await message.answer("У тебя нет средств для снятия.")

    user_data[user_id]["total"] = max(0, user_data[user_id]["total"] - amount)
    await message.answer(f"Снято {amount}₽. Твой баланс: {user_data[user_id]['total']}₽")

# ===== /reset_user =====
@dp.message(Command("reset_user"))
async def reset_user(message: Message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data[user_id]["total"] = 0
    await message.answer("Твой доход обнулён ✅")

# ===== /reset_all =====
@dp.message(Command("reset_all"))
async def reset_all(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("Только админ может использовать эту команду.")
    for u in user_data.values():
        u["total"] = 0
    await message.answer("Все доходы обнулены ✅")

# ===== /my =====
@dp.message(Command("my"))
async def my_history(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        return await message.answer("У тебя пока нет доходов.")
    await message.answer(f"@{user_data[user_id]['name']} — всего: {user_data[user_id]['total']}₽")

# ===== /top =====
@dp.message(Command("top"))
async def top_users(message: Message):
    if not user_data:
        return await message.answer("Пока никто ничего не добавил.")
    sorted_users = sorted(user_data.values(), key=lambda x: x["total"], reverse=True)
    lines = [f"@{u['name']} — {u['total']}₽" for u in sorted_users]
    await message.answer("🏆 Топ пользователей:\n" + "\n".join(lines))

# ===== Запуск бота =====
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
