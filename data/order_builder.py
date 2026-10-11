from copy import deepcopy

from faker import Faker

fake = Faker()


class OrderBuilder:
    """Builder for creating checkout request bodies."""

    def __init__(self):
        self._body = {
            "userId": fake.uuid4(),
            "email": fake.email(),
            "address": {
                "streetAddress": fake.street_address(),
                "state": fake.state_abbr(),
                "country": "United States",
                "city": fake.city(),
                "zipCode": fake.zipcode(),
            },
            "userCurrency": "USD",
            "creditCard": {
                "creditCardCvv": 672,
                "creditCardExpirationMonth": 1,
                "creditCardExpirationYear": 2030,
                "creditCardNumber": "4432-8015-6152-0454",
            },
        }

    def with_user_id(self, user_id: str):
        self._body["userId"] = user_id
        return self

    def with_email(self, email: str):
        self._body["email"] = email
        return self

    def with_currency(self, currency: str):
        self._body["userCurrency"] = currency
        return self

    def without_user_id(self):
        self._body.pop("userId", None)
        return self

    def without_address(self):
        self._body.pop("address", None)
        return self

    def without_credit_card(self):
        self._body.pop("creditCard", None)
        return self

    def with_invalid_email(self):
        self._body["email"] = "invalid-email"
        return self

    def build(self) -> dict:
        return deepcopy(self._body)