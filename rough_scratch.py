from pageObjects.page_factory import PageObject, BaseURL
from pomidor.pomidor_runner import Pomidor
from pomidor.pomidor_runner import PomidorSyntaxError, PomidorObjectNotFound
import pytest
import selenium.webdriver.chrome.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.get('https://www.google.com')
WebDriverWait(<selenium.webdriver.chrome.webdriver.WebDriver (session="bd0dfb95633cdd74a5c1afbcb26589fe")>, 10).until(ec.element_to_be_clickable((By.XPATH,"//a[text()='About']"))).click()
driver.quit()