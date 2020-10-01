import functools
import pathlib
import re
from pomidor.actions import ForwardAction, BackwardAction
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time


class PomidorSyntaxError(Exception):
    """ Pomidor syntax error class. """

    def __init__(self, *args, **kwargs):
        pass


class PomidorObjectNotFound(Exception):
    """ Page object error class. """

    def __init__(self, *args, **kwargs):
        pass


print('\n\n-------\nSTART:\n-------\n\n')


def generate_list_of_pomidor_files(tomato_directory):
    """Goes through a gived directory and creates a list of filenames with
    .pomidor extension"""

    tomato_files_list = []
    tom_dir = pathlib.Path(tomato_directory)
    print(f'List of files: {tom_dir}')
    # one-file scenario
    if tomato_directory.endswith(Pomidor.extension):
        print('Fist!!')
        tomato_files_list.append(tomato_directory)
    for enum, path in enumerate(
            tom_dir.rglob(f'*{Pomidor.extension}')):  # or .glob('**/*.oat')
        tomato_files_list.append(path)
        print(f'{enum + 1}: {path}')
    # print(f'tomato_files_list -> {tomato_files_list}')
    if tomato_files_list == []:
        raise FileNotFoundError(f'No pomidor files found in the directory')
    return tomato_files_list


def define_test_paragraphs(scenarioSteps, filepath, frst_prgrph_line,
                           scenario_title_line_num, line_num,
                           obj_dict, driver, url, wait):
    """Goes over a particular test case paragraph and executes all actions"""

    latest_index = 0
    action_counter = 0
    obj_counter = 0
    tied_obj = False
    scenario_with_action = False
    str_in_quotes = re.findall(r"\'(.+?)\'", scenarioSteps)
    str_in_brackets = re.findall(r" \[(.+?)\]", scenarioSteps)
    print(f'str_in_brackets --> {str_in_brackets}')
    print(f"str_in_quotes --> {str_in_quotes} ")
    strList = re.split(r'[;,.!?\s]', scenarioSteps)
    # tom = Pomidor(browser, obj_dict, url)
    browser_initialized = False

    try:
        for position, strList_item in enumerate(strList[latest_index:]):
            object_found = False
            action_found = False
            if strList_item.startswith("*"):
                scenario_with_action = True
                print(f'\n-Printing from latest index in paragraph -->'
                      f'\n {strList[latest_index:]}')  # whole TC in one string
                backward_action = False
                act = ForwardAction()
                bact = BackwardAction()
                backward_action_dict = bact.backward_actions_dictionary
                forward_action_dict = act.forward_action_dictionary
                print(f'FOWRD dICT --> {forward_action_dict}')
                # Iterate over forward actions
                for action_in_bckwrd_list in backward_action_dict.keys():
                    if action_in_bckwrd_list == '*page_title':
                        pass
                    # look for backward action first
                    print(
                        f'SUCCESS -> for action_in_bckwrd_list in '
                        f'backward_actions_dict.keys():')
                    if strList_item.lower().startswith(action_in_bckwrd_list):
                        action_counter += 1
                        action_found = True
                        backward_action = True
                        action_index = position
                        action_item = action_in_bckwrd_list
                        bk_obj_count = 0
                        for page_objects in strList[latest_index:action_index]:
                            if page_objects.startswith(
                                    "#"):  # if back_obj is found
                                page_object = page_objects  # to prevent obj in
                                # front to reassign value
                                # print(f'Object is found! --> {page_object}')
                                object_found = True
                                bk_obj_count += 1
                            else:
                                continue
                        if bk_obj_count > 1:
                            raise PomidorSyntaxError(
                                """ Negative tested in file
                                'more_than_1_obj_bckwrd_action_except.pomidor' 
                                """

                                f'\nMore than one object is found! Make sure '
                                f'to put only one '
                                f'pertinent item before "{action_item}"'
                                f' (backward action) '
                                f'\nPlease review:"{frst_prgrph_line.strip()}"'
                                f'\nFile name --> {filepath}'
                                f'\nParagraph starts on line -->'
                                f' {scenario_title_line_num}.\n\n'
                                f'Examples:'
                                f'\n*Click on #page and #cart is *visible --> '
                                f'allowed \n '
                                f'*Click on #page and #profile and #cart is '
                                f'*visible --> '
                                f'NOT allowed')
                        else:
                            pass
                        break
                if action_found:
                    latest_index = action_index + 1
                    latest_artifact = strList_item
                if not action_found:
                    # Iterate over forward actions
                    for action_in_frwrd_lst in forward_action_dict:
                        # if forward action is found
                        if strList_item.lower(). \
                                startswith(action_in_frwrd_lst):
                            action_found = True
                            action_counter += 1
                            action_index = position
                            action_item = action_in_frwrd_lst
                            # search for any orphan objects
                            for orphan_obj in strList[latest_index:
                            action_index]:
                                if orphan_obj.startswith("#"):
                                    raise PomidorSyntaxError(
                                        """ Negative syntax to test located in
                                        'orphan_obj_b4_frwd_action.pomidor' 
                                        file"""

                                        f'\n\n{"*" * 58}\nOrphan object found '
                                        f'-> {orphan_obj}. Please associate an'
                                        f' action (*) with this object.\n '
                                        f'\nPlease review: '
                                        f'"{frst_prgrph_line.strip()}"'
                                        f'\nFile name --> {filepath}'
                                        f'\nParagraph starts on line --> '
                                        f'{scenario_title_line_num}')
                            for obj_position, page_object in enumerate(
                                    strList[action_index:]):  # frwd obj
                                if page_object.startswith("#"):
                                    # if obj is found
                                    object_found = True
                                    page_obj_index = position + obj_position
                                    latest_index = page_obj_index + 1
                                    for str_slice_item in strList[action_index
                                                                  + 1:page_obj_index]:
                                        if str_slice_item.startswith("*"):
                                            # if actions left by mistake
                                            raise PomidorSyntaxError(
                                                """ Negative tested with file 
                                                'two_actions.pomidor' """

                                                f'\n\n{"*" * 58}\nWhich action'
                                                f' to use with {page_object}? '
                                                f'{strList_item} (forward '
                                                f'action) or {str_slice_item} '
                                                f'(undefined vector action)? '
                                                f'\nPlease review: '
                                                f'"{frst_prgrph_line.strip()}'
                                                f'"\nFile name --> {filepath}'
                                                f'\nParagraph starts on line '
                                                f'{scenario_title_line_num}')
                                    break
                                else:
                                    object_found = False
                                    continue
                            break
                # Perform action on the object
                if not object_found:
                    raise PomidorSyntaxError(
                        """ Negative tested in file 'no_obj_found.pomidor' """

                        f'\n\n{"*" * 58}\nno object found for action '
                        f'"{strList_item}'
                        f'\nPlease review: "{filepath}",--> line {line_num}')
                else:
                    obj_counter += 1
                    tied_obj = True
                    page_object = page_object.strip('#')
                    print('                check dict first+++++++++++++++')
                    print(f'Action izz - > {action_item}')
                    if page_object not in obj_dict:
                        raise PomidorObjectNotFound(
                            """ Negative tested in file 
                            'obj_not_found_in_page_factory.pomidor' """

                            f'Page object is NOT Found! ---> '
                            f'#{page_object}'
                            f'\nPlease review: '
                            f'"{frst_prgrph_line.strip()}"'
                            f'\nFile name --> {filepath}'
                            f'\nParagraph starts on line --> '
                            f'{scenario_title_line_num + 1}.\n\n')
                    print(f'?????????????Object_source via Tomato class/PO -->'
                          f'{Pomidor.get_dict_obj(page_object)}')
                    page_object_src = obj_dict.get(page_object)[1]
                    page_obj_locator = obj_dict.get(page_object)[0]
                    print(f'page_object_src --> {page_object_src}')
                    print(f'page_obj_locator  --> {page_obj_locator}')
                    # if page_object_src not in
                    print(f'Latest index --> {latest_index}')
                    print(f"\nActions and Assertions performed:")
                    if not browser_initialized:
                        # and Pomidor.before_tests_launch_url.has_been_called:
                        pomidor = Pomidor(driver, obj_dict, url)
                        driver = pomidor.define_browser()
                        browser_initialized = True
                        driver.get(url)
                        driver.title
                        # driver.
                        if Pomidor.max_window.has_been_called:
                            driver.maximize_window()
                        if Pomidor.fullscreen.has_been_called:
                            driver.fullscreen_window()
                        if Pomidor.delete_all_cookies.has_been_called:
                            driver.delete_all_cookies()

                    # if forward or backward action
                    if backward_action:
                        act = backward_action_dict.get(action_item)
                    else:
                        act = forward_action_dict.get(action_item)
                    act_func, str_in_quotes = which_action(act,
                                                           page_object_src,
                                                           page_obj_locator,
                                                           str_in_quotes,
                                                           wait)
                    print(f'ZZZZ! -> act_func : {act_func}')
                    print(f'str_in quotes -> {str_in_quotes}')
                    print(driver)
                    if act == 'send_keys()':
                        exec(f'WebDriverWait(driver, '
                             f'{wait}).until(ec.element_to_be_clickable('
                             f'(By.{page_obj_locator}, '
                             f'\"{page_object_src}\"))).clear()')
                        # TODO add test verifying the content of send_keys()
                        # TODO add *text_value_is [of #page_obj] or #page_obj has *text_value of 'Blah'
                        # TODO add *page_title_is 'Practice - Pomidor Auto...'
                        # TODO create test paragraph skeleton - all actions are enumerated and
                        #  appropriate StrList index is used
                        time.sleep(1)
                    exec(act_func)
            elif strList_item.startswith('#') and not tied_obj:
                obj_counter += 1
                object_found = True
                object = strList_item
        if action_counter < 1:
            scenarioSteps = scenarioSteps.strip()
            scenario_with_action = False
            print(f'\nNo actions are found in test --> "'
                  f'{frst_prgrph_line.strip()}"\nFile name --> {filepath}.'
                  f'\nParagraph starts on line --> {scenario_title_line_num}.'
                  f'\nPlease add actions (*) and their objects (#), otherwise,'
                  f'comment out the whole paragraph with double dashes: "--" ')
        for obj_last in strList[latest_index:]:
            if obj_last.startswith('#'):
                raise PomidorSyntaxError(
                    """ Negative tested in file 'last_orphan_obj.pomidor' """

                    f'\n{"*" * 58}\nOrphan object found -> {obj_last}. '
                    f'Please '
                    f'associate an action (*) with this object.\n '
                    f'\nPlease review: "{frst_prgrph_line.strip()}"'
                    f'\nFile name --> {filepath}'
                    f'\nParagraph starts on line --> '
                    f'{scenario_title_line_num}')
        print('SCENARIO COMPLETED!!!!')
    finally:
        if browser_initialized:
            # Pomidor.quit.has_been_called and :
            # time.sleep(1)
            driver.quit()
            print('\nDriver QUIT!!\n')
        pass
    return scenario_with_action


