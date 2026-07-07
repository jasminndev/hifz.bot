from datetime import datetime

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserSchema(BaseModel):
    id: int
    user_id: int
    fullname: str
    tg_username: str | None
    daily_goal: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AyahSchema(BaseModel):
    id: int
    surah_number: int
    ayah_number: int
    arabic_text: str
    uzbek_text: str
    audio_url: str | None

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_users: int
    active_users: int
    total_ayahs: int
    total_memorized: int
    total_reviews: int
    new_users_today: int
    reviews_today: int
