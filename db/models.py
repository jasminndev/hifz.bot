import enum
from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, Enum as SAEnum
from sqlalchemy import String, Text, BigInteger, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import TimeBasedModel


class ProgressStatus(str, enum.Enum):
    pending = "pending"
    learning = "learning"
    memorized = "memorized"


class ReviewResult(str, enum.Enum):
    correct = "correct"
    incorrect = "incorrect"


class User(TimeBasedModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tg_username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fullname: Mapped[str] = mapped_column(String(200), nullable=False)
    daily_goal: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    progress: Mapped[list["MemorizationProgress"]] = relationship(back_populates="user")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")


class Ayah(TimeBasedModel):
    __tablename__ = "ayahs"
    __table_args__ = (UniqueConstraint("surah_number", "ayah_number"),)

    surah_number: Mapped[int] = mapped_column(Integer, nullable=False)
    ayah_number: Mapped[int] = mapped_column(Integer, nullable=False)
    arabic_text: Mapped[str] = mapped_column(Text, nullable=False)
    uzbek_text: Mapped[str] = mapped_column(Text, nullable=False)
    audio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    progress: Mapped[list["MemorizationProgress"]] = relationship(back_populates="ayah")
    reviews: Mapped[list["Review"]] = relationship(back_populates="ayah")


class MemorizationProgress(TimeBasedModel):
    __tablename__ = "memorization_progress"
    __table_args__ = (UniqueConstraint("user_id", "ayah_id"),)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    ayah_id: Mapped[int] = mapped_column(ForeignKey("ayahs.id"), nullable=False)
    status: Mapped[ProgressStatus] = mapped_column(SAEnum(ProgressStatus), default=ProgressStatus.pending)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    memorized_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    next_review_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    review_stage: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(back_populates="progress")
    ayah: Mapped["Ayah"] = relationship(back_populates="progress")


class Review(TimeBasedModel):
    __tablename__ = "reviews"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    ayah_id: Mapped[int] = mapped_column(ForeignKey("ayahs.id"), nullable=False)
    result: Mapped[ReviewResult] = mapped_column(SAEnum(ReviewResult), nullable=False)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    user: Mapped["User"] = relationship(back_populates="reviews")
    ayah: Mapped["Ayah"] = relationship(back_populates="reviews")
