from clients.db_client import DBClient


class OrderRepository:
    """Repository for querying orders and related data in PostgreSQL."""

    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    def get_order_details_by_id(self, order_id: str) -> list[dict]:
        query = """
            SELECT
                o.order_id,
                oi.product_id,
                oi.quantity,
                oi.item_cost_currency_code,
                oi.item_cost_units,
                s.shipping_tracking_id,
                s.city,
                s.country,
                s.zip_code
            FROM accounting."order" o
            JOIN accounting.orderitem oi
                ON o.order_id = oi.order_id
            JOIN accounting.shipping s
                ON o.order_id = s.order_id
            WHERE o.order_id = %s
        """

        rows = self.db_client.execute(query, (order_id,))

        columns = [
            "order_id",
            "product_id",
            "quantity",
            "currency_code",
            "item_cost_units",
            "shipping_tracking_id",
            "city",
            "country",
            "zip_code",
        ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]