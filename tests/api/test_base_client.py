import requests
import pytest

from clients.base_client import BaseClient


def test_request_timeout():
    client = BaseClient("http://127.0.0.1:1")

    with pytest.raises(requests.RequestException):
        client.get("/products", timeout=0.1)


def test_connection_error_is_logged(caplog):
    client = BaseClient("http://127.0.0.1:1")

    with pytest.raises(requests.ConnectionError):
        client.get("/products")

    assert "Request failed" in caplog.text
    assert "GET" in caplog.text