from typing import TypedDict, Callable
from datetime import datetime

from sqlalchemy.engine import Engine
import pytz


class IMySQLTable(TypedDict):
    name: str
    engine: Engine
    query: str
    transform: Callable[[list[dict]], list[dict]]
    schema: list[dict]


def transform_timestamp(x: datetime) -> str:
    return pytz.timezone("Asia/Saigon").localize(x).isoformat(timespec="seconds")
