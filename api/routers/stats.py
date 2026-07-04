from datetime import datetime, time as dtime

from fastapi import APIRouter, Depends
from sqlalchemy import select, func

from api.dependencies import verify_token
from api.schemas import DashboardStats
from db.models import User, Ayah, MemorizationProgress, Review, ProgressStatus
from db.session import AsyncSessionLocal

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(token: dict = Depends(verify_token)):
    async with AsyncSessionLocal() as session:
        today_start = datetime.combine(datetime.now().date(), dtime.min)

        total_users = await session.scalar(select(func.count(User.id)))
        active_users = await session.scalar(
            select(func.count(User.id)).where(User.is_active == True)
        )
        total_ayahs = await session.scalar(select(func.count(Ayah.id)))
        total_memorized = await session.scalar(
            select(func.count(MemorizationProgress.id)).where(
                MemorizationProgress.status == ProgressStatus.memorized
            )
        )
        total_reviews = await session.scalar(select(func.count(Review.id)))
        new_users_today = await session.scalar(
            select(func.count(User.id)).where(User.created_at >= today_start)
        )
        reviews_today = await session.scalar(
            select(func.count(Review.id)).where(Review.reviewed_at >= today_start)
        )

        return DashboardStats(
            total_users=total_users or 0,
            active_users=active_users or 0,
            total_ayahs=total_ayahs or 0,
            total_memorized=total_memorized or 0,
            total_reviews=total_reviews or 0,
            new_users_today=new_users_today or 0,
            reviews_today=reviews_today or 0,
        )
