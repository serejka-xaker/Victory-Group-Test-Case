from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from .models import URLModel
from .utils import generate_short_id

async def get_url_by_full_url(db: AsyncSession, full_url: str) -> URLModel | None:
    """Поиск существующей ссылки"""
    result = await db.execute(select(URLModel).where(URLModel.full_url == str(full_url)))
    return result.scalar_one_or_none()

async def create_url(db: AsyncSession, full_url: str) -> URLModel:
    """Создание ссылки с защитой от коллизий"""
    existing = await get_url_by_full_url(db, full_url)
    if existing:
        return existing

    for _ in range(10):
        short_id = generate_short_id()
        db_url = URLModel(full_url=str(full_url), short_id=short_id)
        db.add(db_url)
        try:
            await db.commit()
            await db.refresh(db_url)
            return db_url
        except IntegrityError:
            await db.rollback()
            continue
    
    raise RuntimeError("Не удалось сгенерировать уникальный ID")

async def get_url_by_short_id(db: AsyncSession, short_id: str) -> URLModel | None:
    result = await db.execute(select(URLModel).where(URLModel.short_id == short_id))
    return result.scalar_one_or_none()

async def increment_clicks(db: AsyncSession, short_id: str) -> str | None:
    """Атомарное обновление счетчика кликов"""
    result = await db.execute(
        update(URLModel)
        .where(URLModel.short_id == short_id)
        .values(clicks=URLModel.clicks + 1)
        .returning(URLModel.full_url)
    )
    await db.commit()
    return result.scalar_one_or_none()


async def delete_url_by_short_id(db: AsyncSession, short_id: str) -> URLModel | None:
    db_url = await get_url_by_short_id(db, short_id)
    
    if db_url:
        db.expunge(db_url) 
        await db.execute(db.delete(URLModel).where(URLModel.short_id == short_id))
        await db.commit()
        return db_url
        
    return None


async def delete_expired_urls(db: AsyncSession, days: int = 30) -> int:
    threshold = datetime.now(timezone.utc) - timedelta(days=days)
    query = db.delete(URLModel).where(URLModel.created_at < threshold)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount