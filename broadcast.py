import os
import json

from google.cloud import pubsub_v1

TABLES = [i.replace('.json', '') for i in os.listdir('configs')]

def broadcast(broadcast_data):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(os.getenv("PROJECT_ID"), os.getenv("TOPIC_ID"))

    for table in TABLES:
        data = {
            "table": table
        }
        message_json = json.dumps(data)
        message_bytes = message_json.encode("utf-8")
        publisher.publish(topic_path, data=message_bytes).result()

    return len(TABLES)
