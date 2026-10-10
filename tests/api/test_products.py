import pytest
import allure

from data.test_data import PRODUCT_ID, DEFAULT_CURRENCY

# Positive
@allure.feature("Products")
@allure.story("Get products")
def test_get_products(products_client):
    response = products_client.get_products(DEFAULT_CURRENCY)
    body = response.json()

    assert response.status_code == 200
    assert body[0]["id"] == PRODUCT_ID
    assert "name" in body[0]
    assert "priceUsd" in body[0]
    assert "picture" in body[0]


@allure.feature("Products")
@allure.story("Get product")
@pytest.mark.parametrize('currency, product_id', [
        ('USD', '0PUK6V6EV0'),
        ('RUB', '1YMWWN1N4O'),
        ('EUR', '2ZYFJ3GM2N'),
    ]
)
def test_get_product(products_client, currency, product_id):
    response = products_client.get_product(product_id, currency)
    body = response.json()

    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert "name" in body
    assert "priceUsd" in body
    assert "picture" in body



# Negative
@allure.feature("Products")
@allure.story("Get products with invalid currency")
@pytest.mark.parametrize('currency', ['PASHA', 'доллар', '123'])
def test_get_products_invalid_currency(products_client, currency):
    response = products_client.get_products(currency)

    assert response.status_code == 200

    products = response.json()
    for product in products:
        assert product["priceUsd"]["currencyCode"] == currency
        assert product["priceUsd"]["units"] == 0
        assert product["priceUsd"]["nanos"] == 0


@allure.feature("Products")
@allure.story("Get products with invalid product id")
@pytest.mark.parametrize('product_id', ['PASHA', 'fhghfuygfuy', '123'])
def test_get_product_incorrect_poduct_id(products_client, product_id):
    response = products_client.get_product(product_id, DEFAULT_CURRENCY)

    assert response.status_code == 500
