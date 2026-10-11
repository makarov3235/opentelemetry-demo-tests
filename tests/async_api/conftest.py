import httpx
import pytest_asyncio

from config import BASE_URL


@pytest_asyncio.fixture
async def async_client():
    """Создаёт HTTP-клиент для асинхронных API-тестов."""

    timeout = httpx.Timeout(10.0)

    async with httpx.AsyncClient(
        base_url=BASE_URL,
        timeout=timeout,
    ) as client:
        yield client