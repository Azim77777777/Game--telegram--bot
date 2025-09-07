from aiogram import types, Dispatcher
from db import update_balance, get_user

def register_game_handlers(dp: Dispatcher):

    async def crash_cmd(m: types.Message):
        # Пример простой реализации Crash
        user = get_user(m.from_user.id)
        if user[2] < 100:
            await m.answer("❗ Минимальная ставка 100 GG")
            return
        coef = round(random.uniform(1.1, 10), 2)
        win = int(100 * coef)
        chance = user[4]
        is_win = random.randint(1, 100) <= (10 + chance)
        if is_win:
            update_balance(m.from_user.id, win)
            await m.answer(f"💥 Коэффициент: {coef}!\nВы выиграли {win} GG!")
        else:
            update_balance(m.from_user.id, -100)
            await m.answer(f"💥 Коэффициент: {coef}\nВы проиграли 100 GG.")

    async def miner_cmd(m: types.Message):
        # Заглушка: простая выдача случайного бонуса
        win = random.choice([0, 300, 500, 1000])
        update_balance(m.from_user.id, win)
        await m.answer(f"🧨 Miner: Вы получили {win} GG!")

    async def tower_cmd(m: types.Message):
        win = random.choice([0, 500, 2000])
        update_balance(m.from_user.id, win)
        await m.answer(f"🏰 Tower: Выигрыш: {win} GG!")

    async def roulette_cmd(m: types.Message):
        win = random.choice([0, 100, 200, 500, 0, 0, 1000])
        update_balance(m.from_user.id, win)
        await m.answer(f"🎰 Roulette: Выигрыш: {win} GG!")

    async def dice_cmd(m: types.Message):
        number = random.randint(1, 6)
        win = 200 if number == 6 else 0
        update_balance(m.from_user.id, win)
        await m.answer(f"🎲 Выпало: {number}.\n{'Вы выиграли 200 GG!' if win else 'Попробуйте еще!'}")

    dp.register_message_handler(crash_cmd, commands=['crash'])
    dp.register_message_handler(miner_cmd, commands=['miner'])
    dp.register_message_handler(tower_cmd, commands=['tower'])
    dp.register_message_handler(roulette_cmd, commands=['roulette'])
    dp.register_message_handler(dice_cmd, commands=['dice'])
