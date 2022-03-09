from marketing.pipeline.interface import Pipeline
from marketing.connection import laravel_connection
from marketing.pipeline.utils import transform_timestamp

orders = Pipeline(
    "Orders",
    laravel_connection,
    """
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
    lambda rows: [
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
    [
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
)
