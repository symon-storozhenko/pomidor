import concurrent.futures
import functools
import pathlib
import re
from csv import DictReader
import itertools

import pytest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from pomidor.actions import ForwardAction, BackwardAction
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time


class PomidorSyntaxErrorTooManyActions(Exception):
    """ Pomidor syntax error class. """

    def __init__(self, *args, **kwargs):
        print("You have more actions than objects")

class PomidorSyntaxErrorTooManyObjects(Exception):
    """ Pomidor syntax error class. """

    def __init__(self, *args, **kwargs):
        print("You have more objects than actions")

class PomidorObjectNotFound(Exception):
    """ Page object error class. """

    def __init__(self, *args, **kwargs):
        pass

class PomidorObjectDoesNotExistOnPage(Exception):
    """ Pomidor syntax error class. """

    def __init__(self, *args, **kwargs):
        print("Page object does not exist on the page. Please check page "
              "object selector and value")

def generate_list_of_pomidor_files(tomato_directory: str) -> list:
    """Goes through a given directory and creates a list of filenames with
    .pomidor extension"""
    tomato_files_list = []
    tom_dir = pathlib.Path(tomato_directory)
    print(f'List of files: {tom_dir}')
    # one-file scenario
    if tomato_directory.endswith(Pomidor.extension):
        tomato_files_list.append(tomato_directory)
    for enum, path in enumerate(
            tom_dir.rglob(f'*{Pomidor.extension}')):  # or .glob('**/*.oat')
        tomato_files_list.append(path)
        print(f'{enum + 1}: {path}')
    # print(f'tomato_files_list -> {tomato_files_list}')
    if not tomato_files_list:
        raise FileNotFoundError(f'No pomidor files found in the directory')
    return tomato_files_list


class PomidorInit:
    """Creates an object of with the WebDriver based on Browser passed
     (Ex. "Chrome", "Firefox", etc.)
    """

    extension = '.pomidor'

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def __repr__(self):
        return f'Pomidor object with {self.browser} browser'

    def define_browser(self):
        if self.browser == 'Chrome':
            with webdriver.Chrome() as driver:
                driver.get(self.url)
        if self.browser == 'Firefox':
            with webdriver.Firefox() as driver:
                driver.get(self.url)
        return driver


act = ForwardAction()
bact = BackwardAction()
backward_action_dict = bact.backward_actions_dictionary
forward_action_dict = act.forward_action_dictionary


def execute_test_paragraph(scenarioSteps, filepath, frst_prgrph_line,
                           scenario_title_line_num, line_num,
                           obj_dict, driver, url, wait) -> str:
    type_list = ['type', 'types', 'typed']
    send_key_str = []
    str_in_brackets = re.findall(r" \[\[(.+?)\]\]", scenarioSteps)
    str_in_angle_brackets = re.findall(r"<<(.+?)>>", scenarioSteps)
    str_list = re.split(r'[;,.!?\s]', scenarioSteps)
    print(f'str_list -> {str_list}')
    actions = [x.lower() for x in str_list
               if x.lower() in backward_action_dict or \
               x.lower() in forward_action_dict]

    print(f'actions - > {actions}')
    objects = [y.strip("#") for y in str_list
               if y.startswith("#")]
    print(f'objects -> {objects}')
    if len(actions) > len(objects):
        raise PomidorSyntaxErrorTooManyActions
    elif len(objects) > len(actions):
        raise PomidorSyntaxErrorTooManyObjects

    obj_source = [obj_dict.get(i) for i in objects]
    print(f'obj_source -> {obj_source}\n\n')
    if None in obj_source:
        raise PomidorObjectDoesNotExistOnPage
    act_obj_list = [list(a) for a in zip(actions, obj_source)]
    print(f'act_obj_list -> {act_obj_list}\n\n')

    for i in act_obj_list:
        print(f'i in act_obj_list -> {i}')

        print(f'\nact -> {i[0]}')
        print(f'\npage_obj_locator -> {i[1][0]}')
        print(f'\npage_object_src -> {i[1][1]}')

    try:
        pomidor = Pomidor(driver, obj_dict, url)
        driver = pomidor.define_browser()
        driver.get(url)

        for i in act_obj_list:
            acti = i[0]
            page_obj_loc = i[1][0]
            page_object_src = i[1][1]
            act_func, str_in_quotes = which_action(
                acti, page_object_src, page_obj_loc, str_in_brackets, wait)
            if acti.startswith("type"):
                exec(f'WebDriverWait(driver, '
                     f'{wait}).until(ec.element_to_be_clickable('
                     f'(By.{page_obj_loc},\"{page_object_src}\"))).clear()')
                # TODO add is_selected and is_enabled asserts
                # TODO add "page_title" assert

                time.sleep(1)
            print(f'act_func -> {act_func}')
            exec(act_func)

    finally:
        driver.quit()


