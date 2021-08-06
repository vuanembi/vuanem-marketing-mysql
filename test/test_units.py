from .utils import process


def test_salescall():
    data = {
        "table": "SalesCall",
    }
    process(data)


def test_calllogs():
    data = {
        "table": "CallLogs",
    }
    process(data)


def test_orders():
    data = {
        "table": "Orders",
    }
    process(data)
