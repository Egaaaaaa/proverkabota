import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from aiogram.filters import Command
from aiohttp import web

TOKEN = "8523590707:AAF7hd66xppfiBeDveh-nw0lxSQrvWFiyxk"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://proverkabota-production.up.railway.app" + WEBHOOK_PATH

bot = Bot(TOKEN)
dp = Dispatcher()
user_data = {}

# ======== КОМАНДЫ ========

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

    # сообщения всем
    lines = [f"@{u['name']} — всего: {u['total']}₽" for u in user_data.values()]
    total_sum = sum(u["total"] for u in user_data.values())
    text = f"@{username} закинул бабки — {amount}₽\n" + "\n".join(lines) + f"\nОбщая сумма: {total_sum}₽"
    await message.answer(text)

@dp.message(Command("total"))
async def total(message: Message):
    if not user_data:
        return await message.answer("Пока никто ничего не добавил.")
    total_sum = sum(u["total"] for u in user_data.values())
    await message.answer(f"Общая сумма всех участников: {total_sum}₽")

@dp.message(Command("top"))
async def top(message: Message):
    if not user_data:
        return await message.answer("Пока нет участников.")
    sorted_users = sorted(user_data.values(), key=lambda x: x["total"], reverse=True)
    text = "🏆 Топ участников:\n"
    for i, u in enumerate(sorted_users[:10], 1):
        text += f"{i}. @{u['name']} — {u['total']}₽\n"
    await message.answer(text)

@dp.message(Command("reset_user"))
async def reset_user(message: Message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data[user_id]["total"] = 0
        await message.answer("Твоя сумма обнулена ✅")
    else:
        await message.answer("Ты ещё не добавлял сумму.")

# ======== WEBHOOK ========

async def handle(request: web.Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return web.Response(text="ok")

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()

def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    port = int(os.getenv("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
