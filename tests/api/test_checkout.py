from data.test_data import PRODUCT_ID, DEFAULT_CURRENCY, DEFAULT_QUANTITY, CHECKOUT_BODY
from data.order_builder import OrderBuilder
from utils.assertions import (assert_status_code, assert_order_response,)
from jsonschema import validate
from schemas.checkout_schema import CHECKOUT_RESPONSE_SCHEMA
from uuid import uuid4
import allure

#Positive
@allure.feature("Checkout")
@allure.story("Create order")
def test_create_order(checkout_client, cart_client):
    user_id = str(uuid4())

    cart_client.clear_cart(user_id)
    cart_client.add_to_cart(
        DEFAULT_CURRENCY,
        PRODUCT_ID,
        DEFAULT_QUANTITY,
        user_id,
    )

    request_body = (
        OrderBuilder()
        .with_user_id(user_id)
        .with_currency(DEFAULT_CURRENCY)
        .build()
    )

    response = checkout_client.create_order(
        DEFAULT_CURRENCY,
        request_body,
    )

    assert_status_code(response, 200)

    response_body = response.json()
    assert_order_response(response_body)
    validate(
        instance=response_body,
        schema=CHECKOUT_RESPONSE_SCHEMA,
    )


#Negative
@allure.feature("Checkout")
@allure.story("Create order without body")
def test_create_order_without_body(checkout_client, cart_client):
    user_id = str(uuid4())
    cart_client.clear_cart(user_id)
    cart_client.add_to_cart(DEFAULT_CURRENCY, PRODUCT_ID, DEFAULT_QUANTITY, user_id)
    currency = DEFAULT_CURRENCY

    response = checkout_client.create_order_empty_body(currency)

    assert response.status_code == 500
    #body = response.json()
    #assert body["code"] == "PAYMENT_FAILED"
    #assert "error" in body


@allure.feature("Checkout")
@allure.story("Create order without info about user")
def test_create_order_without_info_about_user(checkout_client, cart_client):
    user_id = str(uuid4())
    cart_client.add_to_cart(DEFAULT_CURRENCY, PRODUCT_ID, DEFAULT_QUANTITY, user_id)
    currency = DEFAULT_CURRENCY

    request_body = {        "address": {
            "streetAddress": "1600 Amphitheatre Parkway",
            "state": "CA",
            "country": "United States",
            "city": "Mountain View",
            "zipCode": "94043"
        },
        "userCurrency": DEFAULT_CURRENCY,
        "creditCard": {
            "creditCardCvv": 672,
            "creditCardExpirationMonth": 1,
            "creditCardExpirationYear": 2030,
            "creditCardNumber": "4432-8015-6152-0454"        }    }

    response = checkout_client.create_order(currency, request_body)


    assert response.status_code == 500


@allure.feature("Checkout")
@allure.story("Create order without info about credit card")
def test_create_order_without_info_about_card(checkout_client, cart_client):
    user_id = str(uuid4())
    cart_client.clear_cart(user_id)
    cart_client.add_to_cart(DEFAULT_CURRENCY, PRODUCT_ID, DEFAULT_QUANTITY, user_id)
    currency = DEFAULT_CURRENCY

    request_body = {"userId": user_id ,
        "email": "someone@example.com",
        "address": {
            "streetAddress": "1600 Amphitheatre Parkway",
            "state": "CA",
            "country": "United States",
            "city": "Mountain View",
            "zipCode": "94043"
        },
        "userCurrency": DEFAULT_CURRENCY }

    response = checkout_client.create_order(currency, request_body)

    assert_status_code(response, 422)

    body = response.json()

    assert body["code"] == "PAYMENT_FAILED"
    assert "error" in body


@allure.feature("Checkout")
@allure.story("Create order without info about adress")
def test_create_order_without_info_about_adress(checkout_client, cart_client):
    user_id = str(uuid4())
    cart_client.clear_cart(user_id)
    cart_client.add_to_cart(DEFAULT_CURRENCY, PRODUCT_ID, DEFAULT_QUANTITY, user_id)
    currency = DEFAULT_CURRENCY

    request_body = {
        "userId": user_id ,
        "email": "someone@example.com",
        "userCurrency": DEFAULT_CURRENCY,
        "creditCard": {
            "creditCardCvv": 672,
            "creditCardExpirationMonth": 1,
            "creditCardExpirationYear": 2030,
            "creditCardNumber": "4432-8015-6152-0454"
        }
    }

    response = checkout_client.create_order(currency, request_body)

    assert response.status_code == 200
    assert response.json()


@allure.feature("Checkout")
@allure.story("Create order with invalid email")
def test_create_order_with_invalid_email(checkout_client, cart_client):
    user_id = str(uuid4())

    cart_client.clear_cart(user_id)
    cart_client.add_to_cart(
        DEFAULT_CURRENCY,
        PRODUCT_ID,
        DEFAULT_QUANTITY,
        user_id,
    )

    request_body = (
        OrderBuilder()
        .with_user_id(user_id)
        .with_currency(DEFAULT_CURRENCY)
        .with_invalid_email()
        .build()
    )

    response = checkout_client.create_order(
        DEFAULT_CURRENCY,
        request_body,
    )

    assert response.status_code == 200
    assert response.json()["orderId"]