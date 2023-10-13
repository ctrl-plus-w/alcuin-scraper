from os import listdir, path

from uploader import git

import enlighten
import logging


def get_last_dir(dirs):
    # TODO : Explain why that value_of function (filename comes from the datetime.now() func / used to sort)
    dirs = list(filter(lambda dir: not "." in dir, dirs))
    value_of = lambda name: int(name.replace("_", ""))

    curr = dirs[0]
    value = value_of(curr)

    for directory in dirs:
        if value_of(directory) > value:
            curr = directory
            value = value_of(curr)

    return curr


def upload_last_calendars(logger: logging.Logger):
    basepath = "logs"

    # Retrieve the last dir of scraped pages
    files = listdir(basepath)
    last_dir = get_last_dir(files)

    # Get the filenames of the calendars
    ics_filter = lambda n: n.endswith(".ics")
    calendars = list(filter(ics_filter, listdir(path.join(basepath, last_dir))))

    # Progress bar
    upload_pbar_manager = enlighten.get_manager()
    upload_pbar = upload_pbar_manager.counter(
        total=len(calendars), desc="Uploading the calendars"
    )
    upload_pbar.update()

    for calendar in calendars:
        calendar_file = open(path.join(basepath, last_dir, calendar))
        msg = f":computer: Uploading calendar {calendar}"
        content = calendar_file.read()

        try:
            uploaded_file = git.repo.get_contents(calendar)
            git.repo.update_file(calendar, msg, content, sha=uploaded_file.sha)
        except:
            git.repo.create_file(calendar, msg, content)

        logger.info(f"[{calendar}] Uploaded the file.")
        upload_pbar.update()
