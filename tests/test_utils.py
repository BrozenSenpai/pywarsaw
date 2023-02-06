import pytest
import datetime

from pywarsaw.utils import (
    flat_dict,
    to_date,
    to_datetime,
    to_datetime_with_12,
    to_time,
    comma_number_to_float,
)

flat_dict_data = [
    (
        [
            {
                "key_1": "value_1",
                "key_2": {
                    "nested_key_1": "nested_value_1",
                    "nested_key_2": "nested_value_2",
                },
                "key_3": {"nested_key_3": "nested_value_3"},
            },
        ],
        {
            "key_1": "value_1",
            "key_2_nested_key_1": "nested_value_1",
            "key_2_nested_key_2": "nested_value_2",
            "key_3_nested_key_3": "nested_value_3",
        },
    ),
    (
        [{"key_1": [{"nested_key": "nested_value"}, {"nested_key": "nested_value"}]}],
        {"key_1_nested_key_0": "nested_value", "key_1_nested_key_1": "nested_value"},
    ),
]


@pytest.mark.parametrize("args, result", flat_dict_data)
def test_flat_dict(args, result):
    assert flat_dict(*args) == result


def test_to_datetime():
    time_string = "2021-01-01 12:15:43953745"
    time_obj = datetime.datetime.strptime(time_string[:18], "%Y-%m-%d %H:%M:%S")
    assert to_datetime(time_string) == time_obj
    assert to_datetime(None) == None


def test_to_datetime_with_12():
    time_string = "01-APR-22 12.38.06.000000 PM"
    time_obj = datetime.datetime.strptime(time_string, "%d-%b-%y %H.%M.%S.%f %p")
    assert to_datetime_with_12(time_string) == time_obj
    assert to_datetime_with_12(None) == None


def test_to_date():
    time_int = 20221201
    time_obj = datetime.datetime.strptime(str(time_int), "%Y%m%d").date()
    assert to_date(time_int) == time_obj
    assert to_date(None) == None


def test_to_time():
    time_string = "12:12:12"
    time_obj = datetime.datetime.strptime(time_string, "%H:%M:%S").time()
    assert to_time(time_string) == time_obj
    assert to_time(None) == None


def comma_number_to_float():
    number_str = "21,15"
    assert comma_number_to_float(number_str) == 21.15
