import asyncio

from db.session import AsyncSessionLocal
from db.crud import add_ayah, get_ayah_count

# (surah_number, ayah_number, arabic_text, uzbek_text, audio_url)
AYAHS = [
    (1, 1, 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ', "Mehribon va Rahmli Allohning nomi bilan", None),
    (1, 2, 'الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ', "Barcha hamdlar olamlar Rabbisi Allohga xosdir", None),
    (1, 3, 'الرَّحْمَٰنِ الرَّحِيمِ', "U Mehribon, U Rahmlidir", None),
    (1, 4, 'مَالِكِ يَوْمِ الدِّينِ', "Hisob-kitob Kunining Egasidir", None),
    (1, 5, 'إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ', "Faqat Senga ibodat qilamiz va faqat Sendan madad so'raymiz",
     None),
    (1, 6, 'اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ', "Bizni To'g'ri yo'lga hidoyat qil", None),
    (1, 7, 'صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ',
     "O'zingga ne'mat bergan zotlarning yo'liga, g'azabga uchragan va adashganlarning yo'liga emas", None),

    (112, 1, 'قُلْ هُوَ اللَّهُ أَحَدٌ', "Ayt: U – Alloh Birdir", None),
    (112, 2, 'اللَّهُ الصَّمَدُ', "Alloh Samaddir", None),
    (112, 3, 'لَمْ يَلِدْ وَلَمْ يُولَدْ', "U tug'magan va tug'ilmagan", None),
    (112, 4, 'وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ', "Va Unga teng keladigan hech kim yo'q", None),

    (114, 1, 'قُلْ أَعُوذُ بِرَبِّ النَّاسِ', "Ayt: Odamlarning Rabbiga panoh tilayman", None),
    (114, 2, 'مَلِكِ النَّاسِ', "Odamlarning Podshohiga", None),
    (114, 3, 'إِلَٰهِ النَّاسِ', "Odamlarning Ma'budiga", None),
    (114, 4, 'مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ', "Vasvasa soladigan gijgijchining yomonligidan", None),
    (114, 5, 'الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ', "Odamlarning ko'ksiga vasvasa soladiganining", None),
    (114, 6, 'مِنَ الْجِنَّةِ وَالنَّاسِ', "Jinlardan va odamlardan", None),
]


async def seed():
    async with AsyncSessionLocal() as session:
        existing = await get_ayah_count(session)
        if existing > 0:
            print(f"⚠️  Bazada allaqachon {existing} ta oyat bor. Seed bekor qilindi.")
            return

        for surah, ayah, arabic, uzbek, audio in AYAHS:
            await add_ayah(session, surah, ayah, arabic, uzbek, audio)

        print(f"✅ {len(AYAHS)} ta oyat muvaffaqiyatli qo'shildi!")


if __name__ == "__main__":
    asyncio.run(seed())
