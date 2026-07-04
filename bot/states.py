from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    choosing_goal = State()


class BroadcastState(StatesGroup):
    waiting_message = State()


class AddAyahState(StatesGroup):
    waiting_surah = State()
    waiting_ayah_num = State()
    waiting_arabic = State()
    waiting_uzbek = State()
