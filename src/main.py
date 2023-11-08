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
from operations.ScrapeOperation import ScrapeOperation
from operations.ParseOperation import ParseOperation

from constants.main import PROJECTS

import util

projects = list(PROJECTS.keys())

# Logs directory
logs_directory = f"logs/{util.slugify(str(datetime.now()).split('.')[0])}"
util.create_directory(logs_directory)

# Initialize the logger and the pipe
logger = Logger("PIPE", f"{logs_directory}/logs.txt")
pipe = Pipe(logger, logs_directory)

pipe.add(ScrapeOperation(projects))
pipe.add(ParseOperation())
pipe.add(SupabaseUploadOperation())
pipe.start()
