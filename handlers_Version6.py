from aiogram import types, Dispatcher
import time
import random
from db import (
    get_user, update_balance, set_user_chance, set_user_status,
    reset_bonus_time, reset_box_time, get_profile, get_top_users, set_hide_top,
    get_all_user_ids, create_promo, use_promo, get_promo_logs
)

ADMIN_IDS = [123456789]  # Замени на свои Telegram ID

START_MENU = (
    "╔══════════════════╗\n"
    "   📖 Меню и помощь\n"
    "╚══════════════════╝\n\n"
    "🔹 Основные команды:\n"
    "  /profile — ваш профиль\n"
    "  /bonus — получить бонус (1000–10000 GG/час)\n"
    "  /top — топ игроков\n"
    "  /hide — скрыть/показать себя в топе\n"
    "  /status — купить статус\n"
    "  /box — открыть коробку (раз в 6 часов)\n"
    "  /pay сумма ID — перевести GG другу\n"
    "  /farm — ферма для добычи монет\n"
    "  /bank — банк GG\n"
    "  /promo код — активировать промокод\n"
    "  /games — список игр\n"
    "  /admin — меню администратора\n"
    "  /help — справка\n"
)

GAME_LIST = (
    "🎲 Игры:\n"
    "/crash — угадай взрыв\n"
    "/miner — клетки и мины\n"
    "/tower — проходи уровни\n"
    "/roulette — ставки на числа/цвет\n"
    "/dice — брось кости\n"
)

def register_handlers(dp: Dispatcher):

    async def start_cmd(m: types.Message):
        get_user(m.from_user.id, m.from_user.username)
        await m.answer(START_MENU)

    async def help_cmd(m: types.Message):
        await m.answer(START_MENU)

    async def profile_cmd(m: types.Message):
        get_user(m.from_user.id, m.from_user.username)
        username, balance, status, chance = get_profile(m.from_user.id)
        await m.answer(f"👤 Профиль:\n"
                       f"Имя: {username}\n"
                       f"ID: {m.from_user.id}\n"
                       f"Баланс: {balance} GG\n"
                       f"Статус: {status}\n"
                       f"Шанс на выигрыш: {chance}%")

    async def bonus_cmd(m: types.Message):
        user = get_user(m.from_user.id, m.from_user.username)
        now = int(time.time())
        if now - user[5] < 3600:
            mins = (3600 - (now - user[5])) // 60
            await m.answer(f"⏳ Бонус можно получить через {mins} мин.")
        else:
            bonus = random.randint(1000, 10000)
            update_balance(m.from_user.id, bonus)
            reset_bonus_time(m.from_user.id)
            await m.answer(f"💰 Ваш бонус: {bonus} GG")

    async def top_cmd(m: types.Message):
        top = get_top_users()
        msg = "🏆 Топ игроков:\n"
        for i, (uid, username, balance) in enumerate(top, 1):
            msg += f"{i}) {username or uid}: {balance} GG\n"
        await m.answer(msg)

    async def hide_cmd(m: types.Message):
        user = get_user(m.from_user.id, m.from_user.username)
        val = 0 if user[6] else 1
        set_hide_top(m.from_user.id, val)
        await m.answer("🙈 Статус в топе изменён.")

    async def pay_cmd(m: types.Message):
        try:
            _, amount, uid = m.text.split()
            update_balance(m.from_user.id, -int(amount))
            update_balance(int(uid), int(amount))
            await m.answer(f"✅ Переведено {amount} GG пользователю {uid}")
        except Exception:
            await m.answer("❌ Формат: /pay сумма ID")

    async def status_cmd(m: types.Message):
        await m.answer("🧑‍🎓 Статусы:\nVIP — 10000 GG\nPremium — 50000 GG\nДля покупки напишите /setstatus ваш статус")

    async def box_cmd(m: types.Message):
        user = get_user(m.from_user.id, m.from_user.username)
        now = int(time.time())
        if now - user[7] < 21600:
            mins = (21600 - (now - user[7])) // 60
            await m.answer(f"⏳ Коробку можно открыть через {mins} мин.")
        else:
            prize = random.choice([1000, 2000, 5000, 10000, 0])
            update_balance(m.from_user.id, prize)
            reset_box_time(m.from_user.id)
            await m.answer(f"🎁 Коробка открыта! Вы получили: {prize} GG")

    async def farm_cmd(m: types.Message):
        update_balance(m.from_user.id, random.randint(100, 500))
        await m.answer("🌱 Ваша ферма принесла монеты!")

    async def bank_cmd(m: types.Message):
        user = get_user(m.from_user.id, m.from_user.username)
        await m.answer(f"🔒 Ваш банк: {user[2]} GG\nДля вклада: /bank сумма")

    async def promo_cmd(m: types.Message):
        try:
            _, code = m.text.split()
            reward, msg = use_promo(m.from_user.id, code)
            await m.answer(msg)
        except Exception:
            await m.answer("❌ Формат: /promo КОД")

    async def games_cmd(m: types.Message):
        await m.answer(GAME_LIST)

    dp.register_message_handler(start_cmd, commands=['start'])
    dp.register_message_handler(help_cmd, commands=['help'])
    dp.register_message_handler(profile_cmd, commands=['profile'])
    dp.register_message_handler(bonus_cmd, commands=['bonus'])
    dp.register_message_handler(top_cmd, commands=['top'])
    dp.register_message_handler(hide_cmd, commands=['hide'])
    dp.register_message_handler(pay_cmd, commands=['pay'])
    dp.register_message_handler(status_cmd, commands=['status'])
    dp.register_message_handler(box_cmd, commands=['box'])
    dp.register_message_handler(farm_cmd, commands=['farm'])
    dp.register_message_handler(bank_cmd, commands=['bank'])
    dp.register_message_handler(promo_cmd, commands=['promo'])
    dp.register_message_handler(games_cmd, commands=['games'])

