"""Parser module"""
import re

from bs4 import BeautifulSoup, Tag


# External Librarie & Modules
from src.classes.course import Course

from src import util


class CalendarParser:
    """Parser class used to parse a calendar"""

    def is_location(self, txt: str):
        """Check if the string represents a location"""
        return re.match("(^(amphi|Amphi).*)|((C|A|E)[0-9]+)", txt) is not None

    def get_course(self, course_table, date):
        """Get the course from the course_table html"""
        params = []

        for br_tag in course_table.find_all("br"):
            br_tag.decompose()

        for font_tag in course_table.find_all("font"):
            params.append(font_tag.get_text())
            font_tag.decompose()

        professors = []
        groups = []
        location = None

        for param in params[1:]:
            if self.is_location(param):
                location = param
            elif location is None:
                professors.append(param)
            else:
                groups.append(param)

        if location is None:
            groups = professors[1:]
            professors = professors[:1]

        first_title_part = course_table.get_text().split(";")[0]
        title = re.sub(" +|\n +", " ", first_title_part.strip())

        start_str_time, end_str_time = params.pop(0).split("-")
        start_str_hours, start_str_minutes = start_str_time.split("H")
        end_str_hours, end_str_minutes = end_str_time.split("H")

        start_time = {
            "hours": int(start_str_hours),
            "minutes": int(start_str_minutes),
        }

        end_time = {
            "hours": int(end_str_hours),
            "minutes": int(end_str_minutes),
        }

        professors = list(map(lambda p: p.replace("\xa0", " "), professors))

        return Course(title, start_time, end_time, professors, location, date)

    def parse(self, html):
        """Parse the calendar HTML"""
        soup = BeautifulSoup(html, features="html.parser")

        tbody = soup.select_one("tbody")

        rows = tbody.findChildren("tr", recursive=False)

        # Exclude the first row because it is the row showing the week days (Lundi, Mardi...)
        weeks = rows[1:]

        courses: list[Course] = []
        for week in weeks:
            cells = week.findChildren("td", recursive=False)

            # Exclude the first cell because it is the cell showing the week number
            days = cells[1:]

            for day in days:
                tables = day.findChildren("table", recursive=False)

                if len(tables) == 0:
                    continue

                date_table = tables[0]
                courses_tables = tables[1:]

                date = int(date_table.get_text().strip())
                for course_table in courses_tables:
                    try:
                        course = self.get_course(course_table, date)
                        courses.append(course)
                    except Exception as e:
                        print(e)
                        continue

        return courses


class GradesParser:
    """Parser class used to parse the grades table"""

    def parse_row(self, tag: Tag):
        """Parse a grades table row"""
        spaces_count = len(tag.select(".ygtvspacer"))

        cells = tag.select(".DataGridColumn")

        return {
            "spaces": spaces_count,
            "label": cells[0].text.strip(),
            "code": cells[1].text.strip(),
            "status": cells[2].text.strip(),
            "coef": cells[4].text.strip(),
            "mean": cells[5].text.strip(),
            "credits": cells[6].text.strip(),
            "grade": cells[7].text.strip(),
        }

    def parse(self, html: str):
        """Parse the grades HTML table"""
        soup = BeautifulSoup(html, features="html.parser")

        rows = soup.select(".DataGridItem")

        grades = []

        ue = None
        code_ue = None

        for html_row in rows:
            row = self.parse_row(html_row)

            if row["status"] == "En construction":
                ue = row["label"]
                code_ue = row["code"]
                continue

            grades.append({**row, "ue": ue, "code_ue": code_ue})

        return grades
