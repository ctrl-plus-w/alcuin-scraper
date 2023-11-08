# External Libraries
from supabase import create_client, Client

import os

# Custom Libraries & Modules
from classes.SupabaseUploader import SupabaseUploader
from classes.Operation import Operation
from classes.Course import Course
from classes.Logger import Logger

import util


class SupabaseUploadOperation(Operation):
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SERVICE_ROLE_KEY")

        if not url or not key or url == "" or key == "":
            raise Exception("Missing environment variables.")

        self.supabase = create_client(url, key)

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
