from datetime import datetime

from scrapper import scraper
from parser import parser

from constants.main import PROJECTS

import time
import json
import sys
import re
import os


def slugify(txt):
    return re.sub("-|:| ", "_", txt)


def get_datetime_filename(filename, ext):
    now = str(datetime.now())
    dt = slugify(now.split(".")[0])
    return f"{filename}_{dt}.{ext}"


def main():
    now = str(datetime.now())
    dt = slugify(now.split(".")[0])

    directory = f"logs/{dt}"
    if not os.path.exists(directory):
        # If it doesn't exist, create it
        os.makedirs(directory)

    driver = scraper.setup_session()

    projects = list(PROJECTS.keys())

    projects_courses = {}

    for project in projects:
        start = time.time()
        agenda = scraper.scrape(driver, project)
        html = agenda.get_attribute("innerHTML")
        courses = parser.parse(html)

        projects_courses[project] = courses

        msg = f"[DEBUG] Found a total of {len(courses)} courses for the '{project}' project."
        print(msg)

        filename = slugify(project) + ".json"

        with open(f"{directory}/{filename}", "w") as file:
            file.write(json.dumps(courses, indent=2))
            end = time.time()
            duration = end - start
            print(
                f"[DEBUG] Save the content of the course into the {filename} file. (Took {duration}s)\n"
            )

    driver.close()


if __name__ == "__main__":
    main()
