"""Supabase uploader module"""
from typing import Dict

from src.classes.logger import Logger
from src.classes.course import Course

from src import util


class SupabaseUploader:
    """Supabase uploader class"""

    def __init__(self, supabase, logger: Logger):
        self.logger = logger
        self.supabase = supabase

        self.courses_table = supabase.table("courses")
        self.profiles_table = supabase.table("profiles")
        self.grades_table = supabase.table("grades")

    def find_course_index(self, courses: list[Course], course: Course):
        """
        Through the courses passed in the first parameter, return the index of the course
        first course with the same start and end time (as the second parameter).
        If the course isn't found, return -1.
        """
        for i, _course in enumerate(courses):
            stdt = "start_datetime"
            start_eq = util.compare_dates_with_timezone(course[stdt], _course[stdt])

            eddt = "end_datetime"
            end_eq = util.compare_dates_with_timezone(course[eddt], _course[eddt])

            if start_eq and end_eq:
                return i

        return -1

    def get_uploaded_group_courses(self, project: str):
        """Get all the courses of the given project"""
        request = (
            self.courses_table.select("*").eq("group", project).eq("disabled", False)
        )
        response = request.execute()

        return response.data

    def upload_single_project_courses(self, project: str, courses: list[Course]):
        """Upload the courses of the given project"""
        uploaded_courses = self.get_uploaded_group_courses(project)
        courses_as_supabase_dict = list(map(lambda c: c.as_supabase_dict(), courses))

        for uploaded_course in uploaded_courses:
            matching_course_index = self.find_course_index(
                courses_as_supabase_dict, uploaded_course
            )

            uuid = uploaded_course["id"]

            # In case there is no course at the same time for the group
            # ==> The uploaded course is not on the calendar anymore
            if matching_course_index == -1:
                # Enable this condition if you only want to allow setting courses
                # as disabled if they are in the future
                # if not util.is_in_past(uploaded_course["start_datetime"]):
                self.courses_table.update({"disabled": True}).eq("id", uuid).execute()
                continue

            matching_course = courses_as_supabase_dict[matching_course_index]

            # In case the title, the professors or the location are different
            # ==> The uploaded course at that specific time has been changed
            if (
                matching_course["title"] != uploaded_course["title"]
                or matching_course["professors"] != uploaded_course["professors"]
                or matching_course["location"] != uploaded_course["location"]
            ):
                update_obj = {
                    "title": matching_course["title"],
                    "professors": matching_course["professors"],
                    "location": matching_course["location"],
                }

                self.courses_table.update(update_obj).eq("id", uuid).execute()
                courses_as_supabase_dict.pop(matching_course_index)
                continue

            # Finally, the course is the same, we don't do anything
            courses_as_supabase_dict.pop(matching_course_index)

        self.logger.info(
            f"Found {len(courses_as_supabase_dict)} courses remaining to upload."
        )

        # Then upload the remaining courses
        # ==> Courses that don't exists yet / have been modified
        if len(courses_as_supabase_dict) > 0:
            self.courses_table.insert(courses_as_supabase_dict).execute()

    def upload_projects_courses(self, projects_courses):
        """Upload the projects courses to supabase"""
        for project in projects_courses:
            courses = projects_courses[project]
            self.logger.info(f"Found {len(courses)} for the project {project}")

            self.upload_single_project_courses(project, projects_courses[project])
            self.logger.info(
                f"Successfully checked {len(courses)} to the project {project}."
            )

    def get_profile_from_email(self, email: str):
        """Get the profile from supabase (raise an error if the profile is not found)"""
        profiles = self.profiles_table.select("*").eq("email", email).execute().data

        if len(profiles) == 0:
            msg = f"Didn't found any profile for the given email : '{email}'"
            raise ValueError(msg)

        return profiles[0]

    def get_matching_uploaded_grade(self, grade, profile):
        """Get the uploaded matching grade"""
        req = self.grades_table.select("*")

        req.eq("user_id", profile["id"])
        req.eq("code_ue", grade["code_ue"])
        req.eq("code", grade["code"])
        req.eq("label", grade["label"])
        req.eq("code", grade["code"])

        uploaded_grades = req.execute().data

        if len(uploaded_grades) == 0:
            return None

        return uploaded_grades[0]

    def upload_single_grade(self, grade, profile):
        """Uploade or update a single grade"""
        uploaded_grade = self.get_matching_uploaded_grade(grade, profile)

        def _(value):
            if value == "":
                return None
            return value

        if uploaded_grade:
            self.grades_table.update(
                {
                    "coef": _(grade["coef"]),
                    "mean": _(grade["mean"]),
                }
            ).eq("id", uploaded_grade["id"]).execute()
        else:
            self.grades_table.insert(
                {
                    "user_id": profile["id"],
                    "code_ue": _(grade["code_ue"]),
                    "ue": _(grade["ue"]),
                    "label": _(grade["label"]),
                    "code": _(grade["code"]),
                    "coef": _(grade["coef"]),
                    "mean": _(grade["mean"]),
                }
            ).execute()

    def upload_grades(self, grades: list[Dict], email: str):
        """Upload the grades for the user profiel with the given email"""
        profile = self.get_profile_from_email(email)
        self.logger.info(
            f"Successfully found a profile with id {profile['id']} (email: {email})"
        )

        self.logger.info(f"Uploading {len(grades)} grades to the user's profiel.")
        for grade in grades:
            self.upload_single_grade(grade, profile)
