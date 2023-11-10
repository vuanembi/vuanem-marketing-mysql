from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable
from zoneinfo import ZoneInfo


def transform_timestamp(value: datetime) -> str:
    tz = ZoneInfo("Asia/Ho_Chi_Minh")
    return value.replace(tzinfo=tz).isoformat(timespec="seconds") if value else None


@dataclass
class Pipeline:
    name: str
    query: str
    transform: Callable[[dict], dict]
    schema: list[Any]


SalesCall3 = Pipeline(
    name="SalesCall3",
    query="""
        select
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
        from
            salecalls
        """,
    transform=lambda row: {
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
    },
    schema=[
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

ZNS = Pipeline(
    name="ZNS",
    query="""
        select
            id,
            template_zns_id,
            phone,
            name,
            dateofbirth,
            email,
            status,
            created_at,
            updated_at
        from 
            zns
        """,
    transform=lambda row: {
        "id": row["id"],
        "template_zns_id": row["template_zns_id"],
        "phone": row["phone"],
        "name": row["name"],
        "dateofbirth": row["dateofbirth"],
        "email": row["email"],
        "status": row["status"],
        "created_at": transform_timestamp(row["created_at"]),
        "updated_at": transform_timestamp(row["updated_at"]),
    },
    schema=[
        {"name": "id", "type": "NUMERIC"},
        {"name": "template_zns_id", "type": "STRING"},
        {"name": "phone", "type": "STRING"},
        {"name": "name", "type": "STRING"},
        {"name": "dateofbirth", "type": "STRING"},
        {"name": "email", "type": "STRING"},
        {"name": "status", "type": "NUMERIC"},
        {"name": "created_at", "type": "TIMESTAMP"},
        {"name": "updated_at", "type": "TIMESTAMP"},
    ],
)

ZNS_FOLLOW_STORE = Pipeline(
    name="ZNSFollowStore",
    query="""
        select
            id,
            code,
            created_at,
            updated_at
        from 
            zns_follow_stores
        """,
    transform=lambda row: {
        "id": row["id"],
        "code": row["code"],
        "created_at": transform_timestamp(row["created_at"]),
        "updated_at": transform_timestamp(row["updated_at"]),
    },
    schema=[
        {"name": "id", "type": "NUMERIC"},
        {"name": "code", "type": "STRING"},
        {"name": "created_at", "type": "TIMESTAMP"},
        {"name": "updated_at", "type": "TIMESTAMP"},
    ],
)

ZNS_FOLLOW = Pipeline(
    name="ZNSFollow",
    query="""
        select
            id,
            phone_no,
            user_id,
            username,
            user_text,
            voucher,
            created_at,
            updated_at
        from 
            zns_follows
        """,
    transform=lambda row: {
        "id": row["id"],
        "phone_no": row["phone_no"],
        "user_id": row["user_id"],
        "username": row["username"],
        "user_text": row["user_text"],
        "voucher": row["voucher"],
        "created_at": transform_timestamp(row["created_at"]),
        "updated_at": transform_timestamp(row["updated_at"]),
    },
    schema=[
        {"name": "id", "type": "NUMERIC"},
        {"name": "phone_no", "type": "STRING"},
        {"name": "user_id", "type": "STRING"},
        {"name": "username", "type": "STRING"},
        {"name": "user_text", "type": "STRING"},
        {"name": "voucher", "type": "STRING"},
        {"name": "created_at", "type": "TIMESTAMP"},
        {"name": "updated_at", "type": "TIMESTAMP"},
    ],
)
