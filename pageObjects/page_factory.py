class PageObject:
    def __init__(self):
        self.home_page = {
            'login_field': ['XPATH', "//input[@name=\"username\"]"],
            'password_field': ['XPATH', "//input[@name=\"password\"]"],
            'submit_button': ['CSS', "//button[@type=\"submit\"]"],
        }

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