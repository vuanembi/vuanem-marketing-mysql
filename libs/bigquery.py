from google.cloud import bigquery


def load(
    client: bigquery.Client,
    dataset: str,
    table: str,
    schema: list[dict],
    rows: list[dict],
) -> int:
    return (
        client.load_table_from_json(
            rows,
            f"{dataset}.{table}",
            job_config=bigquery.LoadJobConfig(
                schema=schema,
                create_disposition="CREATE_IF_NEEDED",
                write_disposition="WRITE_TRUNCATE",
            ),
        )
        .result()
        .output_rows
    )
