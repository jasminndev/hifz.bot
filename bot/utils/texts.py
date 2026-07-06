SURAH_NAMES = {
    1: "Al-Fotiha", 2: "Al-Baqara", 3: "Ali Imron", 4: "An-Niso",
    5: "Al-Moida", 6: "Al-An'om", 7: "Al-A'rof", 8: "Al-Anfol",
    9: "At-Tavba", 10: "Yunus", 11: "Hud", 12: "Yusuf",
    13: "Ar-Ra'd", 14: "Ibrohim", 15: "Al-Hijr", 16: "An-Nahl",
    17: "Al-Isro", 18: "Al-Kahf", 19: "Maryam", 20: "To-Ho",
    21: "Al-Anbiyo", 22: "Al-Haj", 23: "Al-Mu'minun", 24: "An-Nur",
    25: "Al-Furqon", 26: "Ash-Shuaro", 27: "An-Naml", 28: "Al-Qasas",
    29: "Al-Ankabut", 30: "Ar-Rum", 31: "Luqmon", 32: "As-Sajda",
    33: "Al-Ahzob", 34: "Saba", 35: "Fotir", 36: "Yo-Sin",
    37: "As-Soffot", 38: "Sod", 39: "Az-Zumar", 40: "G'ofir",
    41: "Fussilat", 42: "Ash-Shuro", 43: "Az-Zuxruf", 44: "Ad-Duxon",
    45: "Al-Josiya", 46: "Al-Ahqof", 47: "Muhammad", 48: "Al-Fath",
    49: "Al-Hujurot", 50: "Qof", 51: "Az-Zoriyot", 52: "At-Tur",
    53: "An-Najm", 54: "Al-Qamar", 55: "Ar-Rahman", 56: "Al-Voqia",
    57: "Al-Hadid", 58: "Al-Mujodala", 59: "Al-Hashr", 60: "Al-Mumtahana",
    61: "As-Saff", 62: "Al-Juma", 63: "Al-Munofiqun", 64: "At-Tag'obun",
    65: "At-Taloq", 66: "At-Tahrim", 67: "Al-Mulk", 68: "Al-Qalam",
    69: "Al-Haqqa", 70: "Al-Maarij", 71: "Nuh", 72: "Al-Jin",
    73: "Al-Muzzammil", 74: "Al-Muddassir", 75: "Al-Qiyoma", 76: "Al-Inson",
    77: "Al-Mursalot", 78: "An-Naba", 79: "An-Noziot", 80: "Abasa",
    81: "At-Takwir", 82: "Al-Infitor", 83: "Al-Mutaffifin", 84: "Al-Inshiqoq",
    85: "Al-Buruj", 86: "At-Toriq", 87: "Al-A'lo", 88: "Al-G'oshiya",
    89: "Al-Fajr", 90: "Al-Balad", 91: "Ash-Shams", 92: "Al-Layl",
    93: "Ad-Duho", 94: "Ash-Sharh", 95: "At-Tin", 96: "Al-Alaq",
    97: "Al-Qadr", 98: "Al-Bayyina", 99: "Az-Zalzala", 100: "Al-Odiyot",
    101: "Al-Qoria", 102: "At-Takosur", 103: "Al-Asr", 104: "Al-Humaza",
    105: "Al-Fil", 106: "Quraysh", 107: "Al-Maun", 108: "Al-Kavsar",
    109: "Al-Kofirun", 110: "An-Nasr", 111: "Al-Masad", 112: "Al-Ikhlos",
    113: "Al-Falaq", 114: "An-Nos",
}


def get_surah_name(surah_number: int) -> str:
    return SURAH_NAMES.get(surah_number, f"Surah {surah_number}")



WELCOME_NEW = """
بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ

Assalomu alaykum, <b>{name}</b>! 👋

✨ <b>HifzBot</b> ga xush kelibsiz!

Bu bot sizga Qur'on oyatlarini
ilmiy usulda yodlashda yordam beradi.

━━━━━━━━━━━━━━━━━━━━━
📌 <b>Qanday ishlaydi?</b>
━━━━━━━━━━━━━━━━━━━━━
🌅 Har kuni yangi oyatlar beriladi
🔁 Muntazam takrorlash eslatiladi
🧪 Test orqali bilim tekshiriladi
📈 Progressingiz kuzatiladi
━━━━━━━━━━━━━━━━━━━━━

🎯 <b>Kunlik maqsadingizni tanlang:</b>
"""

WELCOME_BACK = """
بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ

Assalomu alaykum, <b>{name}</b>! 👋

Xush kelibsiz! Davom etamizmi? 💪
"""

