# External Libraries
from supabase import create_client

# Custom Libraries & Modules
from classes.SupabaseUploader import SupabaseUploader
from classes.Operation import Operation
from classes.Course import Course
from classes.Logger import Logger

from constants.credentials import SUPABASE_URL, SERVICE_ROLE_KEY

import util


class SupabaseUploadOperation(Operation):
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

        super().__init__("SUPABASE-UPLOAD")

    def validate(self, data):
        if not type(data) is dict:
            return False

        projects = list(data.keys())

        if not all(map(lambda c: util.all_instance(data[c], Course), projects)):
            return False

        return True

    def execute(self, data, logger: Logger):
        logger.info(f"Uploading {len(data)} projects to supabase.")

        uploader = SupabaseUploader(self.supabase, logger)
        uploader.upload(data)

        logger.info("Finished to uploade the courses.")
