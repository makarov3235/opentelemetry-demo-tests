import pytest
import allure
from data.test_data import PRODUCT_ID, DEFAULT_CURRENCY, DEFAULT_QUANTITY
from uuid import uuid4

#Positive
@allure.feature("Cart")
@allure.story("Add to cart")
@pytest.mark.parametrize('currency, product_id, quantity', [
        ('USD', '0PUK6V6EV0', 1),
        ('RUB', '1YMWWN1N4O', 2),
        ('EUR', '2ZYFJ3GM2N', 3),
    ]
)
def test_add_to_cart(cart_client, currency, product_id, quantity):
    user_id = str(uuid4())
    cart_client.clear_cart(user_id)
    response = cart_client.add_to_cart(currency, product_id, quantity, user_id)
    body = response.json()

    assert response.status_code == 200
    # assert body['userId'] == user_id
    assert body['items'][0]['productId'] == product_id
    assert body['items'][0]['quantity'] == quantity


@allure.feature("Cart")
@allure.story("Clear cart")
def test_clear_cart(cart_client):
    user_id = str(uuid4())
    response = cart_client.clear_cart(user_id)

    assert response.status_code == 204

    cart_response = cart_client.get_cart(user_id)
    body = cart_response.json()

    assert cart_response.status_code == 200
    assert body['items'] == []



#Negative
@allure.feature("Cart")
@allure.story("Add to cart so many products (1000)")
def test_add_to_cart_so_many_products(cart_client):
    user_id = str(uuid4())
    quantity = 1000
    cart_client.clear_cart(user_id)
    response = cart_client.add_to_cart(DEFAULT_CURRENCY, PRODUCT_ID, quantity, user_id)
    body = response.json()

    assert response.status_code == 200
    assert body['items'][0]['productId'] == PRODUCT_ID
    assert body['items'][0]['quantity'] == quantity


@allure.feature("Cart")
@allure.story("Add to cart so many products (1000000+)")
@pytest.mark.parametrize('currency, product_id, quantity', [
        ('USD', '0PUK6V6EV0', 15465456456456465),
        ('RUB', '1YMWWN1N4O', 25465456456456465),
        ('EUR', '2ZYFJ3GM2N', 35465456456456465),
    ]
)
def test_add_to_cart_soo_many_products(cart_client, currency, product_id, quantity):
    user_id = str(uuid4())
    cart_client.clear_cart(user_id)
    response = cart_client.add_to_cart(currency, product_id, quantity, user_id)

    assert response.status_code == 500


@allure.feature("Cart")
@allure.story("Add to cart product with incorrect product id")
def test_add_to_cart_incorrect_product_id(cart_client):
    user_id = str(uuid4())
    product_id = 'Pasha'
    cart_client.clear_cart(user_id)
    response = cart_client.add_to_cart(DEFAULT_CURRENCY, product_id, DEFAULT_QUANTITY, user_id)
    body = response.json()

    assert response.status_code == 200
    assert body['items'][0]['productId'] == product_id


@allure.feature("Cart")
@allure.story("Add to cart with empty body")
def test_add_to_cart_empty_body(cart_client):

    response = cart_client.add_to_cart("USD")

    assert response.status_code == 500


@allure.feature("Cart")
@allure.story("Add to cart with empty info about user")
def test_add_to_cart_empty_info_about_user(cart_client):
    response = cart_client.add_to_cart(DEFAULT_CURRENCY, PRODUCT_ID, DEFAULT_QUANTITY)
    body = response.json()

    assert response.status_code == 200
    assert body['items'][0]['productId'] == PRODUCT_ID


@allure.feature("Cart")
@allure.story("Add to cart with empty info about product")
def test_add_to_cart_empty_info_about_product(cart_client):
    user_id = str(uuid4())
    cart_client.clear_cart(user_id)
    response = cart_client.add_to_cart(DEFAULT_CURRENCY, user_id)

    assert response.status_code == 500
