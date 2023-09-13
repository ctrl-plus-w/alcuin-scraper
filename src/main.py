from datetime import datetime

from scrapper import scraper
from parser import parser

from constants.main import PROJECTS

import util

import time
import json
import sys
import re
import os


def get_projects_courses():
    # Retrieve the list of all the projects (aka classes) names
    projects = list(PROJECTS.keys())

    # Initialize the directory of the stored logs
    directory = f"logs/{util.slugify(str(datetime.now()).split('.')[0])}"
    util.create_directory(directory)

    # Initialize the selenium session (login to alcuin and switch to the agenda tab)
    driver = scraper.setup_session()

    projects_courses = {}

    # Loop through every project
    for project in projects:
        start = time.time()

        # Scrape the agenda frame, retrieve the html and parse it to get the courses
        agenda = scraper.scrape(driver, project)
        html = agenda.get_attribute("innerHTML")
        courses = parser.parse(html)

        # Map the project name to its courses
        projects_courses[project] = courses
        msg = f"[DEBUG] Found a total of {len(courses)} courses for the '{project}' project."
        print(msg)

        # Store the retrieved courses into a log folder
        filename = util.slugify(project) + ".json"
        with open(f"{directory}/{filename}", "w") as file:
            file.write(json.dumps(courses, indent=2))

            end = time.time()
            duration = end - start

            msg = f"[DEBUG] Save the content of the course into the {filename} file. (Took {duration}s)\n"
            print(msg)

    driver.close()
    return projects_courses


def main():
    projects_courses = get_projects_courses()


if __name__ == "__main__":
    main()