def pomidor_pro_func(code_string, driver, obj_dict, url):
    """Not used..."""

    try:
        # and Pomidor.before_tests_launch_url.has_been_called:
        pomidor = Pomidor(driver, obj_dict, url)
        driver = pomidor.define_browser()
        browser_initialized = True
        driver.get(url)
        driver.title
        # driver.
        if Pomidor.max_window.has_been_called:
            driver.maximize_window()
        if Pomidor.fullscreen.has_been_called:
            driver.fullscreen_window()
        if Pomidor.delete_all_cookies.has_been_called:
            driver.delete_all_cookies()
    finally:
        if browser_initialized:
            # Pomidor.quit.has_been_called and :
            # time.sleep(1)
            driver.quit()
            print('\nDriver QUIT!!\n')
        pass


def go_thru_pomidor_file(func, obj_dict, driver, base_url, urls, wait):
    """Opens one .pomidor file at a time and picks test case paragraphs, one by
    one, top to bottom"""

    scenario_number = 0
    for file_number, filepath in enumerate(func):
        with open(filepath) as file:
            for total_lines_count, row in enumerate(file):
                continue
        with open(filepath) as tomato_file:
            print(f'\nOpening file --> {filepath}\n')
            scenarioSteps = ''
            first_paragraph_line = ''
            url = base_url
            for line_num, line in enumerate(tomato_file):
                if '@base_url' in line:
                    line_list = re.split(r'[;,.!?\s]', line)
                    ad_hoc_url = line_list[1]
                    url = urls.get(ad_hoc_url)
                    print(f'@base_url is caught -> {url}')
                if scenarioSteps == '' and (
                        line in ['\n', '\r\n'] or line.startswith('--')):
                    url = base_url
                else:
                    if scenarioSteps == '':
                        first_paragraph_line = line
                        scenario_title_line_num = line_num
                    if scenarioSteps != '' and line.startswith('--'):
                        continue
                    scenarioSteps += line
                if (scenarioSteps != '' and line in ['\n', '\r\n']) or (
                        scenarioSteps != '' and line_num == total_lines_count):
                    print(f'LINE IS -----> {line} at {line_num}')
                    print(
                        f"\nBegin test:\n ----{first_paragraph_line.strip()}"
                        f"----\n\n"
                        f"\nActions and Assertions performed:")
                    print(f'srtList --> {scenarioSteps}')
                    test_paragraph = \
                        define_test_paragraphs(scenarioSteps, filepath,
                                               first_paragraph_line,
                                               scenario_title_line_num,
                                               line_num, obj_dict, driver,
                                               url, wait)
                    if test_paragraph:
                        scenario_number += 1
                        url = base_url
                    scenarioSteps = ''
    return file_number, scenario_number


