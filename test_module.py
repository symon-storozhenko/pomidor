from pageObjects.page_factory import PageObject
from pomidor.pomidor_runner import Pomidor

po = PageObject()
to = Pomidor(po.home_page)
# print(f'to is --> {to.obj_dict}')
# keyy = 'login_field'
# loc = to.get_dict_obj(keyy)
# source = to.get_dict_obj(keyy)
# Pomidor.get_dict_obj(keyy)
# locators = list(Pomidor.pull_objects(po.home_page))
# Pomidor.pull_objects(po.home_page.get(keyy)[1])

# print(f'Locators! {loc}')

all_tomato_scripts = '/Users/myco/PycharmProjects/tomato3/tomatoes'
one_file = '/Users/myco/PycharmProjects/tomato3/tomatoes/TestCase.pomidor'
# to.run_scripts(all_tomato_scripts, verbose=True) # todo block the print output
# to.run_features(one_file, "E_Page")
# to.run_story(one_file, "jiRA")  # , exact_story_name=True)
#
# print("Hey!")
# to.run_custom_identifier(all_tomato_scripts, 'reporting', 'h')    # TODO - implement dry_run=True option
# print(one_file.endswith('.pomidor'))
# print(f'page Object dict is --> {to.obj_dict}')
# print(to)
# Pomidor.how_many_files(all_tomato_scripts)
#
#
def run_smoke_test(pomidor_function):  # TODO implement concurrency with pytest
    pomidor_function
    print(f'Smoke test passed!')


run_smoke_test(to.run_scripts(one_file))
