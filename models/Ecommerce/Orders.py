from models.Ecommerce.base import IMySQLTable, transform_timestamp
from models.engine import laravel_engine

Orders: IMySQLTable = {
    "name": "Orders",
    "engine": laravel_engine,
    "query": f"""
        SELECT
            id,
            user_id,
            email,
            phone_number,
            amount,
            real_amount,
            utm_campaign,
            utm_medium,
            utm_source,
            created_at
        FROM
            vuanem_ecommerce.orders
        """,
    "transform": lambda rows: [
        {
            "call_id": row["call_id"],
            "customer_id": row["customer_id"],
            "ticket_id": row["ticket_id"],
            "caller": row["caller"],
            "call_type": row["call_type"],
            "call_status": row["call_status"],
            "start_time": transform_timestamp(row["start_time"]),
            "end_time": transform_timestamp(row["end_time"]),
            "created_at": transform_timestamp(row["created_at"]),
            "updated_at": transform_timestamp(row["updated_at"]),
        }
        for row in rows
    ],
    "schema": [
        {"name": "call_id", "type": "STRING"},
        {"name": "customer_id", "type": "INTEGER"},
        {"name": "ticket_id", "type": "INTEGER"},
        {"name": "caller", "type": "STRING"},
        {"name": "call_type", "type": "INTEGER"},
        {"name": "call_status", "type": "STRING"},
        {"name": "start_time", "type": "TIMESTAMP"},
        {"name": "end_time", "type": "TIMESTAMP"},
        {"name": "created_at", "type": "TIMESTAMP"},
        {"name": "updated_at", "type": "TIMESTAMP"},
    ],
}
