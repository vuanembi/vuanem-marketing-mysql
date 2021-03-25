import requests
from main import main

def test_requests():
    response = main({})
    print(response)
    for i in response.get("results"):
        assert i["num_processed"] > 0
        assert i["output_rows"] > 0
        assert i["errors"] is None
