def assert_status_code(response, expected_status: int) -> None:
    assert response.status_code == expected_status, (
        f"Expected status code {expected_status}, "
        f"got {response.status_code}. "
        f"Response body: {response.text}"
    )


def assert_json_field_exists(
    response_body: dict,
    field: str,
) -> None:
    assert field in response_body, (
        f"Expected field '{field}' in response. "
        f"Actual response: {response_body}"
    )


def assert_json_field_not_empty(
    response_body: dict,
    field: str,
) -> None:
    assert_json_field_exists(response_body, field)

    assert response_body[field], (
        f"Expected field '{field}' to be non-empty. "
        f"Actual value: {response_body[field]!r}"
    )


def assert_order_response(response_body: dict) -> None:
    required_fields = [
        "orderId",
        "shippingTrackingId",
        "shippingCost",
        "shippingAddress",
        "items",
    ]

    for field in required_fields:
        assert_json_field_not_empty(response_body, field)