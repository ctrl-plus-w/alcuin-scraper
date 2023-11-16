"""Scraper module"""
# External Libraries
import sys

from typing import Dict
from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# Custom Libraries & Modules
from src.classes.logger import Logger

from src.constants.credentials import USERNAME, PASSWORD
from src.constants.main import PROJECTS


class Scraper:
    """Scraper class to retrieve the HTML from Alcuin"""

    def __init__(self, logger: Logger):
        self.logger = logger
        self.driver = None

        self.setup_driver()

    def login(self):
        """Login to the page"""

        self.logger.info("Navigating to the login page.")
        self.driver.get("https://esaip.alcuin.com/OpDotNet/Noyau/Login.aspx")

        username_input = self.driver.find_element(
            By.ID, "UcAuthentification1_UcLogin1_txtLogin"
        )
        username_input.send_keys(USERNAME)

        password_input = self.driver.find_element(
            By.ID, "UcAuthentification1_UcLogin1_txtPassword"
        )
        password_input.send_keys(PASSWORD)

        submit_button = self.driver.find_element(
            By.ID, "UcAuthentification1_UcLogin1_btnEntrer"
        )
        submit_button.click()

    def switch_to_agenda(self):
        """Switch to the agenda frame"""
        self.driver.execute_script(
            "window.parent.content.location = '/OpDotnet/commun/Login/aspxtoasp.aspx?url=/Eplug/Agenda/Agenda.asp?IdApplication=190&TypeAcces=Utilisateur&IdLien=649';"
        )

    def switch_to_content(self):
        """Switch to the content frame"""
        self.driver.switch_to.frame(
            self.driver.find_element(By.CSS_SELECTOR, 'frame[name="content"]')
        )

    def wait_for_content_to_load(self):
        """Wait for the content frame to load"""
        WebDriverWait(self.driver, 60).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "#DivAll > table:nth-child(19)")
            ),
            "The frame wasn't found.",
        )

    def setup_session(self):
        """Setup the session"""
        return

    def setup_driver(self):
        """Setup the driver"""
        self.logger.info("Setting up the session")
        dev = len(sys.argv) > 1 and "--dev" in sys.argv

        opts = Options()
        servs = Service() if dev else Service(executable_path="/usr/bin/chromedriver")

        if not dev:
            opts.add_argument("--no-sandbox")
            opts.add_argument("--headless")
            opts.add_argument("--disable-gpu")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument("--remote-debugging-port=9222")

            opts.headless = True

        DriverCore = webdriver.Firefox if dev else webdriver.Chrome

        self.logger.info("Creating the driver...")
        self.driver = DriverCore(options=opts, service=servs)
        self.logger.info("Created the driver")

        self.driver.maximize_window()

        self.setup_session()

    def set_project(self, project):
        """Set the project (group) by its id"""
        uid = PROJECTS[project]

        self.logger.info(f"Setting the project to {project} (id: {uid}).")
        self.driver.execute_script(f"ModCal('{uid}');")
        sleep(1)

        self.wait_for_content_to_load()


class CalendarScraper(Scraper):
    """Scraper for the calendars informations"""

    def setup_session(self):
        self.login()
        sleep(5)

        self.logger.info("Switching to the agenda...")
        self.switch_to_agenda()
        sleep(5)

        self.logger.info("Switching to the content frame...")
        self.switch_to_content()

        self.logger.info("Waiting for the content to load...")
        self.wait_for_content_to_load()

        self.logger.info("Selecting the month interval...")
        self.select_interval("Mois")

        self.logger.info("Waiting for the content to load...")
        self.wait_for_content_to_load()

    def set_next_month(self):
        """Switch to the agenda next month"""
        self.logger.info("Switch the agenda to the next month.")
        self.driver.execute_script(
            "SelDat(document.formul.CurDat,null,'MovDat');SelMoiSui();ChxDat=1;SetSelDat();"
        )

    def select_interval(self, visible_text):
        """Select the interval"""
        interval_select = Select(
            self.driver.find_element(
                By.CSS_SELECTOR,
                "#DivTit > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > select:nth-child(2)",
            )
        )

        interval_select.select_by_visible_text(visible_text)

    def get_agenda_table_body(self):
        """Retrieve the agenda table body element"""
        return self.driver.find_element(
            By.CSS_SELECTOR,
            "#DivVis > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1)",
        )

    def scrape_project(self, project: str) -> str:
        """Scrape a single project and return the agenda HTML content"""
        start = time()
        self.set_project(project)

        agenda = self.get_agenda_table_body()
        html = agenda.get_attribute("innerHTML")

        diff = time() - start
        self.logger.info(
            f"Successfully retrieved the HTML content of the {project} agenda. It took {diff} seconds."
        )

        return html

    def scrape(self, projects: list[str]) -> Dict[str, str]:
        """
        Scrape multiple projects and returns the results as a
        dictionnary with the project name being the key and the HTML content being the value
        """
        projects_html = {}

        for project in projects:
            projects_html[project] = self.scrape_project(project)

        return projects_html
