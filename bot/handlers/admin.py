import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.crud import (
    get_all_users, get_total_stats, add_ayah,
)
from db.session import AsyncSessionLocal
from filters.admin import AdminFilter
from keyboards import admin_menu_keyboard, main_menu_keyboard, cancel_keyboard
from states import BroadcastState, AddAyahState

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(AdminFilter())


@router.message(Command("admin"))
async def admin_menu(message: Message):
    await message.answer(
        "👨‍💼 <b>Admin panel</b>\n\nXush kelibsiz!",
        reply_markup=admin_menu_keyboard(),
    )


@router.message(F.text == "📊 Umumiy statistika")
async def total_stats(message: Message):
    async with AsyncSessionLocal() as session:
        s = await get_total_stats(session)

    await message.answer(
        "📊 <b>Umumiy statistika</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{s['total_users']}</b>\n"
        f"✅ Faol foydalanuvchilar: <b>{s['active_users']}</b>\n"
        f"📖 Jami oyatlar (bazada): <b>{s['total_ayahs']}</b>\n"
        f"🧠 Jami yod olingan: <b>{s['total_memorized']}</b>\n"
        f"🔁 Jami takrorlashlar: <b>{s['total_reviews']}</b>\n",
    )


@router.message(F.text == "👥 Foydalanuvchilar")
async def users_list(message: Message):
    async with AsyncSessionLocal() as session:
        users = await get_all_users(session)

    if not users:
        await message.answer("Hali foydalanuvchilar yo'q.")
        return

    text = "👥 <b>Foydalanuvchilar ro'yxati</b>\n\n"
    for i, user in enumerate(users[:20], 1):  # max 20 ta ko'rsatamiz
        status = "✅" if user.is_active else "🚫"
        username = f"@{user.tg_username}" if user.tg_username else "—"
        text += f"{i}. {status} <b>{user.fullname}</b> ({username})\n"
        text += f"   ID: <code>{user.user_id}</code> | Maqsad: {user.daily_goal} oyat\n\n"

    if len(users) > 20:
        text += f"... va yana {len(users) - 20} ta foydalanuvchi"

    await message.answer(text)


@router.message(F.text == "📢 Xabar yuborish")
async def broadcast_start(message: Message, state: FSMContext):
    await message.answer(
        "📢 Barcha foydalanuvchilarga yuboriladigan xabarni yozing:\n\n"
        "(HTML formatida yozish mumkin: <b>bold</b>, <i>italic</i>)",
        reply_markup=cancel_keyboard(),
    )
    await state.set_state(BroadcastState.waiting_message)


@router.message(BroadcastState.waiting_message, F.text == "❌ Bekor qilish")
async def broadcast_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi.", reply_markup=admin_menu_keyboard())


@router.message(BroadcastState.waiting_message)
async def broadcast_send(message: Message, state: FSMContext):
    from bot.loader import bot

    await state.clear()
    text = message.text

    async with AsyncSessionLocal() as session:
        users = await get_all_users(session)

    success, failed = 0, 0
    for user in users:
        if not user.is_active:
            continue
        try:
            await bot.send_message(user.user_id, text)
            success += 1
        except Exception as e:
            logger.warning(f"Broadcast xato (user_id={user.user_id}): {e}")
            failed += 1

    await message.answer(
        f"📢 <b>Xabar yuborildi!</b>\n\n"
        f"✅ Muvaffaqiyatli: <b>{success}</b>\n"
        f"❌ Xato: <b>{failed}</b>",
        reply_markup=admin_menu_keyboard(),
    )


@router.message(F.text == "➕ Oyat qo'shish")
async def add_ayah_start(message: Message, state: FSMContext):
    await message.answer(
        "➕ Yangi oyat qo'shish\n\nSura raqamini kiriting (1-114):",
        reply_markup=cancel_keyboard(),
    )
    await state.set_state(AddAyahState.waiting_surah)


@router.message(AddAyahState.waiting_surah, F.text == "❌ Bekor qilish")
@router.message(AddAyahState.waiting_ayah_num, F.text == "❌ Bekor qilish")
@router.message(AddAyahState.waiting_arabic, F.text == "❌ Bekor qilish")
@router.message(AddAyahState.waiting_uzbek, F.text == "❌ Bekor qilish")
async def add_ayah_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi.", reply_markup=admin_menu_keyboard())


@router.message(AddAyahState.waiting_surah)
async def add_ayah_surah(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (1 <= int(message.text) <= 114):
        await message.answer("❌ Noto'g'ri. 1 dan 114 gacha raqam kiriting:")
        return
    await state.update_data(surah=int(message.text))
    await message.answer("Oyat raqamini kiriting:")
    await state.set_state(AddAyahState.waiting_ayah_num)


@router.message(AddAyahState.waiting_ayah_num)
async def add_ayah_num(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Noto'g'ri. Raqam kiriting:")
        return
    await state.update_data(ayah_num=int(message.text))
    await message.answer("Arabcha matnni kiriting:")
    await state.set_state(AddAyahState.waiting_arabic)


@router.message(AddAyahState.waiting_arabic)
async def add_ayah_arabic(message: Message, state: FSMContext):
    await state.update_data(arabic=message.text)
    await message.answer("O'zbekcha tarjimani kiriting:")
    await state.set_state(AddAyahState.waiting_uzbek)


@router.message(AddAyahState.waiting_uzbek)
async def add_ayah_uzbek(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    async with AsyncSessionLocal() as session:
        try:
            await add_ayah(
                session,
                surah_number=data["surah"],
                ayah_number=data["ayah_num"],
                arabic_text=data["arabic"],
                uzbek_text=message.text,
            )
            await message.answer(
                f"✅ Oyat muvaffaqiyatli qo'shildi!\n\n"
                f"Sura: {data['surah']}, Oyat: {data['ayah_num']}",
                reply_markup=admin_menu_keyboard(),
            )
        except Exception as e:
            await message.answer(
                f"❌ Xato: {e}\n\nEhtimol bu oyat allaqachon mavjud.",
                reply_markup=admin_menu_keyboard(),
            )


@router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main(message: Message):
    await message.answer("Asosiy menyu:", reply_markup=main_menu_keyboard())
