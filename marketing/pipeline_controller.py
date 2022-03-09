from typing import Union

from marketing.pipeline import pipelines
from marketing.pipeline_service import pipeline_service


def pipeline_controller() -> list[dict[str, Union[str, int]]]:
    return [pipeline_service(p) for p in pipelines]