def go_thru_pomidor_file_with_story(func, feature_type, story, obj_dict,
                                    driver, base_url, urls,
                                    exact_story_name, wait):
    """Opens a .pomidor file, one at a time, and picks test case paragraphs
    marked with a passed @marker value (Ex."@story", "@feature" or your own
    custom marker, one by one, top to bottom"""

    scenario_number = 0
    for file_number, filepath in enumerate(func):
        with open(filepath) as file:
            for total_lines_count, row in enumerate(file):
                continue
        with open(filepath) as tomato_file:
            print(f'\nOpening file --> {filepath}\n')
            scenarioSteps = ''
            first_paragraph_line = ''
            feature_instances = 0
            line_counter = 0
            url = base_url
            pro = False
            first_pro_line = False
            browser_initialized = False
            for line_num, line in enumerate(tomato_file):
                if line == 0:
                    continue
                else:
                    line_counter += 1
                print(f'======= ===== General Line #{line_num}====== ======')
                # choose type of marker to run
                if '@base_url' in line:
                    line_list = re.split(r'[;,.!?\s]', line)
                    ad_hoc_url = line_list[1]
                    url = urls.get(ad_hoc_url)
                    print(f'@base_url is caught -> {url}')
                if feature_type.lower() in line.lower():
                    line_list = re.split(r'[;,.!?\s]', line)
                    print(f'{feature_type} \n\n++++++++STORY Line ! --> '
                          f'{line_list}++++++++++\n')
                    for f in line_list:
                        if exact_story_name:
                            if f == story:
                                print(f'Found exact {feature_type}!!!!!!!!')
                                feature_instances += 1
                        else:
                            if story.lower() in f.lower():
                                # or, f.lower().__contains__(story.lower()):
                                print(f'$@$$ FOUND {feature_type}! -> {f}\n')
                                print(f'Line before inner loop--> {line}')
                                feature_instances += 1
                if '@data' in line:
                    line_list = re.split(r'[;,.!?\s]', line)
                    ad_hoc_url = line_list[1]
                    url = urls.get(ad_hoc_url)
                    print(f'@data is caught -> ! {url}')
                if feature_instances > 0:
                    for line_num_in, line in enumerate(tomato_file,
                                                       line_counter):
                        line_counter += 1
                        print(f'Text "{line}" is on line num --> '
                              f'{line_num_in + 1}')

                        # if feature_bool:
                        if scenarioSteps == '' and (line in ['\n', '\r\n']
                                                    or line.startswith(
                                    '--')):  # .pomidor comment
                            continue
                        else:
                            if not pro and line.startswith('"""'):
                                print("@pro is found!")
                                pro = True
                                first_pro_line = True
                            if scenarioSteps == '':
                                print("after @pro is found!")
                                first_paragraph_line = line
                                scenario_title_line_num = line_num
                            if scenarioSteps != '' and line.startswith(
                                    '--'):
                                continue
                            if pro:
                                if first_pro_line:
                                    first_pro_line = False
                                else:
                                    print("@not""")
                                    scenarioSteps = scenarioSteps + line + '\n'
                                    print(f'!!scenarioSteps-> {scenarioSteps}')
                            else:
                                scenarioSteps += line
                                print("Captured wrong scenarioSteps!!")
                        if pro and (scenarioSteps != ''
                                     and line.startswith('"""')):
                            scenarioSteps = scenarioSteps.strip('\n"""')
                            print(f'PROscenarioSteps --> {scenarioSteps}')
                            try:
                                if not browser_initialized:
                                    # and Pomidor.before_tests_launch_url.has_been_called:
                                    pomidor = Pomidor(driver, obj_dict, url)
                                    driver = pomidor.define_browser()
                                    browser_initialized = True
                                    if Pomidor.max_window.has_been_called:
                                        driver.maximize_window()
                                    if Pomidor.fullscreen.has_been_called:
                                        driver.fullscreen_window()
                                    if Pomidor.delete_all_cookies.has_been_called:
                                        driver.delete_all_cookies()
                                    exec(scenarioSteps)
                                    time.sleep(1)
                            finally:
                                if browser_initialized:
                                    # browser_initialized = False
                                    # Pomidor.quit.has_been_called and :
                                    # time.sleep(1)
                                    driver.quit()
                                    print('\nDriver QUIT!!\n')
                                pass
                            pro = False
                            scenario_number += 1
                            scenarioSteps = ''
                            feature_instances = 0
                            break
                        if not pro and (scenarioSteps != ''
                                        and line in ['\n', '\r\n']) or (
                                scenarioSteps != '' and line_counter - 1 ==
                                total_lines_count + 1):
                            print(f'total_lines_count:{total_lines_count}')
                            print(f'LINE IS -----> {line} at '
                                  f'{line_num_in}')
                            print(
                                f"\nBegin test:\n ----"
                                f"{first_paragraph_line.strip()}----\n"
                                f"\nActions and Assertions performed:")
                            latest_index = 0
                            action_counter = 0
                            test_paragraph = define_test_paragraphs(
                                scenarioSteps, filepath,
                                first_paragraph_line,
                                scenario_title_line_num,
                                line_num, obj_dict, driver, url, wait)
                            if test_paragraph:
                                scenario_number += 1
                            scenarioSteps = ''
                            feature_instances = 0
                            break
                    else:
                        line_counter += 1
                        url = base_url
                        continue
                else:
                    continue
    return file_number, scenario_number


