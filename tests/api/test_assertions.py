import pytest

from utils.assertions import (
    assert_status_code,
    assert_json_field_exists,
    assert_json_field_not_empty,
    assert_order_response,
)


class FakeResponse:
    def __init__(self, status_code: int, body: dict):
        self.status_code = status_code
        self._body = body
        self.text = str(body)

    def json(self):
        return self._body


def test_assert_status_code():
    response = FakeResponse(200, {"status": "ok"})

    assert_status_code(response, 200)


def test_assert_status_code_fails_with_details():
    response = FakeResponse(500, {"error": "Internal Server Error"})

    with pytest.raises(AssertionError, match="Expected status code 200"):
        assert_status_code(response, 200)


def test_assert_json_field_exists():
    body = {"orderId": "order-123"}

    assert_json_field_exists(body, "orderId")


def test_assert_json_field_exists_fails():
    body = {"status": "ok"}

    with pytest.raises(AssertionError, match="orderId"):
        assert_json_field_exists(body, "orderId")


def test_assert_json_field_not_empty():
    body = {"orderId": "order-123"}

    assert_json_field_not_empty(body, "orderId")


def test_assert_json_field_not_empty_fails():
    body = {"orderId": ""}

    with pytest.raises(AssertionError, match="non-empty"):
        assert_json_field_not_empty(body, "orderId")


def test_assert_order_response():
    body = {
        "orderId": "order-123",
        "shippingTrackingId": "tracking-123",
        "shippingCost": {"currencyCode": "USD", "units": 5, "nanos": 0},
        "shippingAddress": {"city": "Mountain View"},
        "items": [{"productId": "product-123"}],
    }

    assert_order_response(body)