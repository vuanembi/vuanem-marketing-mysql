import os
import json

import requests
from google.cloud import bigquery

from controller.pipelines import factory, run

BQ_CLIENT = bigquery.Client()
DATASET = "IP_Ecommerce"


def main(request) -> dict:
    data = request.get_json()
    print(data)

    if "table" in data:
        response = {
            "pipelines": "EcommerceMySQL",
            "results": run(BQ_CLIENT, factory(data["table"]), DATASET),
        }
        print(response)
        requests.post(
            f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage",
            json={
                "chat_id": "-465061044",
                "text": json.dumps(response, indent=4),
            },
        )
        return response
    else:
        raise ValueError(data)
