import datetime
import time
from utils.dates_processing import dates_to_text


def now_unix_time():
    return int(time.time())


def get_datetime(unix_time: int, __format: bool = True):
    __datetime = datetime.datetime.fromtimestamp(unix_time)

    if __format:
        return dates_to_text(__datetime)
    return __datetime
