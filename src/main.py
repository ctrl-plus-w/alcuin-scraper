from datetime import datetime

from scrapper import scraper
from parser import parser
from scrap_to_ics import scrap_to_ics
from uploader import upload

from constants.main import PROJECTS

import util

import enlighten
import logging
import time
import json
import sys
import re
import os


def get_projects_courses(logger: logging.Logger):
    # Retrieve the list of all the projects (aka classes) names
    projects = list(PROJECTS.keys())

    # Progress bar
    setup_pbar_manager = enlighten.get_manager()
    setup_pbar = setup_pbar_manager.counter(total=8, desc="Setup")
    setup_pbar.update()

    courses_pbar_manager = enlighten.get_manager()
    courses_pbar = courses_pbar_manager.counter(
        total=(len(projects) * 3), desc="Progress"
    )

    # Initialize the directory of the stored logs
    directory = f"logs/{util.slugify(str(datetime.now()).split('.')[0])}"
    util.create_directory(directory)

    # Initialize the selenium session (login to alcuin and switch to the agenda tab)
    driver = scraper.setup_session(setup_pbar, logger)

    projects_courses = {}

    # Loop through every project (for the current month)
    for project in projects:
        start = time.time()

        # Scrape the agenda frame, retrieve the html and parse it to get the courses
        agenda = scraper.scrape(driver, project)
        html = agenda.get_attribute("innerHTML")
        courses = parser.parse(html)

        # Map the project name to its courses
        projects_courses[project] = courses

        end = time.time()
        duration = end - start

        logger.info(
            f"[{project}]({round(duration)}s) Retrieved the current month courses. Found {len(courses)} courses."
        )
        courses_pbar.update()

    scraper.set_next_month(driver)

    # # Loop through every project (for the next month)
    for project in projects:
        start = time.time()

        # Scrape the agenda frame, retrieve the html and parse it to get the courses
        agenda = scraper.scrape(driver, project)
        html = agenda.get_attribute("innerHTML")
        courses = parser.parse(html)

        # Map the project name to its courses
        projects_courses[project] += courses

        end = time.time()
        duration = end - start

        logger.info(
            f"[{project}]({round(duration)}s) Retrieved the next month courses. Found {len(courses)} courses."
        )
        courses_pbar.update()

    for project in projects:
        calendar = scrap_to_ics.create_events(courses)

        # Store the retrieved courses into a log folder
        filename = util.slugify(project) + ".json"
        with open(f"{directory}/{filename}", "w") as file:
            file.write(json.dumps(courses, indent=2))

        filename = util.slugify(project) + ".ics"
        with open(f"{directory}/{filename}", "wb") as file:
            file.write(calendar.to_ical())

        end = time.time()
        duration = end - start

        logger.info(
            f"[{project}]({round(duration)}s) Saved the file. Found {len(courses)} courses."
        )
        courses_pbar.update()

    driver.close()
    return projects_courses


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    skip_scrape = len(sys.argv) > 1 and "--skip-scrape" in sys.argv

    if not skip_scrape:
        get_projects_courses(logger)

    upload.upload_last_calendars(logger)


if __name__ == "__main__":
    main()
