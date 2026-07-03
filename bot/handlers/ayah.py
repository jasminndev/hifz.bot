import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from db.crud import (
    get_user, get_next_unassigned_ayah, assign_ayah,
    get_todays_learning, mark_memorized, get_ayah_by_id,
)
from db.session import AsyncSessionLocal
from keyboards import ayah_keyboard, main_menu_keyboard

router = Router()

logger = logging.getLogger(__name__)


def format_ayah_msg(ayah) -> str:
    return (
        f"📖 <b>Surah {ayah.surah_number}, Oyat {ayah.ayah_number}</b>\n\n"
        f"<b>Arabcha:</b>\n{ayah.arabic_text}\n\n"
        f"<b>Tarjima:</b>\n{ayah.uzbek_text}"
    )


async def _send_ayah_for_progress(message: Message, progress, ayah):
    await message.answer(
        format_ayah_msg(ayah),
        reply_markup=ayah_keyboard(progress.id),
    )
    if ayah.audio_url:
        try:
            await message.answer_audio(ayah.audio_url, caption="🔊 Tinglang")
        except TelegramBadRequest as e:
            logger.warning(f"Audio yuborilmadi (ayah_id={ayah.id}): {e}")
            await message.answer("⚠️ Audio hozircha mavjud emas.")


@router.message(F.text == "📖 Bugungi oyat")
async def send_daily_ayah(message: Message):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            await message.answer("Avval /start bosing.")
            return

        today_progress = await get_todays_learning(session, user.id)

        if today_progress:
            # Bugun allaqachon tayinlangan, birinchisini ko'rsatamiz
            progress = today_progress[0]
            ayah = await get_ayah_by_id(session, progress.ayah_id)
            await _send_ayah_for_progress(message, progress, ayah)
            return

        # Yangi oyat(lar) tayinlash
        goal = user.daily_goal or 1
        first_progress, first_ayah = None, None

        for i in range(goal):
            next_ayah = await get_next_unassigned_ayah(session, user.id)
            if not next_ayah:
                if i == 0:
                    await message.answer("🎉 Barcha mavjud oyatlarni yodladingiz! Tez orada yangilari qo'shiladi.")
                    return
                break

            progress = await assign_ayah(session, user.id, next_ayah.id)
            if i == 0:
                first_progress, first_ayah = progress, next_ayah

        await _send_ayah_for_progress(message, first_progress, first_ayah)

        if goal > 1:
            await message.answer(
                f"ℹ️ Bugun sizga <b>{goal} ta</b> oyat berildi. "
                "Birini yod olganingizdan so'ng keyingisi ko'rsatiladi."
            )


@router.callback_query(F.data.startswith("memorized_"))
async def on_memorized(callback: CallbackQuery):
    progress_id = int(callback.data.split("_")[1])

    async with AsyncSessionLocal() as session:
        await mark_memorized(session, progress_id)
        user = await get_user(session, callback.from_user.id)

        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(
            "✅ <b>Barakalloh!</b> Oyat yod olindi va takrorlash jadvaliga qo'shildi. 🤲\n\n"
            "1 kundan keyin tekshirish yuboriladi.",
            reply_markup=main_menu_keyboard(),
        )

        # Bugungi qolgan oyatlar bormi?
        remaining = await get_todays_learning(session, user.id)
        if remaining:
            next_progress = remaining[0]
            next_ayah = await get_ayah_by_id(session, next_progress.ayah_id)
            await callback.message.answer(f"Bugungi keyingi oyat ({len(remaining)} qoldi):")
            await _send_ayah_for_progress(callback.message, next_progress, next_ayah)

    await callback.answer()
