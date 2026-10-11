CHECKOUT_RESPONSE_SCHEMA = {
    "type": "object",
    "required": [
        "orderId",
        "shippingTrackingId",
        "shippingCost",
        "shippingAddress",
        "items",
    ],
    "properties": {
        "orderId": {
            "type": "string",
            "minLength": 1,
        },
        "shippingTrackingId": {
            "type": "string",
            "minLength": 1,
        },
        "shippingCost": {
            "type": "object",
        },
        "shippingAddress": {
            "type": "object",
        },
        "items": {
            "type": "array",
            "minItems": 1,
        },
    },
}