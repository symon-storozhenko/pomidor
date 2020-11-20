from selenium import webdriver
from csv import DictReader


class BrowserInit:
    """Creates an object of the WebDriver gets a default url"""
    extension = '.pomidor'

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def __repr__(self):
        return f'Pomidor object with {self.browser} browser and ' \
               f'{self.url} default url'

    def return_url(self, url):
        return self.url

    def define_browser(self):
        if self.browser == 'Chrome':
            driver = webdriver.Chrome()
            driver.get(self.url)
        if self.browser == 'Firefox':
            driver = webdriver.Firefox()
            driver.get(self.url)
        return driver


class PomidorObjAndURL:
    """Class for keeping a page objects repo and additional urls"""

    def __init__(self, page_obj_file, urls_file=None):
        self.urls_file = urls_file
        self.page_obj_file = page_obj_file

    def __repr__(self):
        return f'Pomidor object with page object dictionary:\n' \
               f' {self.page_obj_file}' \
               f'and additional URL dictionary {self.urls}'

    def get_page_objects(self):
        with open(self.page_obj_file) as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',', quotechar='"')
            obj_dict = {rows['name'].strip(): (rows['selector'].strip(),
                        rows['value']) for rows in csv_reader}
        return obj_dict

    def addt_urls(self):
        with open(self.urls_file) as csv_url_file:
            csv_reader = DictReader(csv_url_file, delimiter=',', quotechar='"')
            url_dict = {rows['name'].strip(): rows['url'].strip() for rows in
                        csv_reader}
        return url_dict

    def get_obj_param(self, obj_name):
        obj_dict = self.get_page_objects()
        page_obj_src = obj_dict.get(obj_name)[0]
        page_obj_val = obj_dict.get(obj_name)[1]
        return page_obj_src, page_obj_val


class Pom:

    def __init__(self, browser, url, page_obj, urls=None):
        self.browser = browser
        self.url = BrowserInit.return_url(url)
        self.page_obj = PomidorObjAndURL.get_page_objects(page_obj)

        driver = BrowserInit.define_browser(browser)