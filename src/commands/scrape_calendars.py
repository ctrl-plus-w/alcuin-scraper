"""Scrape calendars command module"""
from src.classes.logger import Logger
from src.classes.pipe import Pipe

from src.operations.supabase_upload import CalendarSupabaseUploadOperation
from src.operations.scrape import CalendarScrapeOperation
from src.operations.parse import CalendarParseOperation
from src.operations.backup import BackupOperation

from src.constants.main import PROJECTS


def run_scrape_calendars_command(logger: Logger, set_finished):
    """Run the retrieve path names command"""
    logs_directory = "/".join(logger.filename.split("/")[:-1])
    backup_file = logs_directory.replace("logs", "backups")

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
