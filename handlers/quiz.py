import random

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from db.crud import get_user, get_memorized_ayahs, get_ayah_by_id
from db.session import AsyncSessionLocal
from keyboards import quiz_keyboard, main_menu_keyboard

router = Router()


@router.message(F.text == "🧪 Test")
async def send_quiz(message: Message):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            await message.answer("Avval /start bosing.")
            return

        memorized = await get_memorized_ayahs(session, user.id)

        if len(memorized) < 2:
            await message.answer(
                "Test uchun kamida 2 ta yod olingan oyat kerak.\nAvval oyatlarni o'rganing! 📖",
                reply_markup=main_menu_keyboard(),
            )
            return

        correct = random.choice(memorized)
        others = [a for a in memorized if a.id != correct.id]
        wrong_choices = random.sample(others, min(3, len(others)))

        options = wrong_choices + [correct]
        random.shuffle(options)

        await message.answer(
            f"🧪 <b>Test</b>\n\n"
            f"Quyidagi oyatning tarjimasini toping:\n\n"
            f"<b>{correct.arabic_text}</b>",
            reply_markup=quiz_keyboard(correct.id, options),
        )


@router.callback_query(F.data.startswith("quiz_"))
async def check_quiz(callback: CallbackQuery):
    _, correct_id, chosen_id = callback.data.split("_")
    correct_id, chosen_id = int(correct_id), int(chosen_id)

    async with AsyncSessionLocal() as session:
        if correct_id == chosen_id:
            await callback.message.edit_text("✅ <b>To'g'ri!</b> Barakalloh! 🌟")
        else:
            correct_ayah = await get_ayah_by_id(session, correct_id)
            await callback.message.edit_text(
                f"❌ <b>Noto'g'ri.</b>\n\nTo'g'ri javob:\n{correct_ayah.uzbek_text}"
            )

    await callback.message.answer("Davom etish:", reply_markup=main_menu_keyboard())
    await callback.answer()
