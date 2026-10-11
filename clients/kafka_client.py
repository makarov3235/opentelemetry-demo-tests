import logging
import time
from contextlib import contextmanager
from collections.abc import Iterator

from kafka import KafkaConsumer

from proto.demo_pb2 import OrderResult


logger = logging.getLogger(__name__)


class KafkaClient:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers

    def create_consumer(self, topic: str) -> KafkaConsumer:
        consumer = KafkaConsumer(
            bootstrap_servers=self.bootstrap_servers,
            enable_auto_commit=False,
            auto_offset_reset="latest",
        )

        try:
            consumer.subscribe([topic])

            # Дожидаемся назначения партиций.
            deadline = time.monotonic() + 10

            while not consumer.assignment():
                if time.monotonic() >= deadline:
                    raise TimeoutError(
                        f"Kafka partitions were not assigned: topic={topic}"
                    )

                consumer.poll(timeout_ms=100)

            # Перемещаемся в конец каждой назначенной партиции.
            consumer.seek_to_end()

            # Применяем позиции чтения после seek_to_end().
            for partition in consumer.assignment():
                consumer.position(partition)

            logger.info(
                "Kafka consumer ready: topic=%s, partitions=%s",
                topic,
                consumer.assignment(),
            )

            return consumer

        except Exception:
            consumer.close()
            raise

    @contextmanager
    def consumer(self, topic: str) -> Iterator[KafkaConsumer]:
        """Создаёт Consumer и гарантированно закрывает его после использования."""
        kafka_consumer = self.create_consumer(topic)

        try:
            yield kafka_consumer
        finally:
            logger.info("Closing Kafka consumer: topic=%s", topic)
            kafka_consumer.close()

    def wait_for_event(
            self,
            consumer: KafkaConsumer,
            topic: str,
            order_id: str,
            timeout_ms: int = 10000,
    ) -> OrderResult:
        deadline = time.monotonic() + timeout_ms / 1000

        logger.info(
            "Waiting for Kafka event: topic=%s, order_id=%s",
            topic,
            order_id,
        )

        while time.monotonic() < deadline:
            remaining_ms = max(
                1,
                int((deadline - time.monotonic()) * 1000),
            )

            records = consumer.poll(
                timeout_ms=min(remaining_ms, 500),
            )

            for partition, messages in records.items():
                for message in messages:
                    event = OrderResult()

                    try:
                        event.ParseFromString(message.value)
                    except Exception:
                        logger.exception(
                            "Failed to parse Kafka message: "
                            "topic=%s, partition=%s, offset=%s",
                            topic,
                            partition.partition,
                            message.offset,
                        )
                        continue

                    if event.order_id == order_id:
                        logger.info(
                            "Kafka event found: topic=%s, order_id=%s",
                            topic,
                            order_id,
                        )
                        return event

        raise TimeoutError(
            f"Kafka event not found: topic={topic}, "
            f"order_id={order_id}, timeout_ms={timeout_ms}"
        )

        try:
            while time.monotonic() < deadline:
                remaining_ms = max(
                    1,
                    int((deadline - time.monotonic()) * 1000),
                )

                records = consumer.poll(
                    timeout_ms=min(remaining_ms, 500),
                )

                for messages in records.values():
                    for message in messages:
                        event = OrderResult()
                        event.ParseFromString(message.value)

                        if event.order_id == order_id:
                            logger.info(
                                "Kafka event found: topic=%s, order_id=%s",
                                topic,
                                order_id,
                            )
                            return event

            raise TimeoutError(
                f"Kafka event not found: topic={topic}, "
                f"order_id={order_id}, timeout_ms={timeout_ms}"
            )

        except Exception:
            logger.exception(
                "Kafka event wait failed: topic=%s, order_id=%s",
                topic,
                order_id,
            )
            raise