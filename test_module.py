from tomato.tomato2 import Tomato

all_tomato_scripts = '/Users/myco/PycharmProjects/tomato3/tomatoes'  # Handled passing 1 file !!
one_file = '/Users/myco/PycharmProjects/tomato3/tomatoes/TestCase.pomidor'
# Tomato.run_scripts(all_tomato_scripts, verbose=True) # todo handle blocking the print output from inside functions
# Tomato.run_features(one_file, "E_Page", exact_story_name=False)
# Tomato.run_story(one_file, "jiRA")  # , exact_story_name=True)
print("Hey!")
# Tomato.how_many_files(one_file)
Tomato.run_custom_identifier(one_file, 'reporting', 'reporting')
print(one_file.endswith('.tomato'))
