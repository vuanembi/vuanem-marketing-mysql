from pipeline.pipeline_service import pipeline_service


def test_service():
    res = pipeline_service()
    assert res
