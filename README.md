# Alcuin scrapper

## Preface

This project is running on a [venv](https://docs.python.org/3/library/venv.html). So as to running any instruction you need to source the env with `source bin/activate`. However, before sourcing the environment, you need to initialize it if not the case with the `python3 -m venv .` (while being in the root folder of the project).

## Installation

All the informations and commands provided on this file are based on the statement that your project is stored in the `/usr/local/alcuin-scraper` folder.

### Ubuntu Setup

For Ubuntu, you might need to install the `xvfb` package to make the `pyvirtualdisplay` library work. You can run the `sudo apt install xvfb` command.
You also will need to install Chrome and Chromedriver with the following command : `sudo apt install chromium-chromedriver chromium-browser`.

### Python Environement Setup

To install all the dependencies, you can run the following command :  `python3 -m pip install -r requirements.txt`. You also need to setup the credentials with an `.env` file. You just have to copy and rename the `.env.example` to `.env` and replace the values inside quotes with your username and password used on the Alcuin platform. You also need to provide a Github Token with repositories access and the name of the repository to store the `.ics` files.

## Run the project

You can run the project with `python3 -m src.main` (for the main scraper) (Don't forget to source the environment.). You can also run the worker with the following command : `python3 -m src.worker`.
Two files `worker.sh` and `main.sh` are also available to run the `worker` module and the `main` module from a bash file. You might have to `chmod +x worker.sh` and `chmod +x main.sh` if you don't have the required permissions to run the files.

## Documentation 

## The call parameters

Multiple parameters are allowed when running either the `src.main` module or the `src.worker` module :
- `--dev`: The dev mode parameter run the project on the Firefox binary of selenium (Chrome otherwise). When not enabled, some properties are passed to the Chrome instance like the headless parameter and some others.

### The pipe pattern

The whole project is runnning under a Pipe design pattern which is composed of multiple operations. Currently, the project include 4 operations, the Backup, the Scraper, the Parser and the Uploader. 

The Backup operation retrieve the data courses (only those with a description) from the supabase database and stores it into a file. The Scraper consists of creating a browser that will browse the Alcuin website and retrieve the HTML content of different tables for the differents "groups" (called projects) of the school OR retrieve the differents grades of a user. The next operation is the Parse operation, this operation takes the HTML content from the previous operation and retrieve the differents courses for the projects OR the grades of ther user. Finally, from the projects retrieved, the Uploader operation uploads compare the already uploaded courses with the retrieved courses and create / update the courses according to the retrieved data OR compare the uploaded user's grades and create / update when needed.

### The worker file

The `src/worker.py` file is intended to be used as a service. Its purpose is to run some queued scraping actions. This queue is stored as records on a postgres database (supabase in this case). The worker run two processes conccurently. One that check every minutes if some items have been added to the queue and another one that create other processes to run the queued scrapers.

To install the worker as a service, a `alcuin-scraper.service` file is provided. Here is the list of commands you need to run so as to "install" it :

```console
sudo cp alcuin-scraper.service /etc/systemd/system
sudo systemctl daemon-reload 
sudo systemctl enable alcuin-scraper.service
sudo systemctl start alcuin-scraper.service

# You can check the service status with
sudo systemctl status alcuin-scraper.service
```