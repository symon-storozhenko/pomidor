class BaseURL:

    def __init__(self):
        self.urls = {
            'home_page': 'http://www.patreon.com',
            'reporting_page': 'https://www.google.com',
            'practice_page': 'https://pomidor-automation.com/practice/',
            'pomidor_home_url': 'https://pomidor-automation.com'

        }


class PageObject:
    def __init__(self):
        self.home_page = {
            # Home page:
            'practice_page': ['CSS_SELECTOR', 'button#menu'],
            'practice_menu_button': ['LINK_TEXT', 'Practice'],
            'non_existent_obj': ['LINK_TEXT', 'Yo'],

            # Practice page:
            'name_field': ['CSS_SELECTOR', 'input#name'],
            'back_home_button': ['CSS_SELECTOR', 'a.wp-block-button__link'],



            # pomidor-automation.com
            # Home page:

            # 'login_field': ['XPATH', "//input[@name=\"username\"]"],
            # 'password_field': ['XPATH', "//input[@name=\"password\"]"],
            # 'submit_button': ['CSS', "//button[@type=\"submit\"]"],
            # 'about_link': ['LINK_TEXT', "About"],
            # 'google_about_link': ['XPATH', "//a[text()=\'About\']"],
            # 'google_search_field': ['CSS_SELECTOR', "input[title=\'Search\']"],
            # 'search_field': ['XPATH',
            #                  '//*[@id="reactTarget"]/div/div[1]/div[2]/div/header/div[2]/ul/li[1]/div/a/div/div/form/div/div/div/div/input'],

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
