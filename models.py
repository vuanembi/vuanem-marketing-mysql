import os
import json
from urllib.parse import quote
from abc import ABC

import pytz
import sqlalchemy as sa
from google.cloud import bigquery

TZ = pytz.timezone("Asia/Saigon")

DATASET = "Ecom"

BQ_CLIENT = bigquery.Client()


class Cursor(ABC):
    def get_cursor(self, uid, pwd, host, db):
        engine = sa.create_engine(f"mysql+pymysql://{uid}:{pwd}@{host}/{db}")
        return engine.raw_connection().cursor()


class MagentoCursor(Cursor):
    def get_cursor(self):
        return super().get_cursor(
            quote(os.getenv("M_MYSQL_UID")),
            quote(os.getenv("M_MYSQL_PWD")),
            quote(os.getenv("M_MYSQL_HOST")),
            quote(os.getenv("M_MYSQL_DB")),
        )


class LaravelCursor(Cursor):
    def get_cursor(self):
        return super().get_cursor(
            quote(os.getenv("L_MYSQL_UID")),
            quote(os.getenv("L_MYSQL_PWD")),
            quote(os.getenv("L_MYSQL_HOST")),
            quote(os.getenv("L_MYSQL_DB")),
        )


class MySQL(ABC):
    def __init__(self):
        self.query, self.fields, self.schema = self.get_config()

    @staticmethod
    def factory(table):
        if table == "SalesCall":
            return SalesCall()
        elif table == "CallLogs":
            return CallLogs()
        elif table == "Orders":
            return Orders()
        else:
            raise NotImplementedError(table)

    def get_config(self):
        with open(f"configs/{self.table}.json", "r") as c, open(
            f"queries/{self.table}.sql"
        ) as q:
            config = json.load(c)
            query = q.read()
        return query, config["fields"], config["schema"]

    def get(self, cursor):
        cursor.execute(self.query)
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, result)) for result in cursor.fetchall()]
        return rows

    def transform(self, _rows):
        rows = [self._transform_type(row) for row in _rows]
        return rows

    def _transform_type(self, row):
        if self.fields.get("timestamp"):
            for i in self.fields["timestamp"]:
                row[i] = TZ.localize(row[i]).isoformat(timespec="seconds")
        return row

    def load(self, rows):
        return BQ_CLIENT.load_table_from_json(
            rows,
            f"{DATASET}.{self.table}",
            job_config=bigquery.LoadJobConfig(
                schema=self.schema,
                create_disposition="CREATE_IF_NEEDED",
                write_disposition="WRITE_TRUNCATE",
            ),
        ).result()

    def run(self):
        cursor = self.cursor.get_cursor()
        rows = self.get(cursor)
        responses = {
            "table": self.table,
            "num_processed": len(rows),
        }
        if len(rows) > 0:
            rows = self.transform(rows)
            loads = self.load(rows)
            responses["output_rows"] = loads.output_rows
        return responses


class SalesCall(MySQL):
    table = "SalesCall"

    def __init__(self):
        super().__init__()
        self.cursor = MagentoCursor()


class CallLogs(MySQL):
    table = "CallLogs"

    def __init__(self):
        super().__init__()
        self.cursor = MagentoCursor()


class Orders(MySQL):
    table = "Orders"

    def __init__(self):
        super().__init__()
        self.cursor = LaravelCursor()
