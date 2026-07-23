import re

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from sqlalchemy import select

from db.models import Ayah
from db.session import AsyncSessionLocal
from utils.texts import get_surah_name

router = Router()

AYAH_PATTERN = re.compile(r'^(\d{1,3})[:/\s](\d{1,3})$')


@router.message(F.text.regexp(r'^\d{1,3}[:/\s]\d{1,3}$'))
async def search_ayah(message: Message):
    match = AYAH_PATTERN.match(message.text.strip())
    if not match:
        return

    surah_num = int(match.group(1))
    ayah_num = int(match.group(2))

    if not (1 <= surah_num <= 114):
        await message.answer(
            f"❌ <b>{surah_num}-sura mavjud emas!</b>\n\n"
            "Qur'onda 1 dan 114 gacha suralar bor."
        )
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ayah).where(
                Ayah.surah_number == surah_num,
                Ayah.ayah_number == ayah_num,
            )
        )
        ayah = result.scalar_one_or_none()

    if not ayah:
        await message.answer(
            f"❌ <b>{surah_num}-sura, {ayah_num}-oyat topilmadi!</b>\n\n"
            f"📌 {get_surah_name(surah_num)} surasi bazada mavjud emas yoki\n"
            f"bu oyat raqami noto'g'ri.\n\n"
            "💡 <i>Masalan: 1:1, 112:4, 114:6</i>"
        )
        return

    text = (
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔍 <b>{get_surah_name(surah_num)}</b> • {ayah_num}-oyat\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<b>{ayah.arabic_text}</b>\n\n"
        f"🌐 <b>Tarjima:</b>\n"
        f"<i>{ayah.uzbek_text}</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )

    await message.answer(text)

    if ayah.audio_url:
        try:
            await message.answer_audio(
                ayah.audio_url,
                caption=f"🔊 {get_surah_name(surah_num)} • {ayah_num}-oyat",
            )
        except TelegramBadRequest:
            pass