# packaging_tutorial
# ├── LICENSE
# ├── README.md
# ├── example_pkg
# │   └── __init__.py
# ├── setup.py
# └── tests

def list_all_mark_values(func, feature_type):
    """Function to list all needed test case paragraphs. No browser execution
    is performed"""

    scenario_number = 0
    marker_values = []
    for file_number, filepath in enumerate(func):
        with open(filepath) as file:
            for total_lines_count, row in enumerate(file):
                continue
        with open(filepath) as tomato_file:
            print(f'\nOpening file --> {filepath}\n')
            for line_num, line in enumerate(tomato_file):
                if feature_type.lower() in line.lower():
                    line = line.upper()
                    line_list = re.split(r'[;,.!?\s]', line)
                    print(f"line_list --> ((((({line_list}")
                    for i in line_list:
                        if i.startswith(feature_type.upper()):
                            line_list.remove(i)
                    marker_values += line_list
                    while "" in marker_values:
                        marker_values.remove("")
                    print(f'{feature_type.upper()} \n\n++++MARKER Line ! --> '
                          f'{marker_values}++++++++++\n')
    return marker_values, len(marker_values)

# Selenium action functions:

def action_func_visible(driver, act, obj_source, locator, wait):
    """Function to construct a string with expected condition:
    visibility_of_element_located"""

    return f'WebDriverWait(driver, {wait}).until(ec.visibility_of_' \
           f'element_located((By.{locator},\"{obj_source}\"))).{act}'


