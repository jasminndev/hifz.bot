from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Ayah, User, MemorizationProgress, ProgressStatus, Review, ReviewResult


# ---------- Ayah ----------

async def add_ayah(
        session: AsyncSession,
        surah_number: int,
        ayah_number: int,
        arabic_text: str,
        uzbek_text: str,
        audio_url: str | None = None,
) -> Ayah:
    ayah = Ayah(
        surah_number=surah_number,
        ayah_number=ayah_number,
        arabic_text=arabic_text,
        uzbek_text=uzbek_text,
        audio_url=audio_url,
    )
    session.add(ayah)
    await session.commit()
    await session.refresh(ayah)
    return ayah


async def get_ayah_count(session: AsyncSession) -> int:
    result = await session.execute(select(Ayah))
    return len(result.scalars().all())


async def get_ayah_by_id(session: AsyncSession, ayah_id: int) -> Ayah | None:
    result = await session.execute(select(Ayah).where(Ayah.id == ayah_id))
    return result.scalar_one_or_none()


# ---------- User ----------

async def get_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def create_user(
        session: AsyncSession,
        user_id: int,
        tg_username: str | None,
        fullname: str,
) -> User:
    user = User(
        user_id=user_id,
        tg_username=tg_username,
        fullname=fullname,
        daily_goal=1,
        is_active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def set_daily_goal(session: AsyncSession, user_id: int, goal: int) -> None:
    user = await get_user(session, user_id)
    if user:
        user.daily_goal = goal
        await session.commit()


# ---------- MemorizationProgress ----------

async def get_next_unassigned_ayah(session: AsyncSession, db_user_id: int) -> Ayah | None:
    """Foydalanuvchiga hali tayinlanmagan birinchi oyatni qaytaradi."""
    assigned_subquery = select(MemorizationProgress.ayah_id).where(
        MemorizationProgress.user_id == db_user_id
    )
    result = await session.execute(
        select(Ayah)
        .where(Ayah.id.not_in(assigned_subquery))
        .order_by(Ayah.surah_number, Ayah.ayah_number)
        .limit(1)
    )
    return result.scalar_one_or_none()


async def assign_ayah(session: AsyncSession, db_user_id: int, ayah_id: int) -> MemorizationProgress:
    progress = MemorizationProgress(
        user_id=db_user_id,
        ayah_id=ayah_id,
        status=ProgressStatus.learning,
    )
    session.add(progress)
    await session.commit()
    await session.refresh(progress)
    return progress


async def get_todays_learning(session: AsyncSession, db_user_id: int) -> list[MemorizationProgress]:
    """Bugun tayinlangan va hali 'learning' holatidagi yozuvlar."""
    from datetime import datetime, time as dtime

    today_start = datetime.combine(datetime.now().date(), dtime.min)

    result = await session.execute(
        select(MemorizationProgress)
        .where(
            MemorizationProgress.user_id == db_user_id,
            MemorizationProgress.status == ProgressStatus.learning,
            MemorizationProgress.assigned_at >= today_start,
        )
        .order_by(MemorizationProgress.assigned_at)
    )
    return list(result.scalars().all())


async def mark_memorized(session: AsyncSession, progress_id: int) -> None:
    from datetime import datetime, timedelta

    INTERVALS = [1, 3, 7, 14]

    result = await session.execute(
        select(MemorizationProgress).where(MemorizationProgress.id == progress_id)
    )
    progress = result.scalar_one_or_none()
    if not progress:
        return

    stage = progress.review_stage
    days = INTERVALS[min(stage, len(INTERVALS) - 1)]

    progress.status = ProgressStatus.memorized
    progress.memorized_at = datetime.now()
    progress.next_review_at = datetime.now() + timedelta(days=days)
    progress.review_stage = stage + 1

    await session.commit()


async def get_due_reviews(session: AsyncSession, db_user_id: int) -> list[MemorizationProgress]:
    from datetime import datetime

    result = await session.execute(
        select(MemorizationProgress)
        .where(
            MemorizationProgress.user_id == db_user_id,
            MemorizationProgress.status == ProgressStatus.memorized,
            MemorizationProgress.next_review_at <= datetime.now(),
        )
        .order_by(MemorizationProgress.next_review_at)
    )
    return list(result.scalars().all())


async def get_progress_by_id(session: AsyncSession, progress_id: int) -> MemorizationProgress | None:
    result = await session.execute(
        select(MemorizationProgress).where(MemorizationProgress.id == progress_id)
    )
    return result.scalar_one_or_none()


async def reset_progress_stage(session: AsyncSession, progress_id: int) -> None:
    progress = await get_progress_by_id(session, progress_id)
    if progress:
        progress.review_stage = 0
        progress.status = ProgressStatus.learning
        progress.next_review_at = None
        await session.commit()


async def save_review_result(
        session: AsyncSession, db_user_id: int, ayah_id: int, result: "ReviewResult"
) -> None:
    review = Review(user_id=db_user_id, ayah_id=ayah_id, result=result)
    session.add(review)
    await session.commit()


async def get_memorized_ayahs(session: AsyncSession, db_user_id: int) -> list[Ayah]:
    result = await session.execute(
        select(Ayah)
        .join(MemorizationProgress, MemorizationProgress.ayah_id == Ayah.id)
        .where(
            MemorizationProgress.user_id == db_user_id,
            MemorizationProgress.status == ProgressStatus.memorized,
        )
    )
    return list(result.scalars().all())


async def get_stats(session: AsyncSession, db_user_id: int) -> dict:
    from datetime import datetime, time as dtime

    total = await session.scalar(
        select(func.count(MemorizationProgress.id)).where(MemorizationProgress.user_id == db_user_id)
    )

    memorized_count = await session.scalar(
        select(func.count(MemorizationProgress.id)).where(
            MemorizationProgress.user_id == db_user_id,
            MemorizationProgress.status == ProgressStatus.memorized,
        )
    )

    today_start = datetime.combine(datetime.now().date(), dtime.min)

    reviews_today = await session.scalar(
        select(func.count(Review.id)).where(
            Review.user_id == db_user_id,
            Review.reviewed_at >= today_start,
        )
    )

    correct_today = await session.scalar(
        select(func.count(Review.id)).where(
            Review.user_id == db_user_id,
            Review.reviewed_at >= today_start,
            Review.result == ReviewResult.correct,
        )
    )

    return {
        "total_assigned": total or 0,
        "memorized": memorized_count or 0,
        "reviews_today": reviews_today or 0,
        "correct_today": correct_today or 0,
    }


async def get_all_active_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).where(User.is_active == True))
    return list(result.scalars().all())
