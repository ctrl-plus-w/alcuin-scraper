"""Service worker module"""
import logging

from time import sleep
from datetime import datetime

from multiprocessing import Process, Queue
from supabase import create_client

import chalk

from src.classes.scraper import InvalidPassword
from src.classes.logger import Logger

from src.commands.scrape_path_names import run_scrape_path_names_command
from src.commands.scrape_grades import run_scrape_grades_command
from src.commands.scrape_calendars import run_scrape_calendars_command

from src.util import _f, slugify, create_directory

from src.constants.credentials import SUPABASE_URL, SERVICE_ROLE_KEY

logging.getLogger("supabase").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("rich").setLevel(logging.WARNING)


def api_checker(queue: Queue, logger: Logger):
    """
    Check every minute if some items have been added to the
    queue and add them if it's not the case
    """

    added_queue_items_id = []

    while True:
        try:
            supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

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
        except Exception as e:
            msg = f"Could not connect to the database ({e})."
            logger.info(chalk.bold(chalk.red(msg)))

        sleep(10)


def run_command(item, logger: Logger):
    """Run a command from the item dictionary"""
    logger.info(chalk.yellow(f"Running command {item['command']} "))

    def set_finished(message: str = None):
        """Set the queue item as finished"""
        args = {"finished": True, "message": message}
        req1 = supabase.table("queue").update(args).eq("id", item["id"])
        req1.execute()

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
        if item["command"] == "SCRAPE_CALENDARS":
            run_scrape_calendars_command(logger, set_finished)

        elif item["command"] == "SCRAPE_GRADES":
            run_scrape_grades_command(logger, user, set_finished)

        elif item["command"] == "SCRAPE_PATH_NAMES":
            run_scrape_path_names_command(logger, user, set_finished)

        else:
            set_finished("! Invalid command.")

    except InvalidPassword:
        req = supabase.table("profiles").update({"alcuin_password": "INVALID"})
        req.eq("id", user["id"])
        req.execute()

        set_finished("! Invalid user password.")

        return


def commands_runner(queue: Queue, logger: Logger):
    """
    Run the commands from the queue
    """
    while True:
        if not queue.empty():
            item = queue.get()

            msg = f"Starting a process from the command id '{item['id']}'."
            logger.info(chalk.cyan(chalk.bold(msg)))

            args = (item, logger)
            name = "command_runner_process"
            process = Process(target=run_command, args=args, name=name)

            process.start()
            process.join()

            msg = f"Finished the process with the command id '{item['id']}' (exit code: {process.exitcode})."
            logger.info(chalk.cyan(chalk.bold(msg)))


def main():
    """Main runner function"""
    # Logs directory
    dt_directory = slugify(str(datetime.now()).split(".", maxsplit=1)[0])
    logs_directory = f"logs/{dt_directory}"
    create_directory(logs_directory)

    queue = Queue()

    # Initialize the logger and the pipe
    logger = Logger("WORKER", f"{logs_directory}/logs.txt")

    args = (queue, logger)

    msg = "Launching the main process : API Process, Runner Process"
    logger.info(chalk.bold(chalk.red(msg)))

    name = "api_checker_process"
    api_process = Process(target=api_checker, args=args, name=name)

    name = "commands_runner_process"
    runner_process = Process(target=commands_runner, args=args, name=name)

    processes = [api_process, runner_process]

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    main()
