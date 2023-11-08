# Custom Libraries & Modules
from classes.Logger import Logger
from classes.Course import Course

import util


class SupabaseUploader:
    def __init__(self, supabase, logger: Logger):
        self.logger = logger
        self.supabase = supabase
        self.table = supabase.table("courses")

    def find_course_index(self, courses: list[Course], course: Course):
        """Through the courses passed in the first parameter, return the index of the course first course with the same start and end time (as the second parameter). If the course isn't found, return -1."""
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
        request = self.table.select("*").eq("group", project).eq("disabled", False)
        response = request.execute()

        return response.data

    def upload_project_courses(self, project: str, courses: list[Course]):
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
                # Enable this condition if you only want to allow setting courses as disabled if they are in the future
                # if not util.is_in_past(uploaded_course["start_datetime"]):
                self.table.update({"disabled": True}).eq("id", uuid).execute()
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

                self.table.update(update_obj).eq("id", uuid).execute()
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
            self.table.insert(courses_as_supabase_dict).execute()

    def upload(self, projects_courses):
        """Upload the projects courses to supabase"""
        for project in projects_courses:
            courses = projects_courses[project]
            self.logger.info(f"Found {len(courses)} for the project {project}")

            self.upload_project_courses(project, projects_courses[project])
            self.logger.info(
                f"Successfully checked {len(courses)} to the project {project}."
            )
