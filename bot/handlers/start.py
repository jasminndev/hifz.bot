from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db.session import AsyncSessionLocal
from db.crud import get_user, create_user, set_daily_goal
from bot.keyboards import goal_keyboard, main_menu_keyboard

router = Router()


class Registration(StatesGroup):
    choosing_goal = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    tg_user = message.from_user

    async with AsyncSessionLocal() as session:
        user = await get_user(session, tg_user.id)

        if user:
            await message.answer(
                f"Assalomu alaykum, <b>{tg_user.full_name}</b>! 🌙\n\n"
                "Xush kelibsiz! Quron yodlash botiga qaytdingiz.",
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
                f"Assalomu alaykum, <b>{tg_user.full_name}</b>! 🌙\n\n"
                "Quron yodlash botiga xush kelibsiz!\n\n"
                "Har kuni nechta oyat yodlamoqchisiz?",
                reply_markup=goal_keyboard(),
            )
            await state.set_state(Registration.choosing_goal)


@router.callback_query(Registration.choosing_goal, F.data.startswith("goal_"))
async def choose_goal(callback: CallbackQuery, state: FSMContext):
    goal = int(callback.data.split("_")[1])

    async with AsyncSessionLocal() as session:
        await set_daily_goal(session, callback.from_user.id, goal)

    await state.clear()
    await callback.message.edit_text(
        f"✅ Ajoyib! Siz kunlik <b>{goal} oyat</b> yodlashni tanladingiz.\n\n"
        "Muvaffaqiyat tilayman! 🤲"
    )
    await callback.message.answer("Asosiy menyu:", reply_markup=main_menu_keyboard())
    await callback.answer()
