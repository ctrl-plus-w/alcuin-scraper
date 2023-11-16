#!/usr/bin/python3
"""Main module"""

# External Libraries
from datetime import datetime


# Custom Libraries & Modules
from src.classes.pipe import Pipe
from src.classes.logger import Logger

from src.operations.supabase_upload import CalendarSupabaseUploadOperation
from src.operations.backup import BackupOperation
from src.operations.scrape import CalendarScrapeOperation
from src.operations.parse import CalendarParseOperation

from src.constants.main import PROJECTS

from src import util


def main():
    """Main project function"""
    projects = list(PROJECTS.keys())

    # Logs & Backup directory
    dt_directory = util.slugify(str(datetime.now()).split(".", maxsplit=1)[0])
    logs_directory = f"logs/{dt_directory}"
    backup_directory = f"backups/{dt_directory}"

    util.create_directory(logs_directory)
    util.create_directory(backup_directory)

    backup_file = f"{backup_directory}/backup.json"

    # Initialize the logger and the pipe
    logger = Logger("PIPE", f"{logs_directory}/logs.txt")
    pipe = Pipe(logger, logs_directory)

    pipe.add(BackupOperation(backup_file))
    pipe.add(CalendarScrapeOperation(projects))
    pipe.add(CalendarParseOperation())
    pipe.add(CalendarSupabaseUploadOperation())
    pipe.start()


if __name__ == "__main__":
    main()
