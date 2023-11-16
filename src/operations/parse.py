"""Parse Operation module"""
# External Libraries
import json

from datetime import datetime
from dateutil import relativedelta

# Custom Libraries & Modules
from src.classes.parser import CalendarParser, GradesParser
from src.classes.operation import Operation
from src.classes.logger import Logger
from src.classes.course import Course

from src import util


class CalendarParseOperation(Operation):
    """Parse Operation used to retrieve the courses from the HTML"""

    def __init__(self):
        super().__init__("PARSE")

    def validate(self, data) -> bool:
        if not isinstance(data, dict):
            return False

        if not all(map(util.all_str, data)):
            return False

        return True

    def save_data(self, data, path: str):
        with open(f"{path}.json", "w", encoding="utf-8") as f:
            courses = {
                project: list(map(lambda c: c.as_supabase_dict(), data[project]))
                for project in data
            }

            json.dump(courses, f, indent=2)

    @staticmethod
    def retrieve_data(path: str):
        """Given a filename (path) retrieve its content and transform it into courses"""
        project_courses = {}

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

            for project in data:
                project_courses[project] = list(map(Course.from_dict, data[project]))

        return project_courses

    def execute(self, data, _logger: Logger):
        today_date = datetime.today()
        next_month_date = today_date + relativedelta.relativedelta(months=1)

        parser = CalendarParser()

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


class GradesParseOperation(Operation):
    """Parse Operation used to retrieve the grades from the HTML"""

    def __init__(self):
        super().__init__("PARSE")

    def validate(self, data) -> bool:
        if not isinstance(data, str):
            return False

        return True

    def save_data(self, data, path: str):
        with open(f"{path}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def retrieve_data(path: str):
        """Given a filename (path) retrieve its content"""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def execute(self, data, _logger: Logger):
        parser = GradesParser()
        return parser.parse(data)