def go_thru_pomidor_file(func, feature, obj_dict,
                         driver, base_url, urls, wait):
    """Opens a .pomidor file, one at a time, and picks test case paragraphs
    marked with a passed @marker value (Ex."@story", "@feature" or your own
    custom marker, one by one, top to bottom"""
    scenario_number = 0
    for file_number, filepath in enumerate(func):
        spl = get_all_file_paragraphs_into_list(filepath)
        counter = 1
        line_num = 1
        for x in spl:
            print(f'counter -> {len(x) + 1}')

            markers_list = [y.lower() for y in x if y.startswith("@")]
            print(f'markers -> {markers_list}')

            # process all markers with markers_list
            feature_mark = ''.join([x.split()[1].strip(r'[;,]') for x in markers_list
                                    if x.startswith("@feature")])
            print(f'feature_mark -> {feature_mark}')

            url = base_url
            url_mark = ''.join([x.split()[1] for x in markers_list
                                if x.startswith("@url")])
            print(f'url_mark -> {url_mark}')
            if url_mark:
                if url_mark.startswith("http") and "://" in url_mark:
                    print(f'@url is caught - {url}')
                    url = url_mark
                else:
                    print(f'Extra @url is caught -> {url}')
                    url = urls.get(url_mark)
                    print(f'final url -> {url}')

            test_case = [y for y in x if not y.startswith("@")
                         and not y.startswith("!!")]
            print(f'test_case -> {test_case}')
            test_case_str = ' '.join([str(i) for i in test_case])
            print(f'test_case_string -> {test_case_str}')

            first_paragraph_line = ''.join(test_case[0])
            print(f'first_paragraph_line -> {first_paragraph_line}')
            scenario_title_line_num = counter + (len(x) + 1)
            print(f'scenario_title_line_num -> {scenario_title_line_num}')

            scenario_number = run_all_or_feature(
                driver, feature, feature_mark,
                filepath,
                first_paragraph_line,
                line_num, obj_dict,
                scenario_number,
                scenario_title_line_num,
                test_case_str, url, wait)

    return file_number, scenario_number


def run_all_or_feature(driver, feature, feature_mark, filepath,
                       first_paragraph_line, line_num, obj_dict,
                       scenario_number, scenario_title_line_num,
                       test_case_str,
                       url, wait):
    if feature:
        if feature_mark == feature.lower():
            test_p = execute_test_paragraph(
                test_case_str, filepath, first_paragraph_line,
                scenario_title_line_num, line_num, obj_dict, driver,
                url, wait)
            print(f'scenario_with_action - {test_p}')
            scenario_number += 1
        else:
            pass
    else:
        test_p = execute_test_paragraph(
            test_case_str, filepath, first_paragraph_line,
            scenario_title_line_num, line_num, obj_dict, driver,
            url, wait)
        scenario_number += 1
        print(f'scenario_with_action - {test_p}')
    return scenario_number


def get_all_file_paragraphs_into_list(filepath):
    with open(filepath) as file:
        list_of_file = file.read().splitlines()
        print(f'list_of_file --> {list_of_file}')

        # get all paragraphs of a file as a list of lists
        spl = [list(y)
               for x, y
               in itertools.groupby(list_of_file, lambda z: z == '')
               if not x]
        print(f'spl -> {spl}')
    return spl


