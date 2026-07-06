import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from db.crud import (
    get_user, get_due_reviews, get_ayah_by_id,
    get_progress_by_id, mark_memorized,
    reset_progress_stage, save_review_result,
)
from db.models import ReviewResult
from db.session import AsyncSessionLocal
from keyboards import review_keyboard, main_menu_keyboard
from utils.safe_parse import parse_callback_int
from utils.texts import (
    REVIEW_START, REVIEW_QUESTION, REVIEW_SHOW_TRANSLATION,
    REVIEW_CORRECT, REVIEW_WRONG, NO_REVIEWS, get_surah_name,
)

logger = logging.getLogger(__name__)
router = Router()

REVIEW_INTERVALS = [1, 3, 7, 14]


@router.message(F.text == "🔁 Takrorlash")
async def send_reviews(message: Message):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            await message.answer("Avval /start bosing.")
            return

        due = await get_due_reviews(session, user.id)

        if not due:
            await message.answer(NO_REVIEWS, reply_markup=main_menu_keyboard())
            return

        await message.answer(REVIEW_START.format(count=len(due)))

        progress = due[0]
        ayah = await get_ayah_by_id(session, progress.ayah_id)

        await message.answer(
            REVIEW_QUESTION.format(
                surah_name=get_surah_name(ayah.surah_number),
                ayah_number=ayah.ayah_number,
                arabic_text=ayah.arabic_text,
            ),
            reply_markup=review_keyboard(progress.id, ayah.id, hide_translation=True),
        )


@router.callback_query(F.data.startswith("show_translation_"))
async def show_translation(callback: CallbackQuery):
    progress_id = parse_callback_int(callback.data, 2)
    if progress_id is None:
        await callback.answer("Noto'g'ri so'rov.", show_alert=True)
        return

    async with AsyncSessionLocal() as session:
        progress = await get_progress_by_id(session, progress_id)
        if not progress:
            await callback.answer("Oyat topilmadi.", show_alert=True)
            return
        ayah = await get_ayah_by_id(session, progress.ayah_id)

        await callback.message.edit_text(
            REVIEW_SHOW_TRANSLATION.format(
                surah_name=get_surah_name(ayah.surah_number),
                ayah_number=ayah.ayah_number,
                arabic_text=ayah.arabic_text,
                uzbek_text=ayah.uzbek_text,
            ),
            reply_markup=review_keyboard(progress.id, ayah.id, hide_translation=False),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("review_correct_"))
async def review_correct(callback: CallbackQuery):
    parts = callback.data.split("_")
    if len(parts) != 4:
        await callback.answer("Noto'g'ri so'rov.", show_alert=True)
        return
    try:
        progress_id, ayah_id = int(parts[2]), int(parts[3])
    except ValueError:
        await callback.answer("Noto'g'ri so'rov.", show_alert=True)
        return

    async with AsyncSessionLocal() as session:
        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer("Avval /start bosing.", show_alert=True)
            return

        await save_review_result(session, user.id, ayah_id, ReviewResult.correct)
        await mark_memorized(session, progress_id)

        progress = await get_progress_by_id(session, progress_id)
        stage = min((progress.review_stage - 1) if progress else 0, len(REVIEW_INTERVALS) - 1)
        days = REVIEW_INTERVALS[stage]

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        REVIEW_CORRECT.format(days=days),
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("review_wrong_"))
async def review_wrong(callback: CallbackQuery):
    parts = callback.data.split("_")
    if len(parts) != 4:
        await callback.answer("Noto'g'ri so'rov.", show_alert=True)
        return
    try:
        progress_id, ayah_id = int(parts[2]), int(parts[3])
    except ValueError:
        await callback.answer("Noto'g'ri so'rov.", show_alert=True)
        return

    async with AsyncSessionLocal() as session:
        user = await get_user(session, callback.from_user.id)
        if not user:
            await callback.answer("Avval /start bosing.", show_alert=True)
            return

        await save_review_result(session, user.id, ayah_id, ReviewResult.incorrect)
        await reset_progress_stage(session, progress_id)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(REVIEW_WRONG, reply_markup=main_menu_keyboard())
    await callback.answer()
