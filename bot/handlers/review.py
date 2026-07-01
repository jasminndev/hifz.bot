from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from db.crud import (
    get_user, get_due_reviews, get_ayah_by_id, get_progress_by_id,
    mark_memorized, reset_progress_stage, save_review_result,
)
from db.models import ReviewResult
from db.session import AsyncSessionLocal
from bot.keyboards import review_keyboard, main_menu_keyboard

router = Router()


@router.message(F.text == "🔁 Takrorlash")
async def send_reviews(message: Message):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            await message.answer("Avval /start bosing.")
            return

        due = await get_due_reviews(session, user.id)

        if not due:
            await message.answer(
                "✅ Hozircha takrorlanadigan oyat yo'q.\nKeyingi takrorlash vaqti kelganda xabar beriladi.",
                reply_markup=main_menu_keyboard(),
            )
            return

        await message.answer(
            f"🔁 <b>Takrorlash vaqti keldi!</b>\n{len(due)} ta oyat kutmoqda."
        )

        progress = due[0]
        ayah = await get_ayah_by_id(session, progress.ayah_id)

        await message.answer(
            f"📖 <b>Surah {ayah.surah_number}, Oyat {ayah.ayah_number}</b>\n\n"
            f"{ayah.arabic_text}\n\n"
            "Tarjimani yodlaysizmi?",
            reply_markup=review_keyboard(progress.id, ayah.id, hide_translation=True),
        )


@router.callback_query(F.data.startswith("show_translation_"))
async def show_translation(callback: CallbackQuery):
    progress_id = int(callback.data.split("_")[2])

    async with AsyncSessionLocal() as session:
        progress = await get_progress_by_id(session, progress_id)
        ayah = await get_ayah_by_id(session, progress.ayah_id)

        await callback.message.edit_text(
            f"📖 <b>Surah {ayah.surah_number}, Oyat {ayah.ayah_number}</b>\n\n"
            f"{ayah.arabic_text}\n\n"
            f"<b>Tarjima:</b>\n{ayah.uzbek_text}\n\n"
            "To'g'ri yodladingizmi?",
            reply_markup=review_keyboard(progress.id, ayah.id, hide_translation=False),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("review_correct_"))
async def review_correct(callback: CallbackQuery):
    _, _, progress_id, ayah_id = callback.data.split("_")
    progress_id, ayah_id = int(progress_id), int(ayah_id)

    async with AsyncSessionLocal() as session:
        user = await get_user(session, callback.from_user.id)
        await save_review_result(session, user.id, ayah_id, ReviewResult.correct)
        await mark_memorized(session, progress_id)  # bosqichni oshiradi

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("✅ Ajoyib! Davom eting. 💪", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("review_wrong_"))
async def review_wrong(callback: CallbackQuery):
    _, _, progress_id, ayah_id = callback.data.split("_")
    progress_id, ayah_id = int(progress_id), int(ayah_id)

    async with AsyncSessionLocal() as session:
        user = await get_user(session, callback.from_user.id)
        await save_review_result(session, user.id, ayah_id, ReviewResult.incorrect)
        await reset_progress_stage(session, progress_id)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "😔 Xavotir olmang! Bu oyatni qaytadan o'rganamiz. 📖",
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()
