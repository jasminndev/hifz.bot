# Quron Yodlash Boti 🌙

Telegram bot foydalanuvchilarga Quron oyatlarini bosqichma-bosqich yodlash va takrorlash imkonini beradi.

## Texnologiyalar

- **Python 3.10+**
- **Aiogram 3.x** — Telegram Bot framework
- **SQLite** — Ma'lumotlar bazasi
- **APScheduler** — Kunlik xabarlar uchun
- **aiohttp** — Quran API dan ma'lumot olish uchun

## O'rnatish

### 1. Bot token olish

[@BotFather](https://t.me/BotFather) ga borib `/newbot` buyrug'ini yuboring va token oling.

### 2. Repo clone qilish

```bash
git clone <repo_url>
cd quron_bot
```

### 3. Virtual muhit yaratish

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 4. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 5. Token sozlash

```bash
cp .env .env
# .env faylini oching va BOT_TOKEN ni to'ldiring
```

### 6. Oyat ma'lumotlarini yuklash (bir marta)

```bash
python seed_ayahs.py
```

Bu buyruq AlQuran Cloud API dan quyidagi suralarni yuklab oladi:
- Al-Fatiha (1:1–7)
- Al-Baqarah (2:1–20)
- Ali 'Imran (3:1–20)
- Al-Ikhlas (112:1–4)
- Al-Falaq (113:1–5)
- An-Nas (114:1–6)

### 7. Botni ishga tushirish

```bash
export BOT_TOKEN=your_token_here   # Linux/Mac
set BOT_TOKEN=your_token_here       # Windows

python bot1.py
```

## Foydalanuvchi buyruqlari

| Buyruq / Tugma | Tavsif |
|---|---|
| `/start` | Botni boshlash va ro'yxatdan o'tish |
| `/menu` | Asosiy menyuni ko'rsatish |
| `/stats` | Statistikani ko'rsatish |
| 📖 Bugungi oyat | Yangi oyat olish |
| 🔁 Takrorlash | Takrorlash vaqti kelgan oyatlar |
| 🧪 Test | Bilimni sinash |
| 📊 Statistika | Natijalarni ko'rish |

## Yodlash metodikasi (Spaced Repetition)

Oyat yod olindikdan keyin quyidagi intervallarda takrorlanadi:

1. **1 kun** — birinchi takrorlash
2. **3 kun** — ikkinchi takrorlash  
3. **7 kun** — uchinchi takrorlash
4. **14 kun** — to'rtinchi takrorlash

Agar takrorlash muvaffaqiyatli bo'lsa — keyingi bosqichga o'tadi.  
Agar unutilgan bo'lsa — boshidan boshlanadi.

## Scheduler (Avtomatik xabarlar)

- **08:00 (Toshkent vaqti)** — Yangi oyatlar yuboriladi
- **18:00 (Toshkent vaqti)** — Takrorlash eslatmasi yuboriladi

## Ma'lumotlar bazasi tuzilishi

```
users                   — Foydalanuvchilar
ayahs                   — Oyatlar (arab matni, tarjima, audio)
memorization_progress   — Har bir user/oyat holati
reviews                 — Takrorlash natijalari
```

## Ko'proq oyat qo'shish

`seed_ayahs.py` faylida `SURAHS` listini tahrirlang:

```python
SURAHS = [
    (1, 7),    # Al-Fatiha
    (2, 286),  # Al-Baqarah — barchasi
    (36, 83),  # Ya-Sin — barchasi
    ...
]
```

## Hosting

Botni serverda ishlatish uchun:

```bash
# systemd service yoki
nohup python bot1.py > bot.log 2>&1 &

# yoki Docker
docker build -t quron-bot .
docker run -e BOT_TOKEN=xxx quron-bot
```
