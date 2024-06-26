"""Utils module"""
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode
from datetime import datetime
from typing import Callable, Iterable, TypeVar, Any, Iterator, List

import re
import os
import pytz


def slugify(txt: str):
    """Slugify a string"""
    return re.sub("-|:| ", "_", txt)


def all_str(arr: list) -> bool:
    """Check if all the elements in the array are strings"""
    return all(map(lambda e: type(e) is str, arr))


def all_instance(arr: list, cls) -> bool:
    """Check if all the elements in the array are instances of the class passed in the second parameter"""
    return all(map(lambda e: isinstance(e, cls), arr))


def create_directory(directory: str):
    """Create a directory if it doesn't exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def is_in_past(date_str: str) -> bool:
    """Check whether or not the given date corresponding the the string is in the past or not"""
    date = datetime.fromisoformat(date_str)
    return date.timestamp() < datetime.now().timestamp()


def compare_dates_with_timezone(date_str1: str, date_str2: str):
    """Compare two dates as string with timezone (check if the dates are equals even if the timezones are differents)"""
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


def get_year(date):
    """Get the year value of a date"""
    year = ""
    date = str(date)
    parse = date.split("-")
    year = int(parse[0])
    return year


def get_month(date):
    """Get the month value of a date"""
    month = ""
    date = str(date)
    parse = date.split("-")
    month = int(parse[1])
    return month


def remove_quote(txt: str):
    """Remove all the quotes inside the string"""
    return txt.replace('"', "")


def capitalize(txt: str):
    """Capitalize a string"""
    return txt[0].upper() + txt[1:]


_T = TypeVar("_T")
_S = TypeVar("_S")


def _f(__function: Callable[[_T], Any], __iterable: Iterable[_T]) -> list[_T]:
    return list(filter(__function, __iterable))


def _m(__func: Callable[..., _S], *iterables: Iterable[Any]) -> list[_S]:
    return list(map(__func, *iterables))


def decrypt_password(encrypted_password: str, private_key: str) -> str:
    """Decrypt the password from the database given a secret key."""
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)

    encrypted_text = b64decode(encrypted_password)
    decrypted_data = cipher.decrypt(encrypted_text)

    return decrypted_data.decode('utf-8', errors='replace')
