"""Scrape calendars command module"""
from datetime import datetime

from src.classes.logger import Logger
from src.classes.pipe import Pipe
from src.constants.main import PROJECTS
from src.operations.backup import BackupOperation
from src.operations.parse import CalendarParseOperation
from src.operations.scrape import CalendarScrapeOperation
from src.operations.supabase_upload import CalendarSupabaseUploadOperation
from src.util import slugify, create_directory


def run_scrape_calendars_command(logger: Logger, set_finished):
    """Run the retrieve path names command"""
    logs_directory = "/".join(logger.filename.split("/")[:-1])

    dt_directory = slugify(str(datetime.now()).split(".", maxsplit=1)[0])
    backup_directory = f"backups/{dt_directory}"
    create_directory(backup_directory)

    backup_file = f"{backup_directory}/backup.json"

    args = (logger, logs_directory, backup_file)
    start_scrape_calendars_pipe(*args)

    set_finished()


def start_scrape_calendars_pipe(
        logger: Logger,
        logs_directory: str,
        backup_file: str,
):
    """Create and start the scrape calendars pipe"""
    projects = list(PROJECTS.keys())
    pipe = Pipe(logger, logs_directory)

    pipe.add(BackupOperation(backup_file))
    pipe.add(CalendarScrapeOperation(projects))
    pipe.add(CalendarParseOperation())
    pipe.add(CalendarSupabaseUploadOperation())
    pipe.start()
