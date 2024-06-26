"""Supabase upload operation module"""
# External Libraries
from supabase import create_client

# Custom Libraries & Modules
from src.classes.supabase_uploader import SupabaseUploader
from src.classes.operation import Operation
from src.classes.course import Course
from src.classes.logger import Logger

from src.constants.credentials import SUPABASE_URL, SERVICE_ROLE_KEY

from src import util


class CalendarSupabaseUploadOperation(Operation):
    """Supabase upload grades operation"""

    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

        super().__init__("SUPABASE-UPLOAD")

    def validate(self, data):
        if not isinstance(data, dict):
            return False

        projects = list(data.keys())

        if not all(map(lambda c: util.all_instance(data[c], Course), projects)):
            return False

        return True

    def execute(self, data, logger: Logger):
        logger.info(f"Uploading {len(data)} projects to supabase.")

        uploader = SupabaseUploader(self.supabase, logger)
        uploader.upload_projects_courses(data)

        logger.info("Finished to uploade the courses.")


class GradesSupabaseUploadOperation(Operation):
    """Supabase upload calendars operation"""

    def __init__(self, email: str):
        self.email = email
        self.supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

        super().__init__("SUPABASE-UPLOAD")

    def validate(self, data):
        if not isinstance(data, list):
            return False

        if not all(map(lambda e: isinstance(e, dict), data)):
            return False

        return True

    def execute(self, data, logger: Logger):
        logger.info(f"Uploading {len(data)} grades to supabase.")

        uploader = SupabaseUploader(self.supabase, logger)
        uploader.upload_grades(data, self.email)

        logger.info("Finished to uploade the grades.")


class PathNamesSupabaseUploadOperation(Operation):
    """Supabase upload path names operation"""

    def __init__(self, email: str):
        self.email = email
        self.supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

        super().__init__("SUPABASE-UPLOAD")

    def validate(self, data):
        if not isinstance(data, list):
            return False

        if not all(map(lambda e: isinstance(e, str), data)):
            return False

        return True

    def execute(self, data, logger: Logger):
        logger.info(
            f"Updating the available path names of the user with email {self.email}"
        )

        req = self.supabase.table("profiles")
        req = req.update({"available_path_names": data})
        req.eq("email", self.email)
        req.execute()

        logger.info("Finished to uploade the grades.")
