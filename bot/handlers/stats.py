from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from db.crud import get_user, get_stats
from db.session import AsyncSessionLocal
from bot.keyboards import main_menu_keyboard

router = Router()


@router.message(F.text == "📊 Statistika")
@router.message(Command("stats"))
async def show_stats(message: Message):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            await message.answer("Avval /start bosing.")
            return

        s = await get_stats(session, user.id)
        goal = user.daily_goal or 1

        text = (
            "📊 <b>Sizning natijalaringiz</b>\n\n"
            f"🎯 Kunlik maqsad: <b>{goal} oyat</b>\n"
            f"📚 Jami tayinlangan: <b>{s['total_assigned']} oyat</b>\n"
            f"✅ Yod olingan: <b>{s['memorized']} oyat</b>\n"
            f"🔁 Bugun takrorlangan: <b>{s['reviews_today']}</b>\n"
            f"💯 To'g'ri javoblar (bugun): <b>{s['correct_today']}</b>\n"
        )

        if s["reviews_today"] > 0:
            pct = round(s["correct_today"] / s["reviews_today"] * 100)
            text += f"📈 Aniqlik: <b>{pct}%</b>\n"

        await message.answer(text, reply_markup=main_menu_keyboard())
