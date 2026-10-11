import pytest
from jsonschema import validate, ValidationError

from schemas.checkout_schema import CHECKOUT_RESPONSE_SCHEMA


def test_valid_checkout_response_matches_schema():
    response_body = {
        "orderId": "order-123",
        "shippingTrackingId": "tracking-123",
        "shippingCost": {
            "currencyCode": "USD",
            "units": 5,
            "nanos": 0,
        },
        "shippingAddress": {
            "city": "Mountain View",
        },
        "items": [
            {
                "productId": "product-123",
            }
        ],
    }

    validate(
        instance=response_body,
        schema=CHECKOUT_RESPONSE_SCHEMA,
    )


def test_checkout_response_without_order_id_fails():
    response_body = {
        "shippingTrackingId": "tracking-123",
        "shippingCost": {},
        "shippingAddress": {},
        "items": [{"productId": "product-123"}],
    }

    with pytest.raises(ValidationError):
        validate(
            instance=response_body,
            schema=CHECKOUT_RESPONSE_SCHEMA,
        )


def test_checkout_response_with_invalid_order_id_type_fails():
    response_body = {
        "orderId": 123,
        "shippingTrackingId": "tracking-123",
        "shippingCost": {},
        "shippingAddress": {},
        "items": [{"productId": "product-123"}],
    }

    with pytest.raises(ValidationError):
        validate(
            instance=response_body,
            schema=CHECKOUT_RESPONSE_SCHEMA,
        )