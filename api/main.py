from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import auth, stats

app = FastAPI(title="HifzBot Admin API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(stats.router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "HifzBot Admin API"}
