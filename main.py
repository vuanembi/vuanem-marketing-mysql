from typing import Union

from marketing.pipeline_controller import pipeline_controller


def main(request) -> list[dict[str, Union[str, int]]]:
    return pipeline_controller()
