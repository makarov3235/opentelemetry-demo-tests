from kafka import KafkaConsumer

from proto.demo_pb2 import OrderResult


class KafkaClient:

    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers

    def wait_for_event(
        self,
        topic: str,
        order_id: str,
        timeout_ms: int = 10000
    ) -> OrderResult:

        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset="earliest",
            consumer_timeout_ms=timeout_ms,
        )

        try:
            for message in consumer:
                event = OrderResult()
                event.ParseFromString(message.value)

                if event.order_id == order_id:
                    return event

            raise TimeoutError(
                f"Order event not found: {order_id}"
            )

        finally:
            consumer.close()