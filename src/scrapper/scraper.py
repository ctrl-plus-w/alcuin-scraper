from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from pyvirtualdisplay import Display

from time import sleep

import enlighten
import sys

from constants.credentials import USERNAME, PASSWORD
from constants.main import PROJECTS


def login(driver):
    username_input = driver.find_element(By.ID, "UcAuthentification1_UcLogin1_txtLogin")
    username_input.send_keys(USERNAME)

    password_input = driver.find_element(
        By.ID, "UcAuthentification1_UcLogin1_txtPassword"
    )
    password_input.send_keys(PASSWORD)

    submit_button = driver.find_element(By.ID, "UcAuthentification1_UcLogin1_btnEntrer")
    submit_button.click()


def switch_to_agenda(driver):
    driver.execute_script(
        "window.parent.content.location = '/OpDotnet/commun/Login/aspxtoasp.aspx?url=/Eplug/Agenda/Agenda.asp?IdApplication=190&TypeAcces=Utilisateur&IdLien=649';"
    )


def switch_to_content(driver):
    content_frame = driver.find_element(By.CSS_SELECTOR, 'frame[name="content"]')
    driver.switch_to.frame(content_frame)


def set_next_month(driver):
    driver.execute_script(
        "SelDat(document.formul.CurDat,null,'MovDat');SelMoiSui();ChxDat=1;SetSelDat();"
    )


def wait_for_content_to_load(driver):
    WebDriverWait(driver, 60).until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "#DivAll > table:nth-child(19)")
        ),
        "The frame wasn't found.",
    )


def select_interval(driver, visible_text):
    interval_select = Select(
        driver.find_element(
            By.CSS_SELECTOR,
            "#DivTit > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > select:nth-child(2)",
        )
    )

    interval_select.select_by_visible_text(visible_text)


def get_agenda_table_body(driver):
    return driver.find_element(
        By.CSS_SELECTOR,
        "#DivVis > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1)",
    )


def setup_session(pbar: enlighten.Manager, logger):
    logger.info("Setting up the session")
    dev = len(sys.argv) > 1 and "--dev" in sys.argv

    """
    This is sometimes required, might need to create a specific parameter to enable this.
    if not dev:
        logger.info("Starting the display..")
        display = Display(visible=0, size=(800, 600))
        display.start()
        logger.info("Started the display")
    """

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

    logger.info("About to create the driver")
    driver = DriverCore(options=opts, service=servs)
    logger.info("Created the driver, about the navigate to the url")
    # driver = webdriver.Firefox(options=opts, service=servs)
    driver.get("https://esaip.alcuin.com/OpDotNet/Noyau/Login.aspx")
    pbar.update()

    login(driver)
    pbar.update()
    sleep(5)
    logger.info("Switching to the agenda...")
    switch_to_agenda(driver)
    pbar.update()
    sleep(5)
    logger.info("Switching to the content frame...")
    switch_to_content(driver)
    pbar.update()
    logger.info("Waiting for the content to load...")
    wait_for_content_to_load(driver)
    pbar.update()
    logger.info("Selecting the month interval...")
    select_interval(driver, "Mois")
    pbar.update()
    logger.info("Waiting for the content to load...")
    wait_for_content_to_load(driver)
    pbar.update()
    print()

    return driver


def set_project(driver, project):
    id = PROJECTS[project]

    driver.execute_script(f"ModCal('{id}');")
    sleep(1)
    wait_for_content_to_load(driver)


def scrape(driver, project):
    set_project(driver, project)

    return get_agenda_table_body(driver)
