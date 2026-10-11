from data.order_builder import OrderBuilder


def test_order_builder_creates_default_body():
    body = OrderBuilder().build()

    assert body["userId"]
    assert body["email"]
    assert body["address"]
    assert body["userCurrency"] == "USD"
    assert body["creditCard"]


def test_order_builder_overrides_currency():
    body = OrderBuilder().with_currency("EUR").build()

    assert body["userCurrency"] == "EUR"


def test_order_builder_can_remove_address():
    body = OrderBuilder().without_address().build()

    assert "address" not in body


def test_order_builder_can_override_email():
    body = OrderBuilder().with_email("test@example.com").build()

    assert body["email"] == "test@example.com"


def test_order_builder_returns_independent_body():
    builder = OrderBuilder()

    first_body = builder.build()
    first_body["address"]["city"] = "Changed City"

    second_body = builder.build()

    assert second_body["address"]["city"] != "Changed City"