from typing import Any, Callable
from dataclasses import dataclass

from marketing import connection


@dataclass
class Pipeline:
    table: str
    connection: connection.Connection
    sql: str
    transform: Callable[[list[dict[str, Any]]], list[dict[str, Any]]]
    schema: list[dict[str, Any]]
