from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from db.models import Ayah


def goal_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for goal in [1, 3, 5]:
        builder.button(text=f"{goal} oyat/kun", callback_data=f"goal_{goal}")
    builder.adjust(3)
    return builder.as_markup()


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="📖 Bugungi oyat"),
        KeyboardButton(text="🔁 Takrorlash"),
    )
    builder.row(
        KeyboardButton(text="🧪 Test"),
        KeyboardButton(text="📊 Statistika"),
    )
    return builder.as_markup(resize_keyboard=True)


def ayah_keyboard(progress_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Yod oldim", callback_data=f"memorized_{progress_id}")
    return builder.as_markup()


def review_keyboard(progress_id: int, ayah_id: int, hide_translation: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if hide_translation:
        builder.button(text="👁 Tarjimani ko'rsatish", callback_data=f"show_translation_{progress_id}")
    else:
        builder.button(text="✅ Ha, to'g'ri!", callback_data=f"review_correct_{progress_id}_{ayah_id}")
        builder.button(text="❌ Yo'q, unutdim", callback_data=f"review_wrong_{progress_id}_{ayah_id}")
    builder.adjust(1)
    return builder.as_markup()


def quiz_keyboard(correct_id: int, options: list[Ayah]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for opt in options:
        label = opt.uzbek_text[:50] + "…" if len(opt.uzbek_text) > 50 else opt.uzbek_text
        builder.button(text=label, callback_data=f"quiz_{correct_id}_{opt.id}")
    builder.adjust(1)
    return builder.as_markup()
