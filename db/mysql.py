from typing import Any

import pymysql.cursors

from marketing import connection


def get(connection: connection.Connection):
    def _get(query: str) -> list[dict[str, Any]]:
        with pymysql.connect(
            host=connection.host,
            user=connection.user,
            password=connection.password,
            cursorclass=pymysql.cursors.DictCursor,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    return _get
