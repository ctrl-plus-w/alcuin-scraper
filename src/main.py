from datetime import datetime
from dateutil import relativedelta

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


def get_projects_courses(directory, logger: logging.Logger):
    # Retrieve the list of all the projects (aka classes) names
    projects = list(PROJECTS.keys())

    # Progress bar
    setup_pbar_manager = enlighten.get_manager()
    setup_pbar = setup_pbar_manager.counter(total=8, desc="Setup")
    setup_pbar.update()

    courses_pbar_manager = enlighten.get_manager()
    courses_pbar = courses_pbar_manager.counter(
        total=(len(projects) * 2), desc="Progress"
    )

    # Initialize the selenium session (login to alcuin and switch to the agenda tab)
    driver = scraper.setup_session(setup_pbar, logger)

    curr_month_projects_courses = {}
    next_month_projects_courses = {}

    # Initialize the project courses
    for project in projects:
        curr_month_projects_courses[project] = []

    # Loop through every project (for the current month)
    for project in projects:
        start = time.time()

        # Scrape the agenda frame, retrieve the html and parse it to get the courses
        agenda = scraper.scrape(driver, project)
        html = agenda.get_attribute("innerHTML")
        courses = parser.parse(html)

        # Map the project name to its courses
        curr_month_projects_courses[project] = courses

        end = time.time()
        duration = end - start

        logger.info(
            f"[{project}]({round(duration)}s) Retrieved the current month courses. Found {len(courses)} courses."
        )
        courses_pbar.update()

    scraper.set_next_month(driver)

    # Loop through every project (for the next month)
    for project in projects:
        start = time.time()

        # Scrape the agenda frame, retrieve the html and parse it to get the courses
        agenda = scraper.scrape(driver, project)
        html = agenda.get_attribute("innerHTML")
        courses = parser.parse(html)

        # Map the project name to its courses
        next_month_projects_courses[project] = courses

        end = time.time()
        duration = end - start

        logger.info(
            f"[{project}]({round(duration)}s) Retrieved the next month courses. Found {len(courses)} courses."
        )
        courses_pbar.update()

    for project in projects:
        curr_month_courses = curr_month_projects_courses[project]
        next_month_courses = next_month_projects_courses[project]

        calendar = scrap_to_ics.create_calendar()

        today_date = datetime.today()
        next_month_date = today_date + relativedelta.relativedelta(months=1)

        def set_month_and_year(month, year):
            def core(event):
                _event = event.copy()
                _event["month"] = month
                _event["year"] = year
                return _event

            return core

        month = scrap_to_ics.get_month(today_date)
        year = scrap_to_ics.get_year(today_date)

        for event in scrap_to_ics.create_events(curr_month_courses, month, year):
            calendar.add_component(event)

        next_month = scrap_to_ics.get_month(next_month_date)
        next_year = scrap_to_ics.get_year(next_month_date)

        for event in scrap_to_ics.create_events(
            next_month_courses, next_month, next_year
        ):
            calendar.add_component(event)

        merged_courses = list(
            map(set_month_and_year(month, year), curr_month_courses)
        ) + list(map(set_month_and_year(next_month, next_year), next_month_courses))

        # Store the retrieved courses into a log folder
        filename = util.slugify(project) + ".json"
        with open(f"{directory}/{filename}", "w") as file:
            file.write(json.dumps(merged_courses, indent=2))

        filename = util.slugify(project) + ".ics"
        with open(f"{directory}/{filename}", "wb") as file:
            file.write(calendar.to_ical())

        end = time.time()
        duration = end - start

        logger.info(
            f"[{project}]({round(duration)}s) Saved the file. Found {len(curr_month_courses)} courses."
        )

    driver.close()
    return curr_month_projects_courses


def main():
    # Initialize the directory of the stored logs
    directory = f"logs/{util.slugify(str(datetime.now()).split('.')[0])}"
    util.create_directory(directory)

    logs_filename = f"{directory}/logs.txt"

    logging.basicConfig(level=logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    logger = logging.getLogger("mylogger")

    log_file_handler = logging.FileHandler(logs_filename)
    log_file_handler.setFormatter(formatter)

    logger.addHandler(log_file_handler)

    skip_scrape = len(sys.argv) > 1 and "--skip-scrape" in sys.argv

    try:
        if not skip_scrape:
            get_projects_courses(directory, logger)

        upload.upload_supabase_last_calendar()
        upload.upload_git_last_calendar()
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
