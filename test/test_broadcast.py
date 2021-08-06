from .utils import process_broadcast


def test_broadcast():
    data = {"broadcast": "standard"}
    process_broadcast(data)
