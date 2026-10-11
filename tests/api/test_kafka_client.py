import pytest

from clients.kafka_client import KafkaClient
from proto.demo_pb2 import OrderResult


class FakeMessage:
    def __init__(self, value: bytes, offset: int = 0):
        self.value = value
        self.offset = offset


class FakePartition:
    partition = 0


def test_wait_for_event_returns_matching_order():
    expected_order_id = "order-123"

    event = OrderResult()
    event.order_id = expected_order_id

    message = FakeMessage(event.SerializeToString())

    class FakeConsumer:
        def poll(self, timeout_ms):
            return {
                FakePartition(): [message],
            }

    client = KafkaClient("localhost:29092")

    result = client.wait_for_event(
        consumer=FakeConsumer(),
        topic="orders",
        order_id=expected_order_id,
        timeout_ms=1000,
    )

    assert result.order_id == expected_order_id


def test_wait_for_event_skips_invalid_message(caplog):
    expected_order_id = "order-123"

    event = OrderResult()
    event.order_id = expected_order_id

    messages = [
        FakeMessage(b"\xff\xff\xff", offset=1),
        FakeMessage(event.SerializeToString(), offset=2),
    ]

    class FakeConsumer:
        def __init__(self):
            self.polled = False

        def poll(self, timeout_ms):
            if self.polled:
                return {}

            self.polled = True

            return {
                FakePartition(): messages,
            }

    client = KafkaClient("localhost:29092")

    result = client.wait_for_event(
        consumer=FakeConsumer(),
        topic="orders",
        order_id=expected_order_id,
        timeout_ms=1000,
    )

    assert result.order_id == expected_order_id
    assert "Failed to parse Kafka message" in caplog.text


def test_wait_for_event_raises_timeout():
    class FakeConsumer:
        def poll(self, timeout_ms):
            return {}

    client = KafkaClient("localhost:29092")

    with pytest.raises(TimeoutError, match="Kafka event not found"):
        client.wait_for_event(
            consumer=FakeConsumer(),
            topic="orders",
            order_id="missing-order",
            timeout_ms=100,
        )