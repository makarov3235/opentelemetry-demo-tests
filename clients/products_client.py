from clients.base_client import BaseClient

class ProductsClient(BaseClient):

    def get_products(self, currency):
        return self.get("/api/products", params={"currencyCode": currency})

    def get_product(self, product_id, currency):
        return self.get(f"/api/products/{product_id}", params={"currencyCode": currency})