import os
import json
from datetime import datetime

import requests
import sqlalchemy as sa
from tqdm import tqdm
from google.cloud import bigquery
from pexecute.thread import ThreadLoom


class MySQLJob:
    def __init__(self, table, **kwargs):
        self.table = table
        self.date_cols = kwargs.get("date_cols", None)
        self.timestamp_cols = kwargs.get("timestamp_cols", None)
        self.dataset = "Ecom"

    def connect_mysql(self):
        engine = sa.create_engine(
            "mysql+pymysql://{uid}:{pwd}@{host}/{db}".format(
                uid=os.getenv("MYSQL_UID"),
                pwd=os.getenv("MYSQL_PWD"),
                host=os.getenv("MYSQL_SERVER"),
                db=os.getenv('MYSQL_DB')
            )
        )
        return engine.raw_connection()

    def extract(self):
        cnxn = self.connect_mysql()
        cursor = cnxn.cursor()
        with open(f"queries/{self.table}.sql") as f:
            query = f.read()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, result)) for result in tqdm(cursor.fetchall())]
        self.num_processed = len(rows)
        return rows

    def transform(self, rows):
        for row in tqdm(rows):
            if self.date_cols:
                for col in self.date_cols:
                    row[col] = row[col].strftime("%Y-%m-%d")
            if self.timestamp_cols:
                for col in self.timestamp_cols:
                    row[col] = row[col].strftime("%Y-%m-%d %H:%M:%S")
        return rows

    def load(self, rows):
        with open(f"schemas/{self.table}.json") as f:
            schema = json.load(f)
        client = bigquery.Client()

        return client.load_table_from_json(
            rows,
            f"{self.dataset}._stage_{self.table}",
            job_config=bigquery.LoadJobConfig(
                schema=schema,
                create_disposition="CREATE_IF_NEEDED",
                write_disposition="WRITE_TRUNCATE",
            ),
        ).result()

    def run(self):
        rows = self.extract()
        rows = self.transform(rows)
        errors = self.load(rows)
        return {
            "table": self.table,
            "num_processed": self.num_processed,
            "output_rows": errors.output_rows,
            "errors": errors.errors,
        }


def main(request):
    SalesCall = MySQLJob("SalesCall", timestamp_cols=["dt"])
    CallLogs = MySQLJob(
        "CallLogs",
        timestamp_cols=["start_time", "end_time", "created_at", "updated_at"],
    )

    loom = ThreadLoom(max_runner_cap=10)
    for i in [SalesCall, CallLogs]:
        loom.add_function(i.run)
    results = loom.execute()

    responses = {
        "pipelines": "MySQL",
        "results": [i["output"] for i in results.values()],
    }

    print(responses)

    _ = requests.post(
        "https://api.telegram.org/bot{token}/sendMessage".format(
            token=os.getenv("TELEGRAM_TOKEN")
        ),
        json={
            "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
            "text": json.dumps(responses, indent=4),
        },
    )
    return responses
