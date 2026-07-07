from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    choosing_goal = State()
    choosing_review_time = State()