GOAL_SET = """
✅ <b>Ajoyib tanlov!</b>

🎯 Kunlik maqsad: <b>{goal} oyat/kun</b>

Har kuni <b>soat 08:00</b> da yangi oyatlar,
<b>18:00</b> da takrorlash eslatmasi yuboriladi.

Alloh yodlashingizni oson qilsin! 🤲
"""

AYAH_MESSAGE = """
━━━━━━━━━━━━━━━━━━━━━
📖 <b>{surah_name}</b> • {ayah_number}-oyat
━━━━━━━━━━━━━━━━━━━━━

<b>{arabic_text}</b>

🌐 <b>Tarjima:</b>
<i>{uzbek_text}</i>

━━━━━━━━━━━━━━━━━━━━━"""

DAILY_AYAH_MORNING = """
🌅 <b>Yangi kun muborak!</b>

Bugungi oyatingiz tayyor.
Bismillah, boshlaylik! 📖
"""

MEMORIZED_SUCCESS = """
✅ <b>Barakalloh!</b>

Oyat yod olindi va takrorlash
jadvaliga qo'shildi 📅

⏰ Keyingi takrorlash: <b>{days} kundan keyin</b>
"""

DAILY_GOAL_COMPLETED = """
🎉 <b>Kunlik maqsad bajarildi!</b>

Bugun <b>{goal} ta</b> oyat yod oldingiz.
Zo'r natija! 💪

Yana o'rganmoqchimisiz?
"""

REVIEW_START = """
🔁 <b>Takrorlash vaqti!</b>

Sizda <b>{count} ta</b> oyat takrorlashni kutmoqda.

Boshlaylikmi? 👇
"""

REVIEW_QUESTION = """
━━━━━━━━━━━━━━━━━━━━━
🔁 <b>{surah_name}</b> • {ayah_number}-oyat
━━━━━━━━━━━━━━━━━━━━━

<b>{arabic_text}</b>

Tarjimani eslay olasizmi? 🤔
━━━━━━━━━━━━━━━━━━━━━"""

REVIEW_SHOW_TRANSLATION = """
━━━━━━━━━━━━━━━━━━━━━
🔁 <b>{surah_name}</b> • {ayah_number}-oyat
━━━━━━━━━━━━━━━━━━━━━

<b>{arabic_text}</b>

🌐 <b>Tarjima:</b>
<i>{uzbek_text}</i>

━━━━━━━━━━━━━━━━━━━━━
To'g'ri yodladingizmi?"""

REVIEW_CORRECT = """
✅ <b>Ajoyib!</b> To'g'ri esladingiz!

Keyingi takrorlash <b>{days} kundan keyin</b> 📅
"""

REVIEW_WRONG = """
😔 <b>Xavotir olmang!</b>

Bu oyatni qaytadan o'rganamiz.
Takrorlash — muvaffaqiyat kaliti! 🔑
"""

NO_REVIEWS = """
✅ <b>Hozircha takrorlanadigan oyat yo'q!</b>

Keyingi takrorlash vaqti kelganda
xabar beriladi 🔔
"""

STATS_MESSAGE = """
━━━━━━━━━━━━━━━━━━━━━
📊 <b>Sizning natijalaringiz</b>
━━━━━━━━━━━━━━━━━━━━━
🎯 Kunlik maqsad:    <b>{goal} oyat</b>
📚 Jami o'rganilgan: <b>{total} oyat</b>
✅ Yod olingan:      <b>{memorized} oyat</b>
🔁 Bugun takrorlandi: <b>{reviews_today}</b>
💯 To'g'ri javoblar: <b>{correct_today}</b>{accuracy}
━━━━━━━━━━━━━━━━━━━━━"""

QUIZ_QUESTION = """
━━━━━━━━━━━━━━━━━━━━━
🧪 <b>Bilim testi</b>
━━━━━━━━━━━━━━━━━━━━━

Quyidagi oyatning tarjimasini toping:

<b>{arabic_text}</b>

👇 To'g'ri javobni tanlang:"""

QUIZ_CORRECT = "✅ <b>To'g'ri!</b> Barakalloh! 🌟"

QUIZ_WRONG = """
❌ <b>Noto'g'ri</b>

To'g'ri javob:
<i>{uzbek_text}</i>
"""

NO_AYAHS_LEFT = """
🎊 <b>Muborak!</b>

Barcha mavjud oyatlarni yodladingiz!
Tez orada yangi oyatlar qo'shiladi 📖
"""
