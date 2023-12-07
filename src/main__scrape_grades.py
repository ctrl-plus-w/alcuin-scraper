import sys
from datetime import datetime
from supabase import create_client

import chalk

from src.classes.logger import Logger

from src.commands.scrape_grades import run_scrape_grades_command

from src.util import slugify, create_directory

from src.constants.credentials import SUPABASE_URL, SERVICE_ROLE_KEY


def main():
    # Logs directory
    dt_directory = slugify(str(datetime.now()).split(".", maxsplit=1)[0])
    logs_directory = f"logs/{dt_directory}"
    create_directory(logs_directory)

    # Initialize the logger and the pipe
    logger = Logger("WORKER", f"{logs_directory}/logs.txt")

    # Initialize supabase
    supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

    def set_finished(message: str = None):
        logger.info(chalk.bold(chalk.red(message)))

    # Retrieve the user
    email = sys.argv[1]
    req = supabase.table("profiles").select("*").eq("email", email)
    users = req.execute().data

    if len(users) == 0:
        msg = "! Did not found any user with the specified email."
        logger.info(chalk.bold(chalk.red(msg)))
        set_finished(msg)
        return

    user = users[0]

    run_scrape_grades_command(logger, user, set_finished)


if __name__ == '__main__':
    main()
