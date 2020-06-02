class PageObject:
    def __init__(self, obj):
        self.home_page = {
            'login_field': ['XPATH', "//input[@name=\"username\"]"],
            'password_field': ['XPATH', "//input[@name=\"password\"]"],
            'submit_button': ['CSS', "//button[@type=\"submit\"]"],
        }[obj]


po = PageObject('login_field')
if True:
    print('hey!', po.home_page,  po.__dict__.keys())