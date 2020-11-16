from selenium import webdriver
from csv import DictReader


class BrowserInit:
    """Creates an object of the WebDriver based on Browser passed
     (Ex. "Chrome", "Firefox", etc.) and gets a default url
    """
    extension = '.pomidor'

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def __repr__(self):
        return f'Pomidor object with {self.browser} browser and ' \
               f'{self.url} default url'

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

    def __init__(self, page_obj_file, urls=None):
        self.urls = urls
        self.page_obj_file = page_obj_file

    def __repr__(self):
        return f'Pomidor object with page object dictionary:\n' \
               f' {self.page_obj_file}' \
               f'and additional URL dictionary {self.urls}'

    def get_page_objects(self):
        with open(self.page_obj_file) as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',')
            obj_dict = {}
            for line_count, row in enumerate(csv_reader):
                obj_dict[row["name"]] = row["selector"], row["value"]
                # obj_dict = {rows['name']: (rows['selector'], row['value'])
                #             for rows in csv_reader}
        return obj_dict

# d = {}
# d["ff"] = "eferf", "fvdvfdv"
# print(d)
# mydict = {rows[0]:rows[1] for rows in reader}
