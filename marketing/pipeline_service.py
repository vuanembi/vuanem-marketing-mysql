from typing import Union
from compose import compose

from marketing.pipeline.interface import Pipeline
from db.mysql import get
from db.bigquery import load


def pipeline_service(pipeline: Pipeline) -> dict[str, Union[str, int]]:
    return compose(
        lambda x: {"table": pipeline.table, "output_rows": x},
        load(pipeline.table, pipeline.schema),
        pipeline.transform,
        get(pipeline.connection),
    )(pipeline.sql)
