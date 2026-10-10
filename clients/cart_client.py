from clients.base_client import BaseClient

class CartClient(BaseClient):

    def add_to_cart(self, currency, product_id=None, quantity=None, user_id=None):
        body = None

        if product_id is not None:
            body = {"item": {
                    "productId": product_id,
                    "quantity": quantity
                },
                "userId": user_id}

        return self.post("/api/cart", params={"currencyCode": currency}, json=body)

    def clear_cart(self, user_id):
        return self.delete("/api/cart", json={"userId": user_id})

    def get_cart(self, user_id):
        return self.get("/api/cart", json={"userId": user_id})
