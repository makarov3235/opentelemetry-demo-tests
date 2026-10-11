import asyncio

import pytest


@pytest.mark.asyncio
async def test_catalog_endpoints_are_available_concurrently(async_client):
    """Проверяем доступность основных API-эндпоинтов."""

    responses = await asyncio.gather(
        async_client.get("/"),
        async_client.get("/api/currency"),
        async_client.get("/api/products"),
    )

    assert responses[0].status_code == 200
    assert responses[1].status_code == 200
    assert responses[2].status_code == 200

    currencies = responses[1].json()
    products = responses[2].json()

    assert currencies
    assert products


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint",
    [
        "/api/products",
        "/api/currency",
    ],
)
async def test_catalog_handles_concurrent_requests(async_client, endpoint):
    """Проверяем обработку конкурентных запросов к API."""

    number_of_requests = 10

    responses = await asyncio.gather(
        *[
            async_client.get(endpoint)
            for _ in range(number_of_requests)
        ]
    )

    assert len(responses) == number_of_requests

    for response in responses:
        assert response.status_code == 200, (
            f"Запрос к {endpoint} вернул статус "
            f"{response.status_code}: {response.text}"
        )

        assert response.json(), (
            f"Запрос к {endpoint} вернул пустой ответ"
        )