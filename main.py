from typing import Union

from pipeline.pipeline_service import pipeline_service


def main(request) -> dict[str, Union[str, int]]:
    return pipeline_service()
