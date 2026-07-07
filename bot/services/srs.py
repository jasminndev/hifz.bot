from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SRSResult:
    next_review_at: datetime
    new_interval: int  # kunlar
    new_easiness: float
    new_stage: int


def calculate_next_review(
        stage: int,
        easiness: float,
        interval: int,
        quality: int,  # 1, 3, yoki 5
) -> SRSResult:
    """
    SM-2 algoritmini hisoblaydi.

    quality:
        5 = Juda oson (Oson tugmasi)
        3 = O'rta (O'rta tugmasi)
        1 = Qiyin/Eslamadim (Qiyin tugmasi)
    """

    # EF yangilash
    new_ef = easiness + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ef = max(1.3, round(new_ef, 2))  # minimal 1.3

    if quality < 3:
        # Eslamagan — boshidan boshlaydi
        new_interval = 1
        new_stage = 0
    else:
        # Eslaganlar uchun interval hisoblash
        if stage == 0:
            new_interval = 1
        elif stage == 1:
            new_interval = 6
        else:
            new_interval = round(interval * new_ef)

        new_stage = stage + 1

    next_review = datetime.utcnow() + timedelta(days=new_interval)

    return SRSResult(
        next_review_at=next_review,
        new_interval=new_interval,
        new_easiness=new_ef,
        new_stage=new_stage,
    )


def quality_to_text(quality: int) -> str:
    if quality == 5:
        return "😊 Oson"
    elif quality == 3:
        return "🤔 O'rta"
    else:
        return "😔 Qiyin"


def interval_to_text(days: int) -> str:
    if days == 1:
        return "ertaga"
    elif days < 7:
        return f"{days} kundan keyin"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} haftadan keyin"
    else:
        months = days // 30
        return f"{months} oydan keyin"
