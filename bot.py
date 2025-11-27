import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Твой токен Telegram
TOKEN = "8523590707:AAF7hd66xppfiBeDveh-nw0lxSQrvWFiyxk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

ADMIN_ID = 123456789  # <- замени на свой Telegram ID для админских команд

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! 👋\n"
        "Отправь сумму в формате:\n"
        "/add 1500\n\n"
        "Команды:\n"
        "/add <сумма> — добавить доход\n"
        "/remove <сумма> — снять часть дохода\n"
        "/total — общий доход всех участников\n"
        "/my — твоя история\n"
        "/top — топ участников\n"
        "/reset_user — обнулить свой доход\n"
        "/reset_all — обнулить всех (только админ)"
    )

@dp.message(Command("add"))
async def add_amount(message: Message):
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("Используй формат: /add 1500")
    amount = int(parts[1])
    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.first_name
    user_data[user_id] = user_data.get(user_id, 0) + amount
    total_sum = sum(user_data.values())

    # Первое сообщение — кто добавил
    await message.answer(f"@{user_name} закинул бабки в общий доход — {amount}₽")
    # Второе сообщение — состояние пользователя и общий доход
    await message.answer(f"@{user_name} — всего: {user_data[user_id]}₽\nОбщая сумма: {total_sum}₽")

@dp.message(Command("remove"))
async def remove_amount(message: Message):
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("Используй формат: /remove 500")
    amount = int(parts[1])
    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.first_name
    current = user_data.get(user_id, 0)
    if amount > current:
        return await message.answer(f"У тебя недостаточно средств. Текущий баланс: {current}₽")
    user_data[user_id] = current - amount
    total_sum = sum(user_data.values())

    # Первое сообщение — кто снял
    await message.answer(f"@{user_name} снял бабки из общего дохода — {amount}₽")
    # Второе сообщение — состояние пользователя и общий доход
    await message.answer(f"@{user_name} — всего: {user_data[user_id]}₽\nОбщая сумма: {total_sum}₽")

@dp.message(Command("total"))
async def total(message: Message):
    if not user_data:
        return await message.answer("Пока никто ничего не добавил.")
    total_sum = sum(user_data.values())
    await message.answer(f"Общий доход всех участников: {total_sum}₽")

@dp.message(Command("my"))
async def my_history(message: Message):
    user_id = message.from_user.id
    total = user_data.get(user_id, 0)
    await message.answer(f"Твой доход: {total}₽")

@dp.message(Command("top"))
async def top_users(message: Message):
    if not user_data:
        return await message.answer("Пока нет данных для топа.")
    sorted_users = sorted(user_data.items(), key=lambda x: x[1], reverse=True)
    text = "Топ участников:\n"
    for i, (uid, amount) in enumerate(sorted_users[:10], start=1):
        user_name = (await bot.get_chat(uid)).username or (await bot.get_chat(uid)).first_name
        text += f"{i}. @{user_name} — {amount}₽\n"
    await message.answer(text)

@dp.message(Command("reset_user"))
async def reset_user(message: Message):
    user_id = message.from_user.id
    user_data[user_id] = 0
    await message.answer("Твой доход обнулён.")

@dp.message(Command("reset_all"))
async def reset_all(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("У тебя нет прав на эту команду.")
    user_data.clear()
    await message.answer("Все доходы обнулены.")

async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print("Ошибка бота:", e)

if __name__ == "__main__":
    asyncio.run(main())
