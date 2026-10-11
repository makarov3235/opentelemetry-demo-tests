import asyncio
from uuid import uuid4

import pytest

from data.test_data import DEFAULT_CURRENCY, PRODUCT_ID, DEFAULT_QUANTITY


@pytest.mark.asyncio
async def test_users_carts_are_isolated(async_client):
    """Проверяем изоляцию корзин при параллельных запросах."""

    users = [
        {
            "user_id": str(uuid4()),
            "product_id": PRODUCT_ID,
            "quantity": DEFAULT_QUANTITY,
        },
        {
            "user_id": str(uuid4()),
            "product_id": "0PUK6V6EV0",
            "quantity": 2,
        },
        {
            "user_id": str(uuid4()),
            "product_id": "1YMWWN1N4O",
            "quantity": 3,
        },
    ]

    async def add_product_to_user_cart(user):
        response = await async_client.post(
            "/api/cart",
            params={"currencyCode": DEFAULT_CURRENCY},
            json={
                "userId": user["user_id"],
                "item": {
                    "productId": user["product_id"],
                    "quantity": user["quantity"],
                },
            },
        )
        return user, response

    # Параллельно добавляем товары в три корзины.
    add_results = await asyncio.gather(
        *(add_product_to_user_cart(user) for user in users)
    )

    for user, response in add_results:
        assert response.status_code == 200, (
            f"Не удалось добавить товар пользователю "
            f"{user['user_id']}: {response.status_code}, {response.text}"
        )

    async def get_user_cart(user):
        response = await async_client.get(
            "/api/cart",
            params={
                "sessionId": user["user_id"],
                "currencyCode": DEFAULT_CURRENCY,
            },
        )
        return user, response

    # Параллельно получаем корзины.
    cart_results = await asyncio.gather(
        *(get_user_cart(user) for user in users)
    )

    for user, response in cart_results:
        assert response.status_code == 200, (
            f"Не удалось получить корзину пользователя "
            f"{user['user_id']}: {response.status_code}, {response.text}"
        )

        cart = response.json()

        assert cart["userId"] == user["user_id"]
        assert len(cart["items"]) == 1
        assert cart["items"][0]["productId"] == user["product_id"]
        assert cart["items"][0]["quantity"] == user["quantity"]