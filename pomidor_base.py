import functools
from pathlib import Path



class PomidorSyntaxError(Exception):
    """ Pomidor syntax error class. """

    def __init__(self, *args, **kwargs):
        pass


class PomidorObjectNotFound(Exception):
    """ Page object error class. """

    def __init__(self, *args, **kwargs):
        pass


# class Pomidor:
#     """A class needed for user to create an object of with the below passed:
#     1. Webdriver type (Ex. "Chrome", "Firefox", etc.)
#     2. Pass page objects as an instance of user PageObject class
#     3. Pass default url
#     4. Pass a dict with additional urls"""
#
#     extension = '.pomidor'
#
#     def __init__(self, browser, obj_dict, url, urls=None):
#         self.urls = urls
#         self.obj_dict = obj_dict
#         self.url = url
#         self.browser = browser
#
#
# print(Pomidor.extension)
extension = '.pomidor'


def generate_list_of_pomidor_files(tomato_directory):
    """Goes through a given directory and creates a list of filenames with
    .pomidor extension"""

    tomato_files_list = []
    tom_dir = Path(tomato_directory)
    print(f'Directory: {tom_dir}')
    # one-file scenario
    # if tomato_directory.endswith(Pomidor.extension):
    #     tomato_files_list.append(tomato_directory)
        # list(p.glob('**/*.py'))
    print('List:')
    print(list(tom_dir.glob('**/*.pomidor')))
    for enum, path in enumerate(tom_dir.glob(f'**/*{extension}')):
        # (tom_dir.rglob(f'*{Pomidor.extension}')):  # or
        tomato_files_list.append(path)
        print(f'{enum + 1}: {path}')

    print(f'tomato_files_list -> {tomato_files_list}')
    if not tomato_files_list:
        raise FileNotFoundError(f'No pomidor files found in the directory')
    return tomato_files_list


generate_list_of_pomidor_files('tests')
