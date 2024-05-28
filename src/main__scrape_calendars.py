from datetime import datetime

import chalk

from src.classes.logger import Logger

from src.commands.scrape_calendars import run_scrape_calendars_command

from src.util import slugify, create_directory


def main():
    # Logs directory
    dt_directory = slugify(str(datetime.now()).split(".", maxsplit=1)[0])
    logs_directory = f"logs/{dt_directory}"
    create_directory(logs_directory)

    # Initialize the logger and the pipe
    logger = Logger("WORKER", f"{logs_directory}/logs.txt")

    def set_finished(msg: str = None):
        if msg:
            logger.info(chalk.bold(chalk.red(msg)))

    run_scrape_calendars_command(logger, set_finished)


if __name__ == '__main__':
    main()
