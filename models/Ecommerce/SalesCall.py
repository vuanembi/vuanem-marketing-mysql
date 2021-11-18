from models.Ecommerce.base import IMySQLTable, transform_timestamp
from models.engine import magento_engine

SalesCall: IMySQLTable = {
    "name": "SalesCall",
    "engine": magento_engine,
    "query": f"""
        SELECT
            customer_name AS name,
            customer_tel AS phone,
            customer_email AS email,
            gclid,
            campain,
            from_landing,
            created_at AS dt,
            shopify_order_id,
            IF(shopify_order_id <> '0', 'shopify_order', 'salescall') AS source
        FROM
            vuanem_ecommerce.vuanem_salescall_salescall
        """,
    "transform": lambda rows: [
        {
            "name": row["name"],
            "phone": row["phone"],
            "email": row["email"],
            "gclid": row["gclid"],
            "campain": row["campain"],
            "from_landing": row["from_landing"],
            "dt": transform_timestamp(row["dt"]),
            "shopify_order_id": row["shopify_order_id"],
            "source": row["source"],
        }
        for row in rows
    ],
    "schema": [
        {"name": "name", "type": "STRING"},
        {"name": "phone", "type": "STRING"},
        {"name": "email", "type": "STRING"},
        {"name": "gclid", "type": "STRING"},
        {"name": "campain", "type": "STRING"},
        {"name": "from_landing", "type": "STRING"},
        {"name": "dt", "type": "TIMESTAMP"},
        {"name": "shopify_order_id", "type": "INTEGER"},
        {"name": "source", "type": "STRING"},
    ],
}
