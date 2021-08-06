import os
import json
import base64

import requests

from models import MySQL
from broadcast import broadcast

def main(request):
    request_json = request.get_json()
    message = request_json["message"]
    data_bytes = message["data"]
    data = json.loads(base64.b64decode(data_bytes).decode("utf-8"))
    print(data)

    if "broadcast" in data:
        results = broadcast(data)
    elif "table" in data:
        job = MySQL.factory(data["table"])
        results = job.run()

    responses = {
        "pipelines": "MySQL",
        "results": results,
    }

    print(responses)
    requests.post(
        "https://api.telegram.org/bot{token}/sendMessage".format(
            token=os.getenv("TELEGRAM_TOKEN")
        ),
        json={
            "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
            "text": json.dumps(responses, indent=4),
        },
    )
    return responses
