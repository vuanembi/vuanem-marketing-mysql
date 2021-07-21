import os
import json

import requests
from pexecute.thread import ThreadLoom

from models import MySQL


def main(request):
    """API Gateway

    Args:
        request (flask.Request): HTTP request

    Returns:
        dict: Responses
    """
        
    SalesCall = MySQL("c2l_SalesCall")
    CallLogs = MySQL("c2c_CaresoftCallLogs")
    loom = ThreadLoom(max_runner_cap=10)
    for i in [SalesCall, CallLogs]:
        loom.add_function(i.run)
    output = loom.execute()

    responses = {
        "pipelines": "MySQL",
        "results": [i["output"] for i in output.values()],
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
