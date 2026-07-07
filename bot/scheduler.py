import asyncio
import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from db.crud import (
    get_all_active_users, get_next_unassigned_ayah, assign_ayah,
    get_due_reviews,
)
from db.models import User
from db.session import AsyncSessionLocal
from keyboards import ayah_keyboard, main_menu_keyboard

logger = logging.getLogger(__name__)


async def send_daily_ayahs(bot: Bot):
    async with AsyncSessionLocal() as session:
        users = await get_all_active_users(session)

        for user in users:
            goal = user.daily_goal or 1
            try:
                first_progress, first_ayah = None, None

                for i in range(goal):
                    next_ayah = await get_next_unassigned_ayah(session, user.id)
                    if not next_ayah:
                        break
                    progress = await assign_ayah(session, user.id, next_ayah.id)
                    if i == 0:
                        first_progress, first_ayah = progress, next_ayah

                if first_ayah:
                    text = (
                        f"🌅 <b>Yangi kun, yangi oyat!</b>\n\n"
                        f"📖 <b>Surah {first_ayah.surah_number}, Oyat {first_ayah.ayah_number}</b>\n\n"
                        f"{first_ayah.arabic_text}\n\n"
                        f"<b>Tarjima:</b>\n{first_ayah.uzbek_text}"
                    )
                    await bot.send_message(
                        user.user_id, text,
                        reply_markup=ayah_keyboard(first_progress.id),
                    )
                    if first_ayah.audio_url:
                        await bot.send_audio(user.user_id, first_ayah.audio_url, caption="🔊 Tinglang")

            except Exception as e:
                logger.warning(f"Could not send to {user.user_id}: {e}")

            await asyncio.sleep(0.05)


async def send_review_reminders(bot: Bot):
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(
                User.is_active == True,
                User.review_time == current_time,
            )
        )
        users = list(result.scalars().all())

        for user in users:
            try:
                due = await get_due_reviews(session, user.id)
                if due:
                    await bot.send_message(
                        user.user_id,
                        f"🔔 <b>Takrorlash vaqti!</b>\n\n"
                        f"Sizda <b>{len(due)} ta</b> oyat kutmoqda.\n"
                        f"Hozir takrorlaymizmi? 📖",
                        reply_markup=main_menu_keyboard(),
                    )
            except Exception as e:
                logger.warning(f"Reminder xato (user_id={user.user_id}): {e}")
            await asyncio.sleep(0.05)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")

    scheduler.add_job(
        send_daily_ayahs, "cron",
        hour=8, minute=0,
        args=[bot],
        id="daily_ayahs",
    )

    scheduler.add_job(
        send_review_reminders, "cron",
        minute="*",
        args=[bot],
        id="review_reminders",
    )

    return scheduler
