"""
Butun Qur'onni (114 sura, 6236 oyat) bazaga yuklash.
Manba:
  - Arabcha matn: api.alquran.cloud (ar.alafasy)
  - O'zbekcha tarjima: quranenc.com (uzbek_mansour)
  - Audio: everyayah.com (Alafasy qiroati, URL hozircha)

Ishga tushirish: python seed_full_quran.py
"""

import asyncio
import logging

import aiohttp
from sqlalchemy import select

from db.crud import add_ayah
from db.models import Ayah
from db.session import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ARABIC_URL = "https://api.alquran.cloud/v1/surah/{}/ar.alafasy"
UZBEK_URL = "https://quranenc.com/api/v1/translation/sura/uzbek_mansour/{}"

HEADERS = {"User-Agent": "HifzBot/1.0", "Accept": "application/json"}


def get_audio_url(surah: int, ayah: int) -> str:
    return f"https://everyayah.com/data/Alafasy_128kbps/{surah:03d}{ayah:03d}.mp3"


async def fetch_json(session: aiohttp.ClientSession, url: str):
    async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=20)) as r:
        return await r.json()


async def get_existing_ayah_keys(db_session) -> set[tuple[int, int]]:
    result = await db_session.execute(select(Ayah.surah_number, Ayah.ayah_number))
    return set(result.all())


async def seed_surah(http_session: aiohttp.ClientSession, db_session, surah_num: int, existing: set):
    try:
        arabic_data = await fetch_json(http_session, ARABIC_URL.format(surah_num))
        uzbek_data = await fetch_json(http_session, UZBEK_URL.format(surah_num))
    except Exception as e:
        logger.warning(f"❌ Surah {surah_num}: fetch xato — {e}")
        return 0

    arabic_ayahs = arabic_data.get("data", {}).get("ayahs", [])
    uzbek_list = uzbek_data.get("result", []) if isinstance(uzbek_data, dict) else []
    uzbek_map = {int(item["aya"]): item["translation"] for item in uzbek_list}

    count = 0
    for ayah in arabic_ayahs:
        ayah_num = ayah["numberInSurah"]
        if (surah_num, ayah_num) in existing:
            continue  # qayta yozmaymiz — davom etish mumkin bo'ladi

        arabic_text = ayah["text"]
        uzbek_text = uzbek_map.get(ayah_num, "")
        audio_url = get_audio_url(surah_num, ayah_num)

        await add_ayah(db_session, surah_num, ayah_num, arabic_text, uzbek_text, audio_url)
        count += 1

    return count


async def main():
    async with AsyncSessionLocal() as db_session:
        existing = await get_existing_ayah_keys(db_session)
        logger.info(f"Bazada hozir {len(existing)} ta oyat bor — bular o'tkazib yuboriladi.")

        total_added = 0
        async with aiohttp.ClientSession() as http_session:
            for surah_num in range(1, 115):  # 1 dan 114 gacha
                added = await seed_surah(http_session, db_session, surah_num, existing)
                total_added += added
                logger.info(f"✅ Surah {surah_num}: {added} ta yangi oyat qo'shildi.")
                await asyncio.sleep(0.3)  # serverlarga hurmat — rate limit

        logger.info(f"🎉 Jami {total_added} ta yangi oyat qo'shildi!")


if __name__ == "__main__":
    asyncio.run(main())
