import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from db.crud import (
    get_user, get_next_unassigned_ayah, assign_ayah,
    get_todays_learning, mark_memorized, get_ayah_by_id,
)
from db.session import AsyncSessionLocal
from keyboards import ayah_keyboard, main_menu_keyboard, more_ayahs_keyboard
from utils.safe_parse import parse_callback_int
from utils.texts import (
    AYAH_MESSAGE, MEMORIZED_SUCCESS, DAILY_GOAL_COMPLETED,
    NO_AYAHS_LEFT, get_surah_name,
)

logger = logging.getLogger(__name__)
router = Router()

REVIEW_INTERVALS = [1, 3, 7, 14]


def format_ayah_msg(ayah) -> str:
    return AYAH_MESSAGE.format(
        surah_name=get_surah_name(ayah.surah_number),
        ayah_number=ayah.ayah_number,
        arabic_text=ayah.arabic_text,
        uzbek_text=ayah.uzbek_text,
    )


async def _send_ayah_for_progress(message: Message, progress, ayah):
    await message.answer(
        format_ayah_msg(ayah),
        reply_markup=ayah_keyboard(progress.id),
    )
    if ayah.audio_url:
        try:
            await message.answer_audio(
                ayah.audio_url,
                caption=f"🔊 {get_surah_name(ayah.surah_number)} • {ayah.ayah_number}-oyat",
            )
        except TelegramBadRequest as e:
            logger.warning(f"Audio yuborilmadi (ayah_id={ayah.id}): {e}")


@router.message(F.text == "📖 Yangi oyat")
async def send_daily_ayah(message: Message):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            await message.answer("Avval /start bosing.")
            return

        goal = user.daily_goal or 1
        today_progress = await get_todays_learning(session, user.id)

        if today_progress:
            progress = today_progress[0]
            ayah = await get_ayah_by_id(session, progress.ayah_id)
            await _send_ayah_for_progress(message, progress, ayah)
            return

        first_progress, first_ayah = None, None
        assigned_count = 0

        for i in range(goal):
            next_ayah = await get_next_unassigned_ayah(session, user.id)
            if not next_ayah:
                if i == 0:
                    await message.answer(NO_AYAHS_LEFT, reply_markup=main_menu_keyboard())
                    return
                break
            progress = await assign_ayah(session, user.id, next_ayah.id)
            assigned_count += 1
            if i == 0:
                first_progress, first_ayah = progress, next_ayah

        await _send_ayah_for_progress(message, first_progress, first_ayah)


@router.callback_query(F.data.startswith("memorized_"))
async def on_memorized(callback: CallbackQuery):
    progress_id = parse_callback_int(callback.data, 1)
    if progress_id is None:
        await callback.answer("Noto'g'ri so'rov.", show_alert=True)
        return

    async with AsyncSessionLocal() as session:
        await mark_memorized(session, progress_id)
        user = await get_user(session, callback.from_user.id)

        stage = 0
        from db.crud import get_progress_by_id
        progress = await get_progress_by_id(session, progress_id)
        if progress:
            stage = min(progress.review_stage - 1, len(REVIEW_INTERVALS) - 1)
        days = REVIEW_INTERVALS[stage]

        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(
            MEMORIZED_SUCCESS.format(days=days)
        )

        remaining = await get_todays_learning(session, user.id)

        if remaining:
            next_progress = remaining[0]
            next_ayah = await get_ayah_by_id(session, next_progress.ayah_id)
            await callback.message.answer(
                f"📖 Keyingi oyat ({len(remaining)} qoldi):"
            )
            await _send_ayah_for_progress(callback.message, next_progress, next_ayah)
        else:
            await callback.message.answer(
                DAILY_GOAL_COMPLETED.format(goal=user.daily_goal or 1),
                reply_markup=more_ayahs_keyboard(),
            )

    await callback.answer()


@router.callback_query(F.data == "learn_more")
async def learn_more(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, callback.from_user.id)
        next_ayah = await get_next_unassigned_ayah(session, user.id)

        if not next_ayah:
            await callback.message.edit_text(NO_AYAHS_LEFT)
            await callback.answer()
            return

        progress = await assign_ayah(session, user.id, next_ayah.id)

    await callback.message.edit_reply_markup(reply_markup=None)
    await _send_ayah_for_progress(callback.message, progress, next_ayah)
    await callback.answer()


@router.callback_query(F.data == "learn_stop")
async def learn_stop(callback: CallbackQuery):
    await callback.message.edit_text(
        "✅ <b>Ajoyib!</b> Bugun yaxshi ish qildingiz.\nErtaga davom etamiz! 💪"
    )
    await callback.message.answer("Asosiy menyu 👇", reply_markup=main_menu_keyboard())
    await callback.answer()
