import datetime

months = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа', 9: 'сентября',
    10: 'октября', 11: 'ноября', 12: 'декабря'
}


def format_hour_to_timestamp(hour: int, timestamp: int = 2):
    __hour = hour + timestamp
    if hour in [22, 23, 24]:
        __hour = (hour - 24) + timestamp
    return __hour


def dates_to_text(__datetime: datetime.datetime) -> str:
    date = '%s %s %s года в ' % (__datetime.day,
                                 months[__datetime.month],
                                 __datetime.year)
    time = '{:02}:{:02}'.format(format_hour_to_timestamp(__datetime.hour), __datetime.minute)
    __datetime = date + time
    return __datetime
