from unittest.mock import Mock

import pytest

from main import main


@pytest.mark.parametrize(
    "table",
    [
        # "Orders",
        "SalesCall",
    ],
)
def test_pipelines(table):
    data = {
        "table": table,
    }
    res = main(Mock(get_json=Mock(return_value=data), args=data))["results"]
    assert res["num_processed"] >= 0
    if res["num_processed"] > 0:
        assert res["num_processed"] == res["output_rows"]
