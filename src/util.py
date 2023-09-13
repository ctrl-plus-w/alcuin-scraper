from datetime import datetime

import re
import os


def slugify(txt):
    return re.sub("-|:| ", "_", txt)


def get_datetime_filename(filename, ext):
    now = str(datetime.now())
    dt = slugify(now.split(".")[0])
    return f"{filename}_{dt}.{ext}"


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