def url_marker(line, url, urls):
    line_list = re.split(r'[;,.!?\s]', line)
    ad_hoc_url = line_list[1]
    print(f'ad_hoc_url is -> {ad_hoc_url}')
    if ad_hoc_url.startswith("http") and "://" in ad_hoc_url:
        print(f'@url is caught - {url}')
        url = ad_hoc_url
    else:
        print(f'Extra @url is caught -> {url}')
        url = urls.get(ad_hoc_url)
    return url


def feature_marker(feature, feature_instances, line) -> object:
    line_list = re.split(r'[;,.!?\s]', line)
    for f in line_list:
        if feature.lower() == f.lower():
            # or, f.lower().__contains__(story.lower()):
            print(f'$@$$ FOUND {feature}! -> {f}\n')
            feature_instances += 1
    return feature_instances


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

def assert_negative(act, obj_source, locator, wait):
    return f'with pytest.raises(TimeoutException):\n\t' \
           f'WebDriverWait(driver, {wait}).until(ec.visibility_of_' \
           f'element_located((By.{locator},\"{obj_source}\"))).{act}'


def action_func_visible(act, obj_source, locator, wait):
    """Function to construct a string with expected condition:
    visibility_of_element_located"""
    actb = backward_action_dict.get(act)
    if act.lower().startswith('not'):
        return f'with pytest.raises(TimeoutException):\n\t' \
               f'WebDriverWait(driver, {wait}).until(ec.visibility_of_' \
               f'element_located((By.{locator},\"{obj_source}\"))).{act}'
    else:
        return f'WebDriverWait(driver, {wait}).until(ec.visibility_of_' \
               f'element_located((By.{locator},\"{obj_source}\"))).{actb}'


def send_keys_func(str_list):
    """Function to construct a string:
        send_keys(str_list[0]"""

    # print(f'str_list  before ++ {str_list}')
    str_list = list(str_list)
    keys_to_send = str_list[0]
    str_list.pop(0)
    # print(f'str_list ++ {str_list}')
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

    print(f'str_list  in which action {act} ++ {str_list}')
    if act.lower().startswith('click') or act.lower().startswith('type'):
        actf = forward_action_dict.get(act)
        func, str_list = action_func_clickable(actf, obj_source, locator,
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
        # self.obj_repo = self.get_page_objects()

    def __repr__(self):
        return f'Pomidor object with page object dictionary:\n' \
               f' {self.obj_dict}' \
               f'and driver {self.driver}'

    @classmethod
    def get_page_objects(cls, obj_d: str) -> dict:
        with open(obj_d) as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',', quotechar='"')
            obj_dicto = {rows['name'].strip(): (rows['selector'].strip(),
                                                rows['value']) for rows in
                         csv_reader}
        return obj_dicto

    @classmethod
    def additional_urls(cls, urls_file: str) -> dict:
        with open(urls_file) as csv_url_file:
            csv_reader = DictReader(csv_url_file, delimiter=',', quotechar='"')
            url_dict = {rows['name'].strip(): rows['url'].strip() for rows in
                        csv_reader}
        return url_dict

    def get_obj_param(self, obj_name):
        obj_dict = self.get_page_objects()
        page_obj_src = obj_dict.get(obj_name)[0]
        page_obj_val = obj_dict.get(obj_name)[1]
        return page_obj_src, page_obj_val

    @trackcalls
    def before_tests_launch_url(self):
        pass

    @trackcalls
    def define_browser(self):
        if self.driver == 'Chrome':
            # chrome_options = Options()
            # chrome_options.add_argument("--headless")
            # driver = webdriver.Chrome(options=chrome_options)
            driver = webdriver.Chrome()
        if self.driver == 'Firefox':
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

    def run(self, dir_path, feature=False, verbose=True, wait=10):
        file_number, scenario_number = go_thru_pomidor_file(
            generate_list_of_pomidor_files(dir_path), feature,
            self.obj_dict, self.driver, self.url, self.urls, wait)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_number + 1}')  #
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
        file_num, scenario_number = go_thru_pomidor_file(
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
