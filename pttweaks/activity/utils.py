from datetime import datetime


UTC_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def utc_to_str(datetime_value):
    return datetime_value.strftime(UTC_DATETIME_FORMAT)


def utc_from_str(datetime_str):
    if datetime_str:
        return datetime.strptime(datetime_str, UTC_DATETIME_FORMAT)


def strip_none(li):
    return [el for el in li if el is not None]
