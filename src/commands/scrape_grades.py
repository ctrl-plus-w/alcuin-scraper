"""Scrape grades command module"""
import chalk

from src.classes.logger import Logger
from src.classes.pipe import Pipe

from src.operations.supabase_upload import GradesSupabaseUploadOperation
from src.operations.scrape import GradesScrapeOperation
from src.operations.parse import GradesParseOperation


def run_scrape_grades_command(logger: Logger, user, set_finished):
    """Run the scrape grades command"""

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
