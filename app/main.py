from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from .database import engine, Base, get_db
from .schemas import URLCreate, URLInfo, URLStats
from . import crud  # Импортируем наш новый модуль


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Сервис сокращения ссылок", lifespan=lifespan)

@app.post("/shorten", response_model=URLInfo, status_code=201)
async def create_short_url(url: URLCreate, db: AsyncSession = Depends(get_db)):
    db_url = await crud.create_url(db, str(url.full_url))
    
    if not db_url:
        raise HTTPException(status_code=500, detail="Не удалось создать короткую ссылку")
    
    return db_url

@app.get("/{short_id}")
async def redirect_to_url(short_id: str, db: AsyncSession = Depends(get_db)):
    full_url = await crud.increment_clicks(db, short_id)
    
    if not full_url:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")

    return RedirectResponse(url=full_url)

@app.get("/stats/{short_id}", response_model=URLStats)
async def get_stats(short_id: str, db: AsyncSession = Depends(get_db)):
    url_entry = await crud.get_url_by_short_id(db, short_id)

    if not url_entry:
        raise HTTPException(status_code=404, detail="Статистика не найдена")

    return url_entry
