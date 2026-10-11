import allure
from repositories.order_repository import OrderRepository
from utils.allure_helpers import attach_json, attach_text
from contextlib import closing
from uuid import uuid4

def test_create_order(mainpage_client, products_client, cart_client, checkout_client, db_client, kafka_client):
    with kafka_client.consumer("orders") as consumer:
        with allure.step("Get main page"):
            response_mainpage = mainpage_client.get_mainpage()
            response_currency = mainpage_client.get_currencies()
            assert response_mainpage.status_code == 200
            assert response_currency.status_code == 200
            assert response_currency.json()
            currency = response_currency.json()[-1]

        with allure.step("Add product to cart"):
            response_products = products_client.get_products(currency)
            product_id = response_products.json()[1]["id"]
            assert response_products.status_code == 200
            response_product = products_client.get_product(product_id, currency)
            assert response_product.status_code == 200

        with allure.step("Create order"):
            user_id = str(uuid4())
            quantity = 1
            cart_client.clear_cart(user_id)
            response_cart = cart_client.add_to_cart(currency, product_id, quantity, user_id)
            assert response_cart.status_code == 200
            request_body = {
                "userId": user_id,
                "email": "sometwo@example.com",
                "address": {
                    "streetAddress": "1600 Amphitheatre Parkway",
                    "state": "CA",
                    "country": "United States",
                    "city": "Mountain Viev",
                    "zipCode": "94043"
                },
                "userCurrency": currency,
                "creditCard": {
                    "creditCardCvv": 672,
                    "creditCardExpirationMonth": 1,
                    "creditCardExpirationYear": 2030,
                    "creditCardNumber": "4432-8015-6152-0454"
                }
            }
            response_checkout = checkout_client.create_order(currency, request_body)

            assert response_checkout.status_code == 200

            response_body = response_checkout.json()

            attach_json(
                "Checkout API response",
                {
                    "status_code": response_checkout.status_code,
                    "body": response_body,
                },
            )
            assert response_body['orderId']
            assert response_body['shippingTrackingId']
            assert response_body['shippingCost']
            assert response_body['shippingAddress']
            assert response_body['items']
            order_id = response_body['orderId']


        with allure.step("DB check"):
            order_repository = OrderRepository(db_client)

            result_db = order_repository.get_order_details_by_id(order_id)
            attach_json(
                "PostgreSQL order details",
                result_db,
            )
            assert result_db, (
                f"Order not found in PostgreSQL or JOIN returned no rows. "
                f"order_id={order_id}"
            )

            assert len(result_db) == len(response_body["items"])

            db_order = result_db[0]

            assert db_order["order_id"] == order_id
            assert db_order["product_id"] == product_id
            assert db_order["quantity"] == quantity
            assert db_order["currency_code"] == currency

            assert db_order["city"] == response_body["shippingAddress"]["city"]
            assert db_order["country"] == response_body["shippingAddress"]["country"]
            assert db_order["zip_code"] == response_body["shippingAddress"]["zipCode"]

        with allure.step("Kafka check"):
            event = kafka_client.wait_for_event(
                consumer=consumer,
                topic="orders",
                order_id=order_id,
            )

            attach_text(
                "Kafka order event",
                str(event),
            )

            assert event.order_id == order_id




