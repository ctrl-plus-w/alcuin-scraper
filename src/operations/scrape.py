"""Scrape Operation module"""
# External Libraries
import json

# Custom Libraries & Modules
from src.classes.operation import Operation
from src.classes.logger import Logger
from src.classes.scraper import CalendarScraper


class CalendarScrapeOperation(Operation):
    """Scrape Operation used to retrieve the HTML content of the calendars"""

    def __init__(self, projects: list[str]):
        self.projects = projects

        super().__init__("SCRAPE")

    def validate(self, _data) -> bool:
        return True

    def save_data(self, data, path: str):
        with open(f"{path}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def execute(self, _data, logger: Logger):
        # Initialize the scrapper
        scraper = CalendarScraper(logger)

        # Initalize the returned data dictionnary
        projects_html = {p: [[], []] for p in self.projects}

        # This loop is used because we run the scrapper twice
        # (one for the current month and another time for the next month)
        for i in range(2):
            scraped_html = scraper.scrape(self.projects)

            for project, html in scraped_html.items():
                projects_html[project][i] = html

            scraper.set_next_month()

        return projects_html
