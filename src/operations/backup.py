"""Backup Operation module"""
import json

from supabase import create_client


# Custom Libraries & Modules
from src.classes.operation import Operation
from src.classes.logger import Logger

from src.constants.credentials import SUPABASE_URL, SERVICE_ROLE_KEY


class BackupOperation(Operation):
    """Backup Operation used to backup the courses with a description"""

    def __init__(self, backup_path: str):
        self.supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
        self.backup_path = backup_path

        super().__init__("SUPABASE-BACKUP")

    def validate(self, data):
        return True

    def execute(self, data, logger: Logger):
        logger.info("Backing up the current courses with a description.")

        # Retrieve the course (only those with a description)
        courses_table = self.supabase.table("courses")
        req = courses_table.select("*").neq("description", "")
        courses = req.execute().data

        # Save the course into the backup file
        f = open(self.backup_path, "w", encoding="utf-8")
        json.dump(courses, f, indent=2)
        f.close()

        logger.info(f"Made a backup with {len(courses)} courses.")

        return data