def send_keys_func(str_list):
    """Function to construct a string:
        send_keys(str_list[0]"""

    print(f'str_list  before ++ {str_list}')
    str_list = list(str_list)
    keys_to_send = str_list[0]
    str_list.pop(0)
    print(f'str_list ++ {str_list}')
    return f"send_keys(\"{keys_to_send}\")", str_list


def action_func_clickable(act, obj_source, locator, str_list, wait):
    """Function to construct a string with expected condition:
        element_to_be_clickable"""

    if act == "click()" or act == "send_keys()":
        if act == "send_keys()":
            act, str_list = send_keys_func(str_list)

    return f'WebDriverWait(driver, {wait}).until(ec.element_to_be_' \
           f'clickable((By.{locator}, \"{obj_source}\"))).{act}', str_list


def click(act, element):
    return f'{element}.{act}'


def which_action(act, obj_source, locator, str_list, wait):
    """Function to determine which action type need to be used, based on the
    selenium action"""

    print(f'str_list  in which action ++ {str_list}')
    if act == "click()" or act == "send_keys()":
        func, str_list = action_func_clickable(act, obj_source, locator,
                                               str_list, wait)
    else:
        func = action_func_visible(act, obj_source, locator, wait)
    return func, str_list


def trackcalls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.has_been_called = True
        return func(*args, **kwargs)

    wrapper.has_been_called = False
    return wrapper


