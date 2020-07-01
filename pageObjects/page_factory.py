class BaseURL:

    def __init__(self):
        self.urls = {
            'home_page': 'http://www.patreon.com',
            'reporting_page': 'https://www.google.com'
        }

class PageObject:
    def __init__(self):
        self.home_page = {
            'login_field': ['XPATH', "//input[@name=\"username\"]"],
            'password_field': ['XPATH', "//input[@name=\"password\"]"],
            'submit_button': ['CSS', "//button[@type=\"submit\"]"],
            'about_link': ['LINK_TEXT', "About"],
            'search_field':['XPATH', '//*[@id="reactTarget"]/div/div[1]/div[2]/div/header/div[2]/ul/li[1]/div/a/div/div/form/div/div/div/div/input']
        }

    # available locators:
    # ID = "id"
    # XPATH = "xpath"
    # LINK_TEXT = "link text"
    # PARTIAL_LINK_TEXT = "partial link text"
    # NAME = "name"
    # TAG_NAME = "tag name"
    # CLASS_NAME = "class name"
    # CSS_SELECTOR = "css selector"


    # def get_obj(self):


# poc = PageObject()
# keyy = 'login_field'
# if poc.home_page.__contains__('login_field'):
#     print('Success!')
#     print(f'{poc.home_page}')
#
# if 'login_field' in poc.home_page:
#     print('Yoyoy!')
#     print(f'login_field --> {poc.home_page.get(keyy)[1]}')
#     print(f'{poc.home_page.items()}')
#
#     # locators = list(Pomidor.pull_objects(po.home_page.items()).values())

# if True:
#     print('hey!', po.home_page,  po.__dict__.keys())