from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options

from time import sleep

from credentials import USERNAME, PASSWORD


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
    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "#DivAll > table:nth-child(19)")
        )
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


def scrape():
    firefox_options = Options()

    firefox_options.headless = True

    driver = webdriver.Firefox(options=firefox_options)
    driver.get("https://esaip.alcuin.com/OpDotNet/Noyau/Login.aspx")

    login(driver)
    switch_to_agenda(driver)
    switch_to_content(driver)
    wait_for_content_to_load(driver)
    select_interval(driver, "Mois")
    wait_for_content_to_load(driver)

    return get_agenda_table_body(driver)
