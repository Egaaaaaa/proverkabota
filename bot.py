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

    # Второе сообщение — все пользователи с их балансом + общая сумма
    balances = ""
    for uid, bal in user_data.items():
        uname = (await bot.get_chat(uid)).username or (await bot.get_chat(uid)).first_name
        balances += f"@{uname} — всего: {bal}₽\n"
    balances += f"Общая сумма: {total_sum}₽"
    await message.answer(balances)


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

    # Второе сообщение — все пользователи с их балансом + общая сумма
    balances = ""
    for uid, bal in user_data.items():
        uname = (await bot.get_chat(uid)).username or (await bot.get_chat(uid)).first_name
        balances += f"@{uname} — всего: {bal}₽\n"
    balances += f"Общая сумма: {total_sum}₽"
    await message.answer(balances)
