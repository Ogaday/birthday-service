from datetime import date, timedelta

from dateutil.relativedelta import relativedelta


class BirthdayInFutureError(Exception):
    """
    Raised when the birthday is in the future.
    """


def next_birthday(dob: date) -> date:
    """
    Calculate the next birthday date on or after the current date, given date of birth.

    Raises BirthdayInFutureError if the date of birth after the current date.
    """
    today = date.today()

    if dob > today:
        raise BirthdayInFutureError()

    diff = relativedelta(today, dob)
    if diff.months == diff.days == 0:
        # Today is the birthday:
        next_ = today
    else:
        # Round up to birthday next year:
        next_ = dob + relativedelta(years=diff.years + 1)

    # Check for leap year birthdays:
    if dob.month == 2 and dob.day == 29:
        if next_.day == 28:
            next_ += timedelta(days=1)

    return next_
