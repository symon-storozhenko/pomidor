from pageObjects.page_factory import PageObject, BaseURL
from pomidor.pomidor_runner import Pomidor
from pomidor.pomidor_runner import PomidorSyntaxError, PomidorObjectNotFound
import pytest
import selenium.webdriver.chrome.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time

art_url = 'http://www.patreon.com'
home_page ='http://www.patreon.com'
earnings_page = 'https://www.patreon.com/dashboard/earnings'

po = PageObject()
burl = BaseURL()
# chrome_driver = webdriver.Chrome()
pomi = Pomidor('Chrome', po.home_page, art_url, burl.urls)
# TODO - initialize Pomidor without base_url
# TODO - initialize Pomidor object without browser?
# TODO - implement @base_url marker


print(f'POMI -> {pomi}')
pomi.before_tests_launch_url()
pomi.quit()

hello_world_path = '/Users/myco/PycharmProjects/tomato3/tomatoes/' \
                  'hello_world.pomidor'

pomi.run_scripts(hello_world_path)
