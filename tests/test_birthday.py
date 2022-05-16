from datetime import date

import pytest
from freezegun import freeze_time

from birthday_service.birthday import BirthdayInFutureError, next_birthday


@freeze_time("2022-05-15 12:00")
def test_next_birthday_same_year():
    dob = date(2020, 6, 1)
    expected = date(2022, 6, 1)
    actual = next_birthday(dob)
    assert actual == expected, f"Expected {expected}, got {actual}"


@freeze_time("2022-05-15 12:00")
def test_next_birthday_next_year():
    dob = date(2020, 4, 1)
    expected = date(2023, 4, 1)
    actual = next_birthday(dob)
    assert actual == expected, f"Expected {expected}, got {actual}"


@freeze_time("2022-05-15 12:00")
def test_next_birthday_same_day():
    dob = date(2020, 5, 15)
    expected = date.today()
    actual = next_birthday(dob)
    assert actual == expected, f"Expected {expected}, got {actual}"


@freeze_time("2022-05-15 12:00")
def test_next_birthday_in_future():
    dob = date(2022, 5, 16)
    with pytest.raises(BirthdayInFutureError):
        next_birthday(dob)


@freeze_time("2022-05-15 12:00")
def test_next_birthday_includes_leap_year():
    dob = date(2020, 1, 15)
    expected = date(2023, 1, 15)
    actual = next_birthday(dob)
    assert actual == expected, f"Expected {expected}, got {actual}"


@freeze_time("2022-05-15 12:00")
def test_next_birthday_for_leapyear_birthday():
    dob = date(2020, 2, 29)
    # In the UK, the legal birthday is on 1st March on non-leap years:
    expected = date(2023, 3, 1)
    actual = next_birthday(dob)
    assert actual == expected, f"Expected {expected}, got {actual}"


@freeze_time("2024-02-01 12:00")
def test_next_birthday_for_leapyear_birthday_on_leapyear():
    dob = date(2020, 2, 29)
    expected = date(2024, 2, 29)
    actual = next_birthday(dob)
    assert actual == expected, f"Expected {expected}, got {actual}"
