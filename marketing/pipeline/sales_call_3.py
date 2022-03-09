from db.mysql import get_ssh
from marketing.pipeline.interface import Pipeline
from marketing.config import webhook_db
from marketing.pipeline.utils import transform_timestamp

sales_call_3 = Pipeline(
    "SalesCall3",
    get_ssh(webhook_db),
    """
        SELECT
            id,
            contact_id,
            customer_name,
            customer_tel,
            customer_email,
            source,
            from_landing,
            order_id,
            notes,
            customer_notes,
            customer_adress,
            customer_actions,
            customer_agents,
            smart_tags,
            ipaddress,
            ticket_id,
            created_at,
            updated_at
        FROM salecalls
        """,
    lambda rows: [
        {
            "id": row["id"],
            "contact_id": row["contact_id"],
            "customer_name": row["customer_name"],
            "customer_tel": row["customer_tel"],
            "customer_email": row["customer_email"],
            "source": row["source"],
            "from_landing": row["from_landing"],
            "order_id": row["order_id"],
            "notes": row["notes"],
            "customer_notes": row["customer_notes"],
            "customer_adress": row["customer_adress"],
            "customer_actions": row["customer_actions"],
            "customer_agents": row["customer_agents"],
            "smart_tags": row["smart_tags"],
            "ipaddress": row["ipaddress"],
            "ticket_id": row["ticket_id"],
            "created_at": transform_timestamp(row["created_at"]),
            "updated_at": transform_timestamp(row["updated_at"]),
        }
        for row in rows
    ],
    [
        {"name": "id", "type": "NUMERIC"},
        {"name": "contact_id", "type": "NUMERIC"},
        {"name": "customer_name", "type": "STRING"},
        {"name": "customer_tel", "type": "STRING"},
        {"name": "customer_email", "type": "STRING"},
        {"name": "source", "type": "STRING"},
        {"name": "from_landing", "type": "STRING"},
        {"name": "order_id", "type": "STRING"},
        {"name": "notes", "type": "STRING"},
        {"name": "customer_notes", "type": "STRING"},
        {"name": "customer_adress", "type": "STRING"},
        {"name": "customer_actions", "type": "STRING"},
        {"name": "customer_agents", "type": "STRING"},
        {"name": "smart_tags", "type": "STRING"},
        {"name": "ipaddress", "type": "STRING"},
        {"name": "ticket_id", "type": "NUMERIC"},
        {"name": "created_at", "type": "TIMESTAMP"},
        {"name": "updated_at", "type": "TIMESTAMP"},
    ],
)
