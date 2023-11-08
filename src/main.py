#!/usr/bin/python3

# External Libraries
from datetime import datetime

import json

# Custom Libraries & Modules
from classes.Pipe import Pipe
from classes.Operation import Operation
from classes.Logger import Logger
from classes.Course import Course

from operations.SupabaseUploadOperation import SupabaseUploadOperation
from operations.BackupOperation import BackupOperation
from operations.ScrapeOperation import ScrapeOperation
from operations.ParseOperation import ParseOperation

from constants.main import PROJECTS

import util


def main():
    projects = list(PROJECTS.keys())

    # Logs & Backup directory
    dt_directory = util.slugify(str(datetime.now()).split(".")[0])
    logs_directory = f"logs/{dt_directory}"
    backup_directory = f"backups/{dt_directory}"

    util.create_directory(logs_directory)
    util.create_directory(backup_directory)

    backup_file = f"{backup_directory}/backup.json"

    # Initialize the logger and the pipe
    logger = Logger("PIPE", f"{logs_directory}/logs.txt")
    pipe = Pipe(logger, logs_directory)

    pipe.add(BackupOperation(backup_file))
    pipe.add(ScrapeOperation(projects))
    pipe.add(ParseOperation())
    pipe.add(SupabaseUploadOperation())
    pipe.start()


if __name__ == "__main__":
    main()