class Pomidor:
    """A class needed for user to create an object of with the below passed:
    1. Webdriver type (Ex. "Chrome", "Firefox", etc.)
    2. Pass page objects as an instance of user PageObject class
    3. Pass default url
    4. Pass a dict with additional urls"""

    extension = '.pomidor'

    def __init__(self, driver, obj_dict, url, urls=None):
        self.urls = urls
        self.obj_dict = obj_dict
        self.url = url
        self.driver = driver

    def __repr__(self):
        return f'Pomidor object with page object dictionary:\n' \
               f' {self.obj_dict}' \
               f'and driver {self.driver}'

    @trackcalls
    def before_tests_launch_url(self):
        pass

    def define_browser(self):
        if self.driver.capitalize() == 'Chrome':
            driver = webdriver.Chrome()
        if self.driver.capitalize() == 'Firefox':
            driver = webdriver.Firefox()
        return driver

    @trackcalls
    def close(self):
        self.driver.close()

    @trackcalls
    def quit(self):
        pass

    @trackcalls
    def max_window(self):
        pass

    @trackcalls
    def fullscreen(self):
        pass

    @trackcalls
    def delete_all_cookies(self):
        pass

    def run_scripts(self, dir_path, verbose=True, wait=10):
        file_num, scenario_number = go_thru_pomidor_file(
            generate_list_of_pomidor_files(dir_path), self.obj_dict,
            self.driver, self.url, self.urls, wait)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_num + 1}')  #
            print(f'Number of scenarios --> {scenario_number}')
        return scenario_number

    def run_features(self, dir_path, feature_value, exact_match=False,
                     verbose=True, before_test=None,
                     after_test=None, wait=10):
        file_number, scenario_number = go_thru_pomidor_file_with_story(
            generate_list_of_pomidor_files(dir_path), "@feature",
            feature_value,
            self.obj_dict, self.driver, self.url, self.urls, exact_match, wait)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_number + 1}')  #
            print(f'Number of scenarios --> {scenario_number}')
        return scenario_number

    def run_story(self, dir_path, feature_value, exact_match=False,
                  verbose=True, before_test=None,
                  after_test=None, wait=10):
        file_num, scenario_number = go_thru_pomidor_file_with_story(
            generate_list_of_pomidor_files(dir_path), "@story",
            feature_value, self.obj_dict, self.driver, self.url, self.urls,
            exact_match, wait)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_num + 1}')  #
            print(f'Number of scenarios --> {scenario_number}')
        return scenario_number

    def run_custom_identifier(self, dir_path, feature_type, feature_value,
                              exact_match=False, verbose=True, wait=2):
        file_num, scenario_number = go_thru_pomidor_file_with_story(
            generate_list_of_pomidor_files(dir_path), feature_type,
            feature_value, self.obj_dict, self.driver, self.url, self.urls,
            exact_match, wait)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_num + 1}')  #
            print(f'Number of scenarios --> {scenario_number}')
        return scenario_number

    @staticmethod
    def list_all_marker_values(dir_path, feature_type):
        marker_list, markers_num = list_all_mark_values(
            generate_list_of_pomidor_files(dir_path), feature_type)
        print(f'{feature_type} total list : {marker_list}')
        print(f"There're {markers_num} values found total")
        print(f"\nUnique {feature_type} list: {set(marker_list)}")
        print(f"Unique number of {feature_type} is {len(set(marker_list))}")
        return markers_num, len(set(marker_list))

    @staticmethod
    def run_standalone_custom_identifier(dir_path, feature_value,
                                         exact_story_name=False,
                                         verbose=True):
        file_num, scenario_number = go_thru_pomidor_file_with_story(
            generate_list_of_pomidor_files(dir_path),
            feature_value, exact_story_name)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_num + 1}')  #
            print(f'Number of scenarios --> {scenario_number}')

    @staticmethod
    def how_many_files(dir_path):
        a = generate_list_of_pomidor_files(dir_path)

    @staticmethod
    def get_dict_obj(obj_key):  # Needed to print only
        pass