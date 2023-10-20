from os import listdir, path
from datetime import datetime, timezone

from uploader import git
from uploader import supabase_instance

import util

import json
import enlighten
import pytz
import logging


def get_last_dir(dirs):
    # TODO : Explain why that value_of function (filename comes from the datetime.now() func / used to sort)
    dirs = list(filter(lambda dir: not "." in dir, dirs))
    value_of = lambda name: int(name.replace("_", ""))

    curr = dirs[0]
    value = value_of(curr)

    for directory in dirs:
        if value_of(directory) > value:
            curr = directory
            value = value_of(curr)

    return curr


def get_uploaded_group_courses(group):
    request = supabase_instance.client.table("courses").select("*").eq("group", group)
    response = request.execute()

    return response.data


def find_course_index(courses, course):
    for i, _course in enumerate(courses):
        if util.compare_dates_with_timezone(
            course["start_datetime"], _course["start_datetime"]
        ) and util.compare_dates_with_timezone(
            course["end_datetime"], _course["end_datetime"]
        ):
            return i

    return -1


def get_groups_courses():
    basepath = "logs"

    # Retrieve the last dir of scraped pages
    files = listdir(basepath)
    last_dir = get_last_dir(files)

    # Get the filenames of the calendars
    ics_filter = lambda n: n.endswith(".json")
    calendars = list(filter(ics_filter, listdir(path.join(basepath, last_dir))))

    group_courses = {}

    for calendar in calendars:
        calendar_file = open(path.join(basepath, last_dir, calendar))
        json_courses = json.loads(calendar_file.read())

        for json_course in json_courses:
            year = json_course["year"]
            month = json_course["month"]
            day = json_course["date"]

            sth = json_course["start_time"]["hours"]
            stm = json_course["start_time"]["minutes"]

            eth = json_course["end_time"]["hours"]
            etm = json_course["end_time"]["minutes"]

            start_date = (
                datetime(year, month, day, sth, stm, 0).strftime("%Y-%m-%dT%H:%M:%S.%f")
                + "+02"
            )

            end_date = (
                datetime(year, month, day, eth, etm, 0).strftime("%Y-%m-%dT%H:%M:%S.%f")
                + "+02"
            )

            group = calendar.split(".")[0]

            course = {
                "title": json_course["title"],
                "description": "",
                "start_datetime": start_date,
                "end_datetime": end_date,
                "group": group,
                "professors": json_course["professors"],
                "location": json_course["location"],
            }

            if group in group_courses:
                group_courses[group].append(course)
            else:
                group_courses[group] = [course]

    return group_courses


def upload_supabase_last_calendar():
    groups_courses = get_groups_courses()

    courses_table = supabase_instance.client.table("courses")

    for group in groups_courses:
        courses = groups_courses[group]
        uploaded_courses = get_uploaded_group_courses(group)

        for uploaded_course in uploaded_courses:
            matching_course_index = find_course_index(courses, uploaded_course)

            uuid = uploaded_course["id"]

            # In case there is no course at the same time for the group
            # ==> The uploaded course is not on the calendar anymore
            if matching_course_index == -1:
                courses_table.update({"disabled": True}).eq("id", uuid).execute()
                continue

            matching_course = courses[matching_course_index]

            # In case the title, the professors or the location are different
            # ==> The uploaded course at that specific time has been changed
            if (
                matching_course["title"] != uploaded_course["title"]
                or matching_course["professors"] != uploaded_course["professors"]
                or matching_course["location"] != uploaded_course["location"]
            ):
                courses_table.update({"disabled": True}).eq("id", uuid).execute()
                continue

            # Finally, the course is the same, we don't do anything
            courses.pop(matching_course_index)

        # Then upload the remaining courses
        # ==> Courses that don't exists yet / have been modified
        if len(courses) > 0:
            courses_table.insert(courses).execute()


def upload_git_last_calendar():
    basepath = "logs"

    # Retrieve the last dir of scraped pages
    files = listdir(basepath)
    last_dir = get_last_dir(files)

    # Get the filenames of the calendars
    ics_filter = lambda n: n.endswith(".ics")
    calendars = list(filter(ics_filter, listdir(path.join(basepath, last_dir))))

    # Progress bar
    upload_pbar_manager = enlighten.get_manager()
    upload_pbar = upload_pbar_manager.counter(
        total=len(calendars), desc="Uploading the calendars"
    )
    upload_pbar.update()

    for calendar in calendars:
        calendar_file = open(path.join(basepath, last_dir, calendar))
        msg = f":computer: Uploading calendar {calendar}"
        content = calendar_file.read()

        try:
            uploaded_file = git.repo.get_contents(calendar)
            git.repo.update_file(calendar, msg, content, sha=uploaded_file.sha)
        except:
            git.repo.create_file(calendar, msg, content)

        print(f"[{calendar}] Uploaded the file.")
