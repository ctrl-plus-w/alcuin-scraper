"""Scrape path names command module"""
import chalk

from src.classes.logger import Logger
from src.classes.pipe import Pipe

from src.operations.supabase_upload import PathNamesSupabaseUploadOperation
from src.operations.scrape import PathNamesScrapeOperation

from src.util import decrypt_password

from src.constants.credentials import RSA_PRIVATE_KEY


def run_scrape_path_names_command(logger: Logger, user, set_finished):
    """Run the retrieve path names command"""

    if "alcuin_password" not in user:
        msg = "! Missing alcuin password on the user profile."
        logger.info(chalk.bold(chalk.red(msg)))
        set_finished(msg)
        return

    user["alcuin_password"] = decrypt_password(user["alcuin_password"], RSA_PRIVATE_KEY)

    logs_directory = "/".join(logger.filename.split("/")[:-1])
    email = user["email"]
    username = email.split("@")[0]
    password = user["alcuin_password"]

    args = (logger, logs_directory, username, email, password)
    start_scrape_path_names_pipe(*args)

    set_finished()


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
