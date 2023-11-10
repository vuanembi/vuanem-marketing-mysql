from typing import Union

from compose import compose

from db.bigquery import load
from db.mysql import get
from pipeline.pipeline_const import SalesCall3, ZNS, ZNS_FOLLOW, ZNS_FOLLOW_STORE


def pipeline_service() -> dict[str, Union[str, int]]:
    results = [
        compose(
            lambda rows: load(rows, pipeline.name, pipeline.schema),
            lambda: [pipeline.transform(row) for row in get(pipeline.query)],
        )()
        for pipeline in [SalesCall3, ZNS, ZNS_FOLLOW, ZNS_FOLLOW_STORE]
    ]

    return {"results": results}
