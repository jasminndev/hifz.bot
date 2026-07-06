from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def goal_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🌱 1 oyat — Boshlang'ich", callback_data="goal_1")
    builder.button(text="🔥 3 oyat — O'rta daraja", callback_data="goal_3")
    builder.button(text="⚡️ 5 oyat — Intensiv", callback_data="goal_5")
    builder.adjust(1)
    return builder.as_markup()


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="📖 Yangi oyat"),
        KeyboardButton(text="🔁 Takrorlash"),
    )
    builder.row(
        KeyboardButton(text="🧪 Test"),
        KeyboardButton(text="📊 Natijalar"),
    )
    return builder.as_markup(resize_keyboard=True)


def ayah_keyboard(progress_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Yod oldim!", callback_data=f"memorized_{progress_id}")
    return builder.as_markup()


def more_ayahs_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📖 Yana o'rganaman", callback_data="learn_more")
    builder.button(text="✅ Bugun yetarli", callback_data="learn_stop")
    builder.adjust(1)
    return builder.as_markup()


def review_keyboard(progress_id: int, ayah_id: int, hide_translation: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if hide_translation:
        builder.button(text="👁 Tarjimani ko'rish", callback_data=f"show_translation_{progress_id}")
    else:
        builder.button(text="✅ Ha, esladim!", callback_data=f"review_correct_{progress_id}_{ayah_id}")
        builder.button(text="❌ Yo'q, unutibman", callback_data=f"review_wrong_{progress_id}_{ayah_id}")
    builder.adjust(1)
    return builder.as_markup()


def quiz_keyboard(correct_id: int, options: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for opt in options:
        label = opt.uzbek_text[:55] + "…" if len(opt.uzbek_text) > 55 else opt.uzbek_text
        builder.button(text=label, callback_data=f"quiz_{correct_id}_{opt.id}")
    builder.adjust(1)
    return builder.as_markup()


def cancel_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="❌ Bekor qilish"))
    return builder.as_markup(resize_keyboard=True)


def admin_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="👥 Foydalanuvchilar"),
        KeyboardButton(text="📊 Umumiy statistika"),
    )
    builder.row(
        KeyboardButton(text="📢 Xabar yuborish"),
        KeyboardButton(text="➕ Oyat qo'shish"),
    )
    builder.row(KeyboardButton(text="🔙 Asosiy menyu"))
    return builder.as_markup(resize_keyboard=True)