def register_admin_handlers(dp: Dispatcher):

    async def admin_cmd(m: types.Message):
        if m.from_user.id not in ADMIN_IDS:
            return
        await m.answer("🛠 Меню администратора:\n"
                       "Команды:\n"
                       "/add ID сумма — выдать GG\n"
                       "/remove ID сумма — снять GG\n"
                       "/setchance ID % — повысить шанс\n"
                       "/setstatus ID статус — выдать статус\n"
                       "/notifyall текст — сообщение всем\n"
                       "/newpromo код сумма — создать промокод\n"
                       "/promologs — посмотреть логи промокодов\n"
                       "/resetbonus ID — сбросить бонус\n")

    async def add_cmd(m: types.Message):
        if m.from_user.id not in ADMIN_IDS:
            return
        try:
            _, uid, amount = m.text.split()
            update_balance(int(uid), int(amount))
            await m.answer(f"✅ Пополнено {amount} GG для пользователя {uid}")
        except Exception:
            await m.answer("❌ Формат: /add ID сумма")

    async def remove_cmd(m: types.Message):
        if m.from_user.id not in ADMIN_IDS:
            return
        try:
            _, uid, amount = m.text.split()
            update_balance(int(uid), -int(amount))
            await m.answer(f"❌ Снято {amount} GG у пользователя {uid}")
        except Exception:
            await m.answer("❌ Формат: /remove ID сумма")

    async def setchance_cmd(m: types.Message):
        if m.from_user.id not in ADMIN_IDS:
            return
        try:
            _, uid, chance = m.text.split()
            set_user_chance(int(uid), int(chance))
            await m.answer(f"⚡ Шанс выигрыша установлен: {chance}% для пользователя {uid}")
        except Exception:
            await m.answer("❌ Формат: /setchance ID %")

    async def setstatus_cmd(m: types.Message):
        if m.from_user.id not in ADMIN_IDS:
            return
        try:
            _, uid, status = m.text.split()
            set_user_status(int(uid), status)
            await m.answer(f"🎖 Статус '{status}' выдан пользователю {uid}")
        except Exception:
            await m.answer("❌ Формат: /setstatus ID статус")

    async def notify_cmd(m: types.Message):
        if m.from_user.id not in ADMIN_IDS:
            return
        try:
            _, text = m.text.split(" ", 1)
            for uid in get_all_user_ids():
                try:
                    await m.bot.send_message(uid, f"📢 Сообщение от администрации:\n{text}")
                except:
                    continue
            await m.answer("✅ Оповещение отправлено всем!")
        except Exception:
            await m.answer("❌ Формат: /notifyall текст")

    async def newpromo_cmd(m: types.Message):
        if m.from_user.id not in ADMIN_IDS:
            return
        try:
            _, code, reward = m.text.split()
            create_promo(code, int(reward))
            await m.answer(f"🎟 Промокод '{code}' на {reward} GG создан!")
        except Exception:
            await m.answer("❌ Формат: /newpromo КОД сумма")

    async def promologs_cmd(m: types.Message):
        if m.from_user.id not in ADMIN_IDS:
            return
        logs = get_promo_logs()
        msg = "📋 Логи промокодов:\n"
        for code, reward, used_by in logs:
            msg += f"{code}: {reward} GG, использовали: {used_by}\n"
        await m.answer(msg)

    async def resetbonus_cmd(m: types.Message):
        if m.from_user.id not in ADMIN_IDS:
            return
        try:
            _, uid = m.text.split()
            reset_bonus_time(int(uid))
            await m.answer(f"⏰ Таймер бонуса сброшен для пользователя {uid}")
        except Exception:
            await m.answer("❌ Формат: /resetbonus ID")

    dp.register_message_handler(admin_cmd, commands=['admin'])
    dp.register_message_handler(add_cmd, commands=['add'])
    dp.register_message_handler(remove_cmd, commands=['remove'])
    dp.register_message_handler(setchance_cmd, commands=['setchance'])
    dp.register_message_handler(setstatus_cmd, commands=['setstatus'])
    dp.register_message_handler(notify_cmd, commands=['notifyall'])
    dp.register_message_handler(newpromo_cmd, commands=['newpromo'])
    dp.register_message_handler(promologs_cmd, commands=['promologs'])
    dp.register_message_handler(resetbonus_cmd, commands=['resetbonus'])