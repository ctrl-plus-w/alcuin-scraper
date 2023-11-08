# External Libraries
from datetime import datetime
from dateutil import relativedelta

import json

# Custom Libraries & Modules
from classes.Operation import Operation
from classes.Scraper import Scraper
from classes.Parser import Parser
from classes.Logger import Logger
from classes.Course import Course

import util


class ParseOperation(Operation):
    def __init__(self):
        super().__init__("PARSE")

    def validate(self, data) -> bool:
        if not type(data) is dict:
            return False

        if not all(map(lambda e: util.all_str(e), data)):
            return False

        return True

    def save_data(self, data, path: str):
        with open(f"{path}.json", "w") as f:
            courses = {
                project: list(map(lambda c: c.as_supabase_dict(), data[project]))
                for project in data
            }

            json.dump(courses, f, indent=2)

    @staticmethod
    def retrieve_data(path: str):
        project_courses = {}
        with open(path) as f:
            data = json.load(f)

            for project in data:
                project_courses[project] = list(
                    map(
                        lambda course: Course.from_dict(course),
                        data[project],
                    )
                )

        return project_courses

    def execute(self, data, logger: Logger):
        today_date = datetime.today()
        next_month_date = today_date + relativedelta.relativedelta(months=1)

        parser = Parser()

        projects_courses = {}

        for project in data:
            curr_month_courses = parser.parse(data[project][0])
            next_month_courses = parser.parse(data[project][1])

            Course.set_month(curr_month_courses, util.get_month(today_date))
            Course.set_year(curr_month_courses, util.get_year(today_date))

            Course.set_month(next_month_courses, util.get_month(next_month_date))
            Course.set_year(next_month_courses, util.get_year(next_month_date))

            Course.set_group(curr_month_courses, project)
            Course.set_group(next_month_courses, project)

            projects_courses[project] = curr_month_courses + next_month_courses

        return projects_courses
