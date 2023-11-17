"""Service worker module"""
import logging

from time import sleep
from datetime import datetime

from multiprocessing import Process, Queue
from supabase import create_client

import chalk

from src.classes.scraper import InvalidPassword
from src.classes.logger import Logger
from src.classes.pipe import Pipe

from src.operations.supabase_upload import (
    GradesSupabaseUploadOperation,
    PathNamesSupabaseUploadOperation,
)
from src.operations.scrape import GradesScrapeOperation, PathNamesScrapeOperation
from src.operations.parse import GradesParseOperation

from src.util import _f, slugify, create_directory

from src.constants.credentials import SUPABASE_URL, SERVICE_ROLE_KEY


logging.getLogger("supabase").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("rich").setLevel(logging.WARNING)


def start_scrape_grades_pipe(
    logger: Logger,
    logs_directory: str,
    username: str,
    email: str,
    password: str,
    path_name: str,
):
    """Create an start the scrape grades pipe"""
    pipe = Pipe(logger, logs_directory)

    pipe.add(GradesScrapeOperation(username, password, path_name))
    pipe.add(GradesParseOperation())
    pipe.add(GradesSupabaseUploadOperation(email))

    pipe.start()


def start_scrape_path_names_pipe(
    logger: Logger,
    logs_directory: str,
    username: str,
    email: str,
    password: str,
):
    """Create and start the scrape path names pipe"""
    pipe = Pipe(logger, logs_directory)

    pipe.add(PathNamesScrapeOperation(username, password))
    pipe.add(PathNamesSupabaseUploadOperation(email))

    pipe.start()


def api_checker(queue: Queue, logger: Logger):
    """
    Check every minute if some items have been added to the
    queue and add them if it's not the case
    """
    supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

    added_queue_items_id = []

    while True:
        req = supabase.table("queue").select("*").eq("finished", False)
        sb_queue_items = req.execute().data

        # Only keep the queue items that didn't got added yet
        sb_queue_items = _f(
            lambda i: not i["id"] in added_queue_items_id, sb_queue_items
        )

        if len(sb_queue_items) > 0:
            msg = f"Retrieved {len(sb_queue_items)} items."
            logger.info(chalk.red(chalk.bold(msg)))

        # Add all the items to the queue
        for queue_item in sb_queue_items:
            queue.put(queue_item)
            added_queue_items_id.append(queue_item["id"])

        sleep(60)


def run_scrape_grades_operation(logger: Logger, user, set_finished):
    """Run the scrape grades operation"""

    if not "alcuin_password" in user:
        msg = "! Missing alcuin password on the user profile."
        logger.info(chalk.bold(chalk.red(msg)))
        set_finished(msg)
        return

    if not "path_name" in user:
        msg = "! Missing path name on the user profile."
        logger.info(chalk.bold(chalk.red(msg)))
        set_finished(msg)
        return

    logs_directory = "/".join(logger.filename.split("/")[:-1])
    email = user["email"]
    username = email.split("@")[0]
    password = user["alcuin_password"]
    path_name = user["path_name"]

    args = (logger, logs_directory, username, email, password, path_name)
    start_scrape_grades_pipe(*args)

    set_finished()


def run_scrape_path_names_operation(logger: Logger, user, set_finished):
    """Run the retrieve path names operation"""

    if not "alcuin_password" in user:
        msg = "! Missing alcuin password on the user profile."
        logger.info(chalk.bold(chalk.red(msg)))
        set_finished(msg)
        return

    logs_directory = "/".join(logger.filename.split("/")[:-1])
    email = user["email"]
    username = email.split("@")[0]
    password = user["alcuin_password"]

    args = (logger, logs_directory, username, email, password)
    start_scrape_path_names_pipe(*args)

    set_finished()


def run_operation(item, logger: Logger):
    """Run an operation from the item dictionnary"""
    logger.info(chalk.yellow(f"Running operation {item['operation']} "))

    def set_finished(message: str = None):
        """Set the queue item as finished"""
        args = {"finished": True, "message": message}
        req = supabase.table("queue").update(args).eq("id", item["id"])
        req.execute()

    supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

    req = supabase.table("profiles").select("*").eq("id", item["user_id"])
    users = req.execute().data

    if len(users) == 0:
        msg = "! Did not found any user with the specified id."
        logger.info(chalk.bold(chalk.red(msg)))
        set_finished(msg)
        return

    user = users[0]

    try:
        if item["operation"] == "SCRAPE_GRADES":
            run_scrape_grades_operation(logger, user, set_finished)

        elif item["operation"] == "SCRAPE_PATH_NAMES":
            run_scrape_path_names_operation(logger, user, set_finished)

        else:
            set_finished("! Invalid operation.")
    except InvalidPassword:
        req = supabase.table("profiles").update({"alcuin_password": "INVALID"})
        req.eq("id", user["id"])
        req.execute()

        set_finished("! Invalid user password.")

        return


def operations_runner(queue: Queue, logger: Logger):
    """
    Run the operations from the queue
    """
    while True:
        if not queue.empty():
            item = queue.get()

            msg = f"Starting a process from the operation id '{item['id']}'."
            logger.info(chalk.cyan(chalk.bold(msg)))

            args = (item, logger)
            process = Process(target=run_operation, args=args)

            process.start()
            process.join()

            msg = f"Finished the process with the operation id '{item['id']}'."
            logger.info(chalk.cyan(chalk.bold(msg)))


def main():
    """Main runner function"""
    # Logs directory
    dt_directory = slugify(str(datetime.now()).split(".", maxsplit=1)[0])
    logs_directory = f"logs/worker/{dt_directory}"
    create_directory(logs_directory)

    queue = Queue()

    # Initialize the logger and the pipe
    logger = Logger("WORKER", f"{logs_directory}/logs.txt")

    args = (queue, logger)

    msg = "Launching the main process : API Process, Runner Process"
    logger.info(chalk.bold(chalk.red(msg)))

    api_process = Process(target=api_checker, args=args)
    runner_process = Process(target=operations_runner, args=args)

    processes = [api_process, runner_process]

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    main()
