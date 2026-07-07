import logging
import random

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from db.crud import get_user, get_memorized_ayahs, get_ayah_by_id
from db.session import AsyncSessionLocal
from keyboards import (
    quiz_type_keyboard, quiz_keyboard,
    exam_keyboard, main_menu_keyboard,
)
from utils.texts import (
    QUIZ_QUESTION, QUIZ_CORRECT, QUIZ_TYPE_SELECT, EXAM_QUESTION, EXAM_RESULT,
    get_grade, )

logger = logging.getLogger(__name__)
router = Router()


class ExamState(StatesGroup):
    in_progress = State()


def _build_quiz_options(memorized: list, correct) -> list:
    others = [a for a in memorized if a.id != correct.id]
    wrong_choices = random.sample(others, min(3, len(others)))
    options = wrong_choices + [correct]
    random.shuffle(options)
    return options


# ---------- Test turi tanlash ----------

@router.message(F.text == "🧪 Test")
async def send_quiz_menu(message: Message):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            await message.answer("Avval /start bosing.")
            return

        memorized = await get_memorized_ayahs(session, user.id)

        if len(memorized) < 2:
            await message.answer(
                "Test uchun kamida <b>2 ta</b> yod olingan oyat kerak.\n"
                "Avval oyatlarni o'rganing! 📖",
                reply_markup=main_menu_keyboard(),
            )
            return

    await message.answer(QUIZ_TYPE_SELECT, reply_markup=quiz_type_keyboard())


# ---------- Oddiy test (1 ta savol) ----------

@router.callback_query(F.data == "quiz_type_single")
async def start_single_quiz(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, callback.from_user.id)
        memorized = await get_memorized_ayahs(session, user.id)

    correct = random.choice(memorized)
    options = _build_quiz_options(memorized, correct)

    await callback.message.edit_text(
        QUIZ_QUESTION.format(arabic_text=correct.arabic_text),
        reply_markup=quiz_keyboard(correct.id, options),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("quiz_") & ~F.data.startswith("quiz_type_"))
async def check_single_quiz(callback: CallbackQuery):
    parts = callback.data.split("_")
    correct_id, chosen_id = int(parts[1]), int(parts[2])

    async with AsyncSessionLocal() as session:
        if correct_id == chosen_id:
            await callback.message.edit_text(QUIZ_CORRECT)
        else:
            correct_ayah = await get_ayah_by_id(session, correct_id)
            await callback.message.edit_text(
                f"❌ <b>Noto'g'ri.</b>\n\n"
                f"✅ <b>To'g'ri javob:</b>\n\n"
                f"<b>{correct_ayah.arabic_text}</b>\n\n"
                f"🌐 <i>{correct_ayah.uzbek_text}</i>"
            )

    await callback.message.answer("Davom etish:", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "quiz_type_exam")
async def start_exam(callback: CallbackQuery, state: FSMContext):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, callback.from_user.id)
        memorized = await get_memorized_ayahs(session, user.id)

    total = min(10, len(memorized))
    questions = random.sample(memorized, total)
    first = questions[0]
    options = _build_quiz_options(memorized, first)

    await state.set_state(ExamState.in_progress)
    await state.update_data(
        questions=[q.id for q in questions],
        current=0,
        correct=0,
        wrong=0,
        total=total,
        options={"1": [o.id for o in options]},  # ← options saqlaymiz
    )

    await callback.message.edit_text(
        EXAM_QUESTION.format(
            current=1,
            total=total,
            arabic_text=first.arabic_text,
        ),
        reply_markup=exam_keyboard(
            correct_id=first.id,
            options=options,
            question_num=1,
            total=total,
        ),
    )
    await callback.answer()


@router.callback_query(ExamState.in_progress, F.data.startswith("exam_"))
async def handle_exam_answer(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    correct_id = int(parts[1])
    chosen_id = int(parts[2])
    question_num = int(parts[3])
    total = int(parts[4])

    data = await state.get_data()
    is_correct = correct_id == chosen_id

    new_correct = data["correct"] + (1 if is_correct else 0)
    new_wrong = data["wrong"] + (0 if is_correct else 1)
    current = data["current"] + 1

    await state.update_data(correct=new_correct, wrong=new_wrong, current=current)

    # Tugmalarni darhol o'chiramiz — ikki marta bosilmasin
    await callback.message.edit_reply_markup(reply_markup=None)

    # Natija xabari
    if is_correct:
        result_text = f"✅ <b>To'g'ri!</b> ({question_num}/{total})"
    else:
        async with AsyncSessionLocal() as session:
            correct_ayah = await get_ayah_by_id(session, correct_id)
        result_text = (
            f"❌ <b>Noto'g'ri!</b> ({question_num}/{total})\n\n"
            f"✅ To'g'ri javob:\n"
            f"<b>{correct_ayah.arabic_text}</b>\n"
            f"<i>{correct_ayah.uzbek_text}</i>"
        )

    await callback.message.answer(result_text)
    await callback.answer()

    # Oxirgi savol bo'lsa — natijani ko'rsatamiz
    if current >= total:
        await state.clear()
        percent = round(new_correct / total * 100)
        await callback.message.answer(
            EXAM_RESULT.format(
                correct=new_correct,
                total=total,
                wrong=new_wrong,
                percent=percent,
                grade=get_grade(percent),
            ),
            reply_markup=main_menu_keyboard(),
        )
        return

    # Keyingi savolni yuboramiz
    async with AsyncSessionLocal() as session:
        user = await get_user(session, callback.from_user.id)
        memorized = await get_memorized_ayahs(session, user.id)

    next_ayah_id = data["questions"][current]
    memorized_map = {a.id: a for a in memorized}
    next_ayah = memorized_map.get(next_ayah_id)

    if not next_ayah:
        await state.clear()
        await callback.message.answer("Xatolik yuz berdi.", reply_markup=main_menu_keyboard())
        return

    next_options = _build_quiz_options(memorized, next_ayah)

    # Options ni state ga saqlaymiz
    all_options = data.get("options", {})
    all_options[str(current + 1)] = [o.id for o in next_options]
    await state.update_data(options=all_options)

    await callback.message.answer(
        EXAM_QUESTION.format(
            current=current + 1,
            total=total,
            arabic_text=next_ayah.arabic_text,
        ),
        reply_markup=exam_keyboard(
            correct_id=next_ayah.id,
            options=next_options,
            question_num=current + 1,
            total=total,
        ),
    )
