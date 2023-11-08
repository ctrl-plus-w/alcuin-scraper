# External Libraries
import json

# Custom Libraries & Modules
from classes.Operation import Operation
from classes.Logger import Logger
from classes.Scraper import Scraper


class ScrapeOperation(Operation):
    def __init__(self, projects: list[str]):
        self.projects = projects

        super().__init__("SCRAPE")

    def validate(self, data) -> bool:
        return True

    def save_data(self, data, path: str):
        with open(f"{path}.json", "w") as f:
            json.dump(data, f, indent=2)

    def execute(self, data, logger: Logger):
        # Initialize the scrapper
        scraper = Scraper(logger)

        # Initalize the returned data dictionnary
        projects_html = {p: [[], []] for p in self.projects}

        # This loop is used because we run the scrapper twice (one for the current month and another time for the next month)
        for i in range(2):
            scraped_html = scraper.scrape(self.projects)

            for project in scraped_html:
                projects_html[project][i] = scraped_html[project]

            scraper.set_next_month()

        return projects_html
