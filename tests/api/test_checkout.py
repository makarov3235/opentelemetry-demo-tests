from data.test_data import PRODUCT_ID, DEFAULT_CURRENCY, DEFAULT_QUANTITY, CHECKOUT_BODY
import allure

#Positive
@allure.feature("Checkout")
@allure.story("Create order")
def test_create_order(checkout_client, cart_client):
    user_id = '2ec6efab-8e41-4ec1-b948-cffe7b2026ff'
    cart_client.clear_cart(user_id)
    cart_client.add_to_cart(DEFAULT_CURRENCY, PRODUCT_ID, DEFAULT_QUANTITY, user_id)
    currency = DEFAULT_CURRENCY

    request_body = CHECKOUT_BODY

    response = checkout_client.create_order(currency, request_body)
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['orderId']
    assert response_body['shippingTrackingId']
    assert response_body['shippingCost']
    assert response_body['shippingAddress']
    assert response_body['items']


#Negative
@allure.feature("Checkout")
@allure.story("Create order without body")
def test_create_order_without_body(checkout_client, cart_client):
    user_id = '2ec6efab-8e41-4ec1-b948-cffe4b2024ss'
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
    user_id = '2ec6efab-8e41-4ec1-b948-cffe4b2036ff'
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
@allure.story("Create order without info about credit cart")
def test_create_order_without_info_about_card(checkout_client, cart_client):
    user_id = '2ec6efab-8e41-4ec1-b948-cffe4b3026ff'
    cart_client.clear_cart(user_id)
    cart_client.add_to_cart(DEFAULT_CURRENCY, PRODUCT_ID, DEFAULT_QUANTITY, user_id)
    currency = DEFAULT_CURRENCY

    request_body = {"userId": "2ec6efab-8e41-4ec1-b948-cffe4b3026ff",
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

    assert response.status_code == 422

    body = response.json()

    assert body["code"] == "PAYMENT_FAILED"
    assert "error" in body


@allure.feature("Checkout")
@allure.story("Create order without info about adress")
def test_create_order_without_info_about_adress(checkout_client, cart_client):
    user_id = '2ec6efab-8e41-4ec1-b948-cffe4b3032ff'
    cart_client.clear_cart(user_id)
    cart_client.add_to_cart(DEFAULT_CURRENCY, PRODUCT_ID, DEFAULT_QUANTITY, user_id)
    currency = DEFAULT_CURRENCY

    request_body = {
        "userId": "2ec6efab-8e41-4ec1-b948-cffe4b3032ff",
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
