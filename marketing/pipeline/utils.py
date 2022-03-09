from datetime import datetime

import pytz


def transform_timestamp(x: datetime) -> str:
    return pytz.timezone("Asia/Saigon").localize(x).isoformat(timespec="seconds")
