from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.crud import get_user, create_user, set_daily_goal, set_review_time
from db.session import AsyncSessionLocal
from keyboards import goal_keyboard, main_menu_keyboard, review_time_keyboard
from states import Registration
from utils.texts import SETTINGS_MENU
from utils.texts import WELCOME_NEW, WELCOME_BACK, GOAL_SET, REVIEW_TIME_SELECT, REVIEW_TIME_SET

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    tg_user = message.from_user

    async with AsyncSessionLocal() as session:
        user = await get_user(session, tg_user.id)

        if user:
            await message.answer(
                WELCOME_BACK.format(name=tg_user.full_name),
                reply_markup=main_menu_keyboard(),
            )
        else:
            await create_user(
                session,
                user_id=tg_user.id,
                tg_username=tg_user.username,
                fullname=tg_user.full_name,
            )
            await message.answer(
                WELCOME_NEW.format(name=tg_user.full_name),
                reply_markup=goal_keyboard(),
            )
            await state.set_state(Registration.choosing_goal)


@router.callback_query(Registration.choosing_goal, F.data.startswith("goal_"))
async def choose_goal(callback: CallbackQuery, state: FSMContext):
    goal = int(callback.data.split("_")[1])

    async with AsyncSessionLocal() as session:
        await set_daily_goal(session, callback.from_user.id, goal)

    await callback.message.edit_text(
        GOAL_SET.format(goal=goal)
    )
    await callback.message.answer(
        REVIEW_TIME_SELECT,
        reply_markup=review_time_keyboard(),
    )
    await state.set_state(Registration.choosing_review_time)
    await callback.answer()


@router.callback_query(Registration.choosing_review_time, F.data.startswith("review_time_"))
async def choose_review_time(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split("review_time_")[1]

    async with AsyncSessionLocal() as session:
        await set_review_time(session, callback.from_user.id, time)

    await state.clear()
    await callback.message.edit_text(
        REVIEW_TIME_SET.format(time=time)
    )
    await callback.message.answer("Asosiy menyu 👇", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.message(Command("settings"))
async def settings_menu(message: Message):
    async with AsyncSessionLocal() as session:
        user = await get_user(session, message.from_user.id)
        if not user:
            await message.answer("Avval /start bosing.")
            return

    await message.answer(
        SETTINGS_MENU.format(
            goal=user.daily_goal,
            review_time=user.review_time or "18:00",
        )
    )
    await message.answer(
        "⏰ Takrorlash vaqtini o'zgartirish:",
        reply_markup=review_time_keyboard(),
    )


@router.callback_query(F.data.startswith("review_time_"))
async def update_review_time(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Registration.choosing_review_time:
        return

    time = callback.data.split("review_time_")[1]
    async with AsyncSessionLocal() as session:
        await set_review_time(session, callback.from_user.id, time)

    await callback.message.edit_text(
        REVIEW_TIME_SET.format(time=time)
    )
    await callback.message.answer("Asosiy menyu 👇", reply_markup=main_menu_keyboard())
    await callback.answer()
