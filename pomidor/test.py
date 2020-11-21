from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pomidor.pomidor_init import BrowserInit, PomidorObjAndURL, Pom
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from pomidor.actions import ForwardAction, BackwardAction

# pomi = BrowserInit("Chrome", 'https://pomidor-automation.com/')
# driver = pomi.define_browser()
# with driver as d:
#     d.get('https://pomidor-automation.com/practice/')

act = ForwardAction()
bact = BackwardAction()
backward_action_dict = bact.backward_actions_dictionary
forward_action_dict = act.forward_action_dictionary

d = backward_action_dict.keys()
print(d)

for item in forward_action_dict.values():
    print(item)

if "click()" in forward_action_dict.keys():
    print("yay!")

url = 'https://pomidor-automation.com/'

driver = webdriver.Chrome()
driver.get(url)

try:

    practice_btn = driver.find_element_by_link_text("Practice")
    assert practice_btn.is_displayed()

    practice_btn.click()

    name_field = driver.find_element_by_css_selector("input#name")
    assert name_field.is_displayed()
    print("name_field is displayed")

    # fake_obj = driver.find_element_by_link_text("Fake")
    # back_home_button, CSS_SELECTOR, a.wp - block - button__link
    back_home_button = driver.find_element_by_css_selector("a.wp-block-button__link")
    # back_home_button.is_displayed()
    WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.CSS_SELECTOR,
                                                "va.wp-block-button__link")))
    print("back_home_button is displayed")

    name_field = driver.find_element_by_css_selector("input#name")
    assert name_field.is_displayed()

finally:
    driver.quit()
