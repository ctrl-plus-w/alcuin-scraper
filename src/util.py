from datetime import datetime

import re
import os
import pytz


def slugify(txt):
    return re.sub("-|:| ", "_", txt)


def get_datetime_filename(filename, ext):
    now = str(datetime.now())
    dt = slugify(now.split(".")[0])
    return f"{filename}_{dt}.{ext}"


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def compare_dates_with_timezone(date_str1, date_str2):
    # Parse the date strings into datetime objects
    date1 = datetime.fromisoformat(date_str1).astimezone(pytz.utc)
    date2 = datetime.fromisoformat(date_str2).astimezone(pytz.utc)

    # Compare the year, month, day, hour, and minute, while considering timezones
    return (
        date1.year == date2.year
        and date1.month == date2.month
        and date1.day == date2.day
        and date1.hour == date2.hour
        and date1.minute == date2.minute
        and date1.utcoffset() == date2.utcoffset()
    )
