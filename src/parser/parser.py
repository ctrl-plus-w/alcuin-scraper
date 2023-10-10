from bs4 import BeautifulSoup


import re


def is_location(str):
    return re.match("(^(amphi|Amphi).*)|((C|A|E)[0-9]+)", str) is not None


def get_course(course_table, date):
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
        if is_location(param):
            location = param
        elif location is None:
            professors.append(param)
        else:
            groups.append(param)

    if location is None:
        groups = professors
        professors = []

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

    course = {
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "professors": list(map(lambda p: p.replace("\xa0", " "), professors)),
        "groups": groups,
        "location": location,
        "date": date,
    }

    return course


def parse(html):
    soup = BeautifulSoup(html, features="html.parser")

    tbody = soup.select_one("tbody")

    rows = tbody.findChildren("tr", recursive=False)
    weeks = rows[2:]

    courses = []

    for week in weeks:
        cells = week.findChildren("td", recursive=False)
        days = cells[2:]

        for day in days:
            tables = day.findChildren("table", recursive=False)

            date_table = tables[0]
            courses_tables = tables[1:]

            date = int(date_table.get_text().strip())

            for course_table in courses_tables:
                course = get_course(course_table, date)
                courses.append(course)

    return courses
