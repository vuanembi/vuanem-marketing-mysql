from typing import Any
from google.cloud import bigquery

BQ_CLIENT = bigquery.Client()

DATASET = "IP_Ecommerce"


def load(table: str, schema: list[dict]):
    def _load(rows: list[dict[str, Any]]) -> int:
        return (
            BQ_CLIENT.load_table_from_json(
                rows,
                f"{DATASET}.{table}",
                job_config=bigquery.LoadJobConfig(
                    schema=schema,
                    create_disposition="CREATE_IF_NEEDED",
                    write_disposition="WRITE_TRUNCATE",
                ),
            )
            .result()
            .output_rows
        )

    return _load
