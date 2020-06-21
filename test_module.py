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
one_file = 'tomatoes/TestCase.pomidor'
# to.run_scripts(all_tomato_scripts, verbose=True) # todo block the print output
no_obj_found = '/Users/myco/PycharmProjects/tomato3/negative_pomidory/'\
                         'no_obj_found.pomidor'
last_line_3_scenarios = '/Users/myco/PycharmProjects/tomato3/negative_pomidory/'\
                         'last_line_is_read.pomidor'

scratch = '/Users/myco/PycharmProjects/tomato3/negative_pomidory/'\
                         'scratch.pomidor'

to.list_all_marker_values(all_tomato_scripts, "featu")
to.run_custom_identifier(all_tomato_scripts, 'When', 'I')
# to.run_scripts(one_file)
# to.run_story(one_file, '3344')
# to.run_features(one_file, "E_Page")
# to.run_story(one_file, "jira-3344", exact_story_name=True)
#
# print("Hey!")
# to.run_custom_identifier(all_tomato_scripts, 'reporting', 'h')    # TODO - implement dry_run=True option
# print(one_file.endswith('.pomidor'))
# print(f'page Object dict is --> {to.obj_dict}')
# print(to)
# Pomidor.how_many_files(all_tomato_scripts)
#
#
# def run_smoke_test(pomidor_function):  # TODO implement concurrency with pytest
#     pomidor_function
#     print(f'Smoke test passed!')


# run_smoke_test(to.run_scripts(one_file))
