import allure

def test_create_order(mainpage_client, products_client, cart_client, checkout_client, db_client, kafka_client):
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
        user_id = '2ec6efab-8e32-7ec1-b948-cmpe5c6036ff'
        quantity = 1
        cart_client.clear_cart(user_id)
        response_cart = cart_client.add_to_cart(currency, product_id, quantity, user_id)
        assert response_cart.status_code == 200
        request_body = {
            "userId": "2ec6efab-8e32-7ec1-b948-cmpe5c6036ff",
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
        response_body = response_checkout.json()
        assert response_checkout.status_code == 200
        assert response_body['orderId']
        assert response_body['shippingTrackingId']
        assert response_body['shippingCost']
        assert response_body['shippingAddress']
        assert response_body['items']
        order_id = response_body['orderId']

    with allure.step("DB check"):
        result_db = db_client.execute(
            '''
            SELECT
                o.order_id,
                oi.product_id,
                oi.quantity,
                oi.item_cost_currency_code,
                oi.item_cost_units,
                s.shipping_tracking_id,
                s.city,
                s.country,
                s.zip_code
            FROM accounting."order" o
            JOIN accounting.orderitem oi
                ON o.order_id = oi.order_id
            JOIN accounting.shipping s
                ON o.order_id = s.order_id
            WHERE o.order_id = %s
            ''',
            (order_id,)
        )

        db_shipping = result_db[0]
        assert result_db
        assert len(result_db) == len(response_body["items"])
        assert db_shipping[0] == order_id
        assert db_shipping[1] == product_id
        assert db_shipping[2] == quantity
        assert db_shipping[3] == currency
        assert db_shipping[6] == response_body["shippingAddress"]["city"]
        assert db_shipping[7] == response_body["shippingAddress"]["country"]
        assert db_shipping[8] == response_body["shippingAddress"]["zipCode"]

    with allure.step("Kafka check"):
        event = kafka_client.wait_for_event(
            topic="orders",
            order_id=order_id,
            timeout_ms=30000
        )
        assert event.order_id == order_id


