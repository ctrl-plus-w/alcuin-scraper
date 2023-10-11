from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from pyvirtualdisplay import Display

from time import sleep

import enlighten

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


def setup_session(pbar: enlighten.Manager):
    display = Display(visible=0, size=(800, 600))
    display.start()

    opts = Options()
    servs = Service(executable_path="/usr/bin/chromedriver")

    opts.add_argument("--no-sandbox")
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--remote-debugging-port=9222")

    opts.headless = True

    driver = webdriver.Chrome(options=opts, service=servs)
    driver.get("https://esaip.alcuin.com/OpDotNet/Noyau/Login.aspx")
    pbar.update()

    login(driver)
    pbar.update()
    sleep(1)
    switch_to_agenda(driver)
    pbar.update()
    switch_to_content(driver)
    pbar.update()
    wait_for_content_to_load(driver)
    pbar.update()
    select_interval(driver, "Mois")
    pbar.update()
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

