from clients.base_client import BaseClient

class CheckoutClient(BaseClient):

    def create_order(self, currency, body):
        return self.post("/api/checkout", params={"currencyCode": currency}, json = body)

    def create_order_empty_body(self, currency):
        return self.post("/api/checkout", params={"currencyCode": currency})