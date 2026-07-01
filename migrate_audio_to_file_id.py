import asyncio
import logging

from sqlalchemy import select

from bot.loader import bot
from db.models import Ayah
from db.session import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ADMIN_ID = 7556384250


def get_audio_url(surah_number: int, ayah_number: int) -> str:
    return f"https://everyayah.com/data/Alafasy_128kbps/{surah_number:03d}{ayah_number:03d}.mp3"


async def migrate():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Ayah))
        ayahs = list(result.scalars().all())

        logger.info(f"Jami {len(ayahs)} ta oyat topildi.")

        for ayah in ayahs:
            # Agar allaqachon file_id bo'lsa (https bilan boshlanmasa) — o'tkazib yuboramiz
            if ayah.audio_url and not ayah.audio_url.startswith("http"):
                logger.info(f"Surah {ayah.surah_number}:{ayah.ayah_number} — allaqachon file_id bor, o'tkazildi.")
                continue

            url = get_audio_url(ayah.surah_number, ayah.ayah_number)

            try:
                msg = await bot.send_audio(
                    ADMIN_ID,
                    url,
                    caption=f"Surah {ayah.surah_number}:{ayah.ayah_number}",
                )
                file_id = msg.audio.file_id

                ayah.audio_url = file_id
                await session.commit()

                logger.info(f"✅ Surah {ayah.surah_number}:{ayah.ayah_number} — file_id saqlandi.")

                # Adminga yuborilgan xabarni o'chiramiz (faqat file_id kerak)
                await bot.delete_message(ADMIN_ID, msg.message_id)

            except Exception as e:
                logger.warning(f"❌ Surah {ayah.surah_number}:{ayah.ayah_number} — xato: {e}")

            await asyncio.sleep(0.5)  # rate-limit guard

        logger.info("🎉 Migratsiya tugadi!")

    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(migrate())
