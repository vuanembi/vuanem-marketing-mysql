import pytest

from marketing.pipeline import pipelines
from marketing.pipeline_service import pipeline_service


@pytest.mark.parametrize(
    "pipeline",
    pipelines,
    ids=[i.table for i in pipelines],
)
def test_service(pipeline):
    res = pipeline_service(pipeline)
    assert res["output_rows"] > 0
