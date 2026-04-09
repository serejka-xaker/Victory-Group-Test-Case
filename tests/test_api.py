import pytest
import string
from unittest.mock import AsyncMock, MagicMock
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.utils import generate_short_id
from app.crud import create_url
from app.database import Base, engine


def test_generate_short_id_logic():
    size = 10
    short_id = generate_short_id(size=size)
    assert len(short_id) == size
    assert all(c in (string.ascii_letters + string.digits) for c in short_id)

@pytest.mark.asyncio
async def test_create_url_logic_existing():
    """Тест: Если URL уже есть в базе, возвращается существующий объект"""
    mock_db = AsyncMock()
    test_url = "https://google.com"

    mock_result = MagicMock()
    fake_url_obj = MagicMock()
    fake_url_obj.short_id = "abc12345"
    
    mock_result.scalar_one_or_none.return_value = fake_url_obj

    mock_db.execute.return_value = mock_result

    result = await create_url(mock_db, test_url)

    assert result.short_id == "abc12345"
    mock_db.add.assert_not_called()



@pytest.mark.asyncio
async def test_api_invalid_url():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/shorten", json={"full_url": "invalid-url"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_api_stats_not_found():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/stats/nonexistent_id")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_url_collision_retry():
    """Тест: проверка, что при коллизии short_id происходит повторная попытка"""
    from sqlalchemy.exc import IntegrityError
    mock_db = AsyncMock()
    
    mock_select_result = MagicMock()
    mock_select_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_select_result

    mock_db.commit.side_effect = [
        IntegrityError(None, None, None), 
        IntegrityError(None, None, None), 
        None
    ]


    result = await create_url(mock_db, "https://complex-test.com")


    assert mock_db.commit.call_count == 3  
    assert mock_db.rollback.call_count == 2  
    assert result is not None

