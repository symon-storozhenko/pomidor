from tomato.tomato2 import Tomato

all_tomato_scripts = '/Users/myco/PycharmProjects/tomato3/tomatoes'  # Handled passing 1 file !!
one_file = '/Users/myco/PycharmProjects/tomato3/tomatoes/TestCase.tomato'
Tomato.run_scripts(one_file, verbose=True) # todo handle blocking the print output from inside functions
Tomato.run_features(one_file, "Home_Page")
Tomato.run_story(one_file, "jiRA")  # , exact_story_name=True)
print("Hey!")
Tomato.how_many_files(one_file)
print(one_file.endswith('.tomato'))
