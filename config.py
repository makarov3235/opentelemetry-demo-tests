import os

BASE_URL = os.getenv(
    "BASE_URL",
    "http://localhost:8080",
)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "17469"))
DB_NAME = os.getenv("DB_NAME", "astronomy_db")
DB_USER = os.getenv("DB_USER", "astronomy_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "astronomy_password")
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:29092",
)