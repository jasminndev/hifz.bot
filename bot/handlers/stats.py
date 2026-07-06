from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from db.crud import get_user, get_stats
from db.session import AsyncSessionLocal
from keyboards import main_menu_keyboard
from utils.texts import STATS_MESSAGE

router = Router()


@router.message(F.text == "📊 Natijalar")
@router.message(Command("stats"))
async def show_stats(message: Message):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            await message.answer("Avval /start bosing.")
            return

        s = await get_stats(session, user.id)
        goal = user.daily_goal or 1

        accuracy = ""
        if s["reviews_today"] > 0:
            pct = round(s["correct_today"] / s["reviews_today"] * 100)
            accuracy = f"\n📈 Aniqlik:           <b>{pct}%</b>"

        await message.answer(
            STATS_MESSAGE.format(
                goal=goal,
                total=s["total_assigned"],
                memorized=s["memorized"],
                reviews_today=s["reviews_today"],
                correct_today=s["correct_today"],
                accuracy=accuracy,
            ),
            reply_markup=main_menu_keyboard(),
        )
