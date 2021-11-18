import importlib

from google.cloud import bigquery

from models.Ecommerce.base import IMySQLTable
from libs.mysql import get
from libs.bigquery import load


def factory(table: str) -> IMySQLTable:
    try:
        module = importlib.import_module(f"models.Ecommerce.{table}")
        return getattr(module, table)
    except (ImportError, AttributeError):
        raise ValueError(table)


def run(client: bigquery.Client, model: IMySQLTable, dataset: str) -> dict:
    data = get(model["engine"], model["query"])
    responses = {
        "table": model["name"],
        "num_processed": len(data),
    }
    if len(data) > 0:
        responses["output_rows"] = load(
            client,
            dataset,
            model["name"],
            model["schema"],
            model["transform"](data),
        )
    return responses
