from clients.products_client import ProductsClient
from clients.cart_client import CartClient
from clients.checkout_client import CheckoutClient
from clients.mainpage_client import MainpageClient
from clients.db_client import DBClient
from clients.kafka_client import KafkaClient
from config import (
    BASE_URL,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    KAFKA_BOOTSTRAP_SERVERS,
)
import pytest

@pytest.fixture
def products_client():
    return ProductsClient(BASE_URL)

@pytest.fixture
def cart_client():
    return CartClient(BASE_URL)

@pytest.fixture
def checkout_client():
    return CheckoutClient(BASE_URL)

@pytest.fixture
def mainpage_client():
    return MainpageClient(BASE_URL)

@pytest.fixture
def db_client():
    client = DBClient(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    yield client

    client.close()


@pytest.fixture
def kafka_client():
    return KafkaClient(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
    )

