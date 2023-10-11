# Alcuin scrapper

## Preface

This project is running on a [venv](https://docs.python.org/3/library/venv.html). So as to running any instruction you need to source the env with `source bin/activate`. However, before sourcing the environment, you need to initialize it if not the case with the `python3 -m venv .` (while being in the root folder of the project).

## Installation

### Ubuntu Setup

For Ubuntu, you might need to install the `xvfb` package to make the `pyvirtualdisplay` library work. You can run the `sudo apt install xvfb` command.
You also will need to install Chrome and Chromedriver with the following command : `sudo apt install chromium-chromedriver chromium-browser`.

### Python Environement Setup

To install all the dependencies, you can run the following command :  `python3 -m pip install -r requirements.txt`. You also need to setup the credentials with an `.env` file. You just have to copy and rename the `.env.example` to `.env` and replace the values inside quotes with your username and password used on the Alcuin platform. You also need to provide a Github Token with repositories access and the name of the repository to store the `.ics` files.

## Run the project

You can run the project with `python3 src/main.py`. (Don't forget to source the environment.)

## Documentation 

The type of the course dictionnary returned by the parser :
```
{
  "title": str,
  "start_time": {
    "hours": int,
    "minutes": int,
  },
  "end_time": {
    "hours": int,
    "minutes": int,
  },
  "professors": str[],
  "groups": str[],
  "location": str | None,
  "date": int,
}
```
