from tomato.tomato2 import Tomato

all_tomato_scripts = '/Users/myco/PycharmProjects/tomato3/tomatoes'  # Todo handle passing 1 file
# Tomato.run_scripts(all_tomato_scripts, verbose=True) # todo handle blocking the print output from inside functions
# Tomato.run_features(all_tomato_scripts, "Home_Page")
Tomato.run_story(all_tomato_scripts, "99")  # , exact_story_name=True)
print("Hey!")
