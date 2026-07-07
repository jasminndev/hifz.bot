from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.dependencies import create_access_token
from api.schemas import TokenResponse
from db.database import conf

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    admin_id: int
    secret: str


ADMIN_SECRET = "admin123" 


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    print(f"ADMIN_IDS: {conf.bot.ADMIN_IDS}")
    if data.admin_id not in conf.bot.ADMIN_IDS or data.secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Noto'g'ri ma'lumotlar")

    token = create_access_token({"sub": str(data.admin_id)})
    return TokenResponse(access_token=token)
