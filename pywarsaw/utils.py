import datetime
from collections.abc import MutableMapping


def flat_dict(d, parent_key="", sep="_", index=None):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if index is not None:
            new_key = "{}_{}".format(new_key, index)
        if isinstance(v, dict):
            items.extend(flat_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flat_dict(item, new_key, sep=sep, index=i).items())
                else:
                    items.append((new_key, item))
        else:
            items.append((new_key, v))
    return dict(items)


# Helpers for types converting


def to_datetime(f: str) -> datetime.datetime:
    return (
        datetime.datetime.strptime(f[:18], "%Y-%m-%d %H:%M:%S") if f is not None else f
    )


def to_datetime_with_12(f: str) -> datetime.datetime:
    return (
        datetime.datetime.strptime(f, "%d-%b-%y %H.%M.%S.%f %p") if f is not None else f
    )


def to_date(f: int) -> datetime.date:
    return datetime.datetime.strptime(str(f), "%Y%m%d").date() if f is not None else f


def to_time(f: str):
    return datetime.datetime.strptime(f, "%H:%M:%S").time() if f is not None else f


def comma_number_to_float(f: str) -> float:
    f = f.replace(",", ".")
    return float(f) if f.isdigit() else f
