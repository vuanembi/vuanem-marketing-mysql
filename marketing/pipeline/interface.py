from typing import Any, Callable
from dataclasses import dataclass


@dataclass
class Pipeline:
    table: str
    get: Callable[[str], list[dict[str, Any]]]
    sql: str
    transform: Callable[[list[dict[str, Any]]], list[dict[str, Any]]]
    schema: list[dict[str, Any]]
