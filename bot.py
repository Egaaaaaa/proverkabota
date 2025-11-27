import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import web

# ====== Настройки ======
TOKEN = os.getenv("TOKEN")  # Telegram Bot Token
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")  # Домен или IP сервера
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))  # твой ID для reset_all

# ====== Команды ======

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

async def send_balances(message: Message):
    total_sum = sum(user_data.values())
    balances = ""
    for uid, bal in user_data.items():
        try:
            user = await bot.get_chat(uid)
            uname = user.username or user.first_name
            balances += f"@{uname} — всего: {bal}₽\n"
        except:
            balances += f"{uid} — всего: {bal}₽\n"
    balances += f"Общая сумма: {total_sum}₽"
    await message.answer(balances)

@dp.message(Command("add"))
async def add_amount(message: Message):
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("Используй формат: /add 1500")
    amount = int(parts[1])
    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.first_name
    user_data[user_id] = user_data.get(user_id, 0) + amount

    await message.answer(f"@{user_name} закинул бабки в общий доход — {amount}₽")
    await send_balances(message)

@dp.message(Command("remove"))
async def remove_amount(message: Message):
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("Используй формат: /remove 500")
    amount = int(parts[1])
    user_id = message.from_user.id
    current = user_data.get(user_id, 0)
    if amount > current:
        return await message.answer(f"У тебя недостаточно средств. Текущий баланс: {current}₽")
    user_data[user_id] = current - amount
    user_name = message.from_user.username or message.from_user.first_name

    await message.answer(f"@{user_name} снял бабки из общего дохода — {amount}₽")
    await send_balances(message)

@dp.message(Command("total"))
async def total(message: Message):
    if not user_data:
        return await message.answer("Пока никто ничего не добавил.")
    await send_balances(message)

@dp.message(Command("my"))
async def my_balance(message: Message):
    user_id = message.from_user.id
    bal = user_data.get(user_id, 0)
    await message.answer(f"Твой баланс: {bal}₽")

@dp.message(Command("top"))
async def top_users(message: Message):
    top = sorted(user_data.items(), key=lambda x: x[1], reverse=True)
    text = "Топ участников:\n"
    for uid, bal in top[:10]:
        user = await bot.get_chat(uid)
        uname = user.username or user.first_name
        text += f"@{uname}: {bal}₽\n"
    await message.answer(text)

@dp.message(Command("reset_user"))
async def reset_user(message: Message):
    user_id = message.from_user.id
    user_data[user_id] = 0
    await message.answer("Твой баланс обнулён.")

@dp.message(Command("reset_all"))
async def reset_all(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("У тебя нет прав для этой команды.")
    user_data.clear()
    await message.answer("Все балансы обнулены админом.")

# ====== Webhook сервер ======
async def handle(request):
    update = types.Update(**await request.json())
    await dp.process_update(update)
    return web.Response()

app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle)

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()

app.on_startup.append(on_startup)
app.on_cleanup.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
