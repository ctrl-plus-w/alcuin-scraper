from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

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


def main():
    driver = webdriver.Firefox()
    driver.get("https://esaip.alcuin.com/OpDotNet/Noyau/Login.aspx")

    login(driver)
    switch_to_agenda(driver)

    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, 'frame[name="content"]')
        )
    )

    content_frame = driver.find_element(By.CSS_SELECTOR, 'frame[name="content"]')
    driver.switch_to.frame(content_frame)

    driver.get_screenshot_as_file("temp.png")


# agenda = driver.find_element(
#     By.CSS_SELECTOR,
#     "#DivVis > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1)",
# )
# print(agenda)


if __name__ == "__main__":
    main()
