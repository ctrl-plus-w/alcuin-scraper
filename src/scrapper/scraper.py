from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options

from time import sleep

from constants.credentials import USERNAME, PASSWORD
from constants.main import PROJECTS


def login(driver):
    print("[DEBUG] Logging in.")
    username_input = driver.find_element(By.ID, "UcAuthentification1_UcLogin1_txtLogin")
    username_input.send_keys(USERNAME)

    password_input = driver.find_element(
        By.ID, "UcAuthentification1_UcLogin1_txtPassword"
    )
    password_input.send_keys(PASSWORD)

    submit_button = driver.find_element(By.ID, "UcAuthentification1_UcLogin1_btnEntrer")
    submit_button.click()


def switch_to_agenda(driver):
    print("[DEBUG] Switching to the agenda tab.")
    driver.execute_script(
        "window.parent.content.location = '/OpDotnet/commun/Login/aspxtoasp.aspx?url=/Eplug/Agenda/Agenda.asp?IdApplication=190&TypeAcces=Utilisateur&IdLien=649';"
    )


def switch_to_content(driver):
    print("[DEBUG] Switching to the content frame.")
    content_frame = driver.find_element(By.CSS_SELECTOR, 'frame[name="content"]')
    driver.switch_to.frame(content_frame)


def wait_for_content_to_load(driver):
    print("[DEBUG] Waiting for the frame to load.")
    WebDriverWait(driver, 60).until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "#DivAll > table:nth-child(19)")
        ),
        "The frame wasn't found.",
    )


def select_interval(driver, visible_text):
    print("[DEBUG] Setting the time interval to ", visible_text, ".")
    interval_select = Select(
        driver.find_element(
            By.CSS_SELECTOR,
            "#DivTit > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > select:nth-child(2)",
        )
    )

    interval_select.select_by_visible_text(visible_text)


def get_agenda_table_body(driver):
    print("[DEBUG] Retrieving the agenda body.")
    return driver.find_element(
        By.CSS_SELECTOR,
        "#DivVis > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1)",
    )


def setup_session():
    firefox_options = Options()

    firefox_options.headless = True

    driver = webdriver.Firefox(options=firefox_options)
    driver.get("https://esaip.alcuin.com/OpDotNet/Noyau/Login.aspx")

    login(driver)
    sleep(1)
    switch_to_agenda(driver)
    switch_to_content(driver)
    wait_for_content_to_load(driver)
    select_interval(driver, "Mois")
    wait_for_content_to_load(driver)
    print()

    return driver


def set_project(driver, project):
    id = PROJECTS[project]
    print(f"[DEBUG] Setting the project to {project}.")

    driver.execute_script(f"ModCal('{id}');")
    sleep(1)
    wait_for_content_to_load(driver)


def scrape(driver, project):
    set_project(driver, project)

    return get_agenda_table_body(driver)
