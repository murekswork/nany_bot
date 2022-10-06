import datetime


def datetime_to_str(date: datetime.datetime) -> str:
    return datetime.datetime.strftime(date, "%d.%m.%Y")
