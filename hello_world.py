from pageObjects.page_factory import PageObject
from pomidor.pomidor_runner import Pomidor
from pomidor.pomidor_runner import PomidorSyntaxError, PomidorObjectNotFound
import pytest
import selenium.webdriver.chrome.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

po = PageObject()
driver = webdriver.Chrome()
pomi = Pomidor(driver, po.home_page)


hello_world_url = '/Users/myco/PycharmProjects/tomato3/tomatoes/' \
                  'hello_world.pomidor'


pomi.before_test('http://www.google.com')
pomi.after_test()
# pomi.after_test(driver)

pomi.run_scripts(hello_world_url)

if pomi.before_test.has_been_called:
    print("YEAH!")
