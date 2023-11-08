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

The whole project is runnning under a Pipe design pattern which is composed of multiple operations. Currently, the project include 4 operations, the Backup, the Scraper, the Parser and the Uploader. The Backup operation retrieve the courses (only those with a description) from the supabase database and stores it into a file. The Scraper consists of creating a browser that will browse the Alcuin website and retrieve the HTML content of different tables for the differents "groups" (called projects) of the school. The next operation is the Parse operation, this operation takes the HTML content from the previous operation and retrieve the differents courses for the projects. Finally, from the projects retrieved, the Uploader operation uploads compare the already uploaded courses with the retrieved courses and create / update the courses according to the retrieved data.