import concurrent.futures
import functools
import time
import traceback

import pytest
import pathlib
import re
from csv import DictReader
from concurrent.futures import ThreadPoolExecutor
import itertools
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from pomidor.actions import ForwardAction, BackwardAction
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
from pomidor.pomidor_exceptions import PomidorDataFeedNoKeyError, \
    PomidorDataFeedNoAngleKeysProvided, PomidorDataFeedNoCSVFileProvided, \
    PomidorFileNotFoundError, PomidorSyntaxErrorTooManyActions, \
    PomidorSyntaxErrorTooManyObjects, PomidorObjectDoesNotExistInCSVFile, \
    Colors, PomidorObjectDoesNotExistOnPage, \
    PomidorPrerequisiteScenarioNotFoundError


def generate_list_of_pomidor_files(tomato_directory: str) -> list:
    """Goes through a given directory and creates a list of filenames with
    .pomidor extension"""
    tomato_files_list = []
    tom_dir = pathlib.Path(tomato_directory)
    # single-file scenario
    if tomato_directory.endswith(Pomidor.extension):
        tomato_files_list.append(tomato_directory)
    for enum, path in enumerate(
            tom_dir.rglob(f'*{Pomidor.extension}')):
        tomato_files_list.append(path)
    if not tomato_files_list:
        raise PomidorFileNotFoundError(tom_dir)
    return tomato_files_list


def go_thru_one_file(base_url, driver, feature, story, filepath, obj_dict,
                     urls, wait, prerequisites):
    scenario_number = 0
    spl = get_all_file_paragraphs_into_list(filepath)
    counter = 1
    tc_name = ''
    tcs_list = []
    story = None
    for x in spl:
        line_num = x[0][0]
        list_of_lists_wo_enum = [list(y[1:]) for y in x]
        prgrph_list = [item for t in list_of_lists_wo_enum
                       for item in t]
        markers_list = [y.lower() for y in prgrph_list
                        if y.startswith("@")]
        data_mark, feature_mark_list, tc_name_value, url, prereq = all_markers(
            base_url, markers_list, urls)
        if prereq:
            story = prereq
        test_case = [y for y in prgrph_list if not y.startswith("@")
                     and not y.startswith("!!")]
        test_case_str = ' '.join([str(i) for i in test_case])
        str_list = re.split(r'[;,.!?\s]', test_case_str)

        actions = [x.lower() for x in str_list
                   if x.lower() in backward_action_dict or \
                   x.lower() in forward_action_dict]

        objects = [y.strip("#") for y in str_list
                   if y.startswith("#")]

        if actions or objects:
            if tc_name_value:
                tc_name = tc_name_value
            else:
                tc_name = ''.join(test_case[0])
            tc_id = f'{filepath}::{tc_name}::line {line_num}'
            scenario_title_line_num = counter + (len(x) + 1)
            try:
                if feature:
                    if feature.lower() in feature_mark_list:
                        scenario_number += 1
                        if story:
                            pre_tc_name, pre_tc_str, preq_url, pre_str_in_br, \
                            match = go_thru_prereq_file(
                                url, driver, story, prerequisites,
                                obj_dict, urls, wait, line_num, filepath)
                            if match:
                                test_p = execute_test_paragraph(
                                    test_case_str, filepath,
                                    scenario_title_line_num, tc_name, line_num,
                                    obj_dict, driver, url, wait, data_mark,
                                    prereq_tcs=pre_tc_str, prereq_url=preq_url,
                                    prereq_path=prerequisites,
                                    prereq_str_to_type=pre_str_in_br)
                        else:
                            test_p = execute_test_paragraph(
                                test_case_str, filepath, tc_name,
                                scenario_title_line_num, line_num, obj_dict,
                                driver, url, wait, data_mark)
                        tcs_list.append(f"PASSED {tc_id}")
                    else:
                        pass
                else:
                    scenario_number += 1
                    if story:
                        pre_tc_name, pre_tc_str, preq_url, pre_str_in_br, \
                        match = go_thru_prereq_file(
                            url, driver, story, prerequisites,
                            obj_dict, urls, wait, line_num, filepath)
                        if match:
                            test_p = execute_test_paragraph(
                                test_case_str, filepath,
                                scenario_title_line_num, tc_name, line_num,
                                obj_dict, driver, url, wait, data_mark,
                                prereq_tcs=pre_tc_str, prereq_url=preq_url,
                                prereq_path=prerequisites, prereq_str_to_type=
                                pre_str_in_br)
                    else:
                        test_p = execute_test_paragraph(
                            test_case_str, filepath, tc_name,
                            scenario_title_line_num, line_num, obj_dict,
                            driver, url, wait, data_mark)
                    tcs_list.append(f"PASSED {tc_id}")
            except Exception as e:
                tcs_list.append(f"FAILED {tc_id}")
                print(e)
                raise e
            finally:
                if test_case_str.startswith('crazytomato -1'):
                    print(f'crazytomato -1 found')
                else:
                    continue
    return scenario_number, tc_name, tcs_list


def go_thru_prereq_file(base_url, driver, story, prereq_filepath, obj_dict,
                        urls, wait, line_num, path):
    spl = get_all_file_paragraphs_into_list(prereq_filepath)
    counter = 1
    tc_name = ''
    url = ''
    test_case_str = []
    match = False
    for x in spl:
        # line_num = x[0][0]
        list_of_lists_wo_enum = [list(y[1:]) for y in x]
        prgrph_list = [item for t in list_of_lists_wo_enum
                       for item in t]
        markers_list = [y.lower() for y in prgrph_list
                        if y.startswith("@")]
        data_mark, feature_mark_list, tc_name_value, url, prereq = all_markers(
            base_url, markers_list, urls)
        if prereq:
            story = prereq
        test_case = [y for y in prgrph_list if not y.startswith("@")
                     and not y.startswith("!!")]
        test_case_str = ' '.join([str(i) for i in test_case])
        prereq_str_in_brackets = re.findall(r" \[\[(.+?)]]", test_case_str)

        str_list = re.split(r'[;,.!?\s]', test_case_str)

        actions = [x.lower() for x in str_list
                   if x.lower() in backward_action_dict or \
                   x.lower() in forward_action_dict]

        objects = [y.strip("#") for y in str_list
                   if y.startswith("#")]

        if actions or objects:
            if tc_name_value:
                tc_name = tc_name_value
            else:
                tc_name = ''.join(test_case[0])
            tc_id = f'Prerequisite::{prereq_filepath}::{tc_name}::line ' \
                    f'{line_num}'
            scenario_title_line_num = counter + (len(x) + 1)
            if story == tc_name:
                match = True
                break
    if not match:
        raise PomidorPrerequisiteScenarioNotFoundError(
            path, line_num, prereq_filepath, story)
    return tc_name, test_case_str, url, prereq_str_in_brackets, match


act = ForwardAction()
bact = BackwardAction()
backward_action_dict = bact.backward_actions_dictionary
forward_action_dict = act.forward_action_dictionary


def get_list_of_dicts_from_csv(file):
    try:
        with open(file) as read_obj:
            dict_reader = DictReader(read_obj)
            list_of_dict = list(dict_reader)
            return list_of_dict
    except PomidorFileNotFoundError(file) as e:
        raise e



def execute_test_paragraph(scenarioSteps, filepath, frst_prgrph_line, tc_name,
                           line_num, obj_dict, driver, url, wait, data_mark,
                           prereq_tcs=None, prereq_url=None,
                           prereq_path=None, prereq_str_to_type=None) -> str:
    csv_list_of_dicts = []
    csv_list_of_dicts_range = 0
    str_in_angle_brackets = re.findall(r"<<(.+?)>>", scenarioSteps)
    if data_mark and not str_in_angle_brackets:
        raise PomidorDataFeedNoAngleKeysProvided(filepath, line_num, data_mark)

    if not data_mark and str_in_angle_brackets:
        raise PomidorDataFeedNoCSVFileProvided(filepath, line_num, data_mark)

    if data_mark and str_in_angle_brackets:
        csv_list_of_dicts = get_list_of_dicts_from_csv(data_mark)
        csv_list_of_dicts_range = len(csv_list_of_dicts)

    angle_n_square = re.findall(r" <<(.+?)>>|\[\[(.+?)]]", scenarioSteps)
    angle_square_list = []
    angle_n_square_print = [('FirstName', ''), ('', 'some free text'),
                            ('City of Birth', '')]
    combine_angle_n_square_into_list(filepath, angle_n_square,
                                     angle_square_list,
                                     csv_list_of_dicts, line_num, data_mark)
    str_in_brackets = re.findall(r" \[\[(.+?)]]", scenarioSteps)
    act_obj_list, objects = prep_acts_n_objs(filepath, line_num, obj_dict,
                                             scenarioSteps)

    try:
        pomidor = Pomidor(driver, obj_dict, url)
        driver = pomidor.define_browser()
        if prereq_tcs:
            driver.get(prereq_url)
            driver.delete_all_cookies()
            # driver.maximize_window()
            prereq_act_obj_list, prereq_objects = \
                prep_acts_n_objs(prereq_path, line_num, obj_dict, prereq_tcs)
            run_once(driver, prereq_objects, prereq_act_obj_list,
                     prereq_str_to_type, prereq_path, line_num, wait)

        if driver.current_url == url or \
            str(driver.current_url).rstrip("/") == url:
            pass
        else:
            driver.get(url)
        if str_in_angle_brackets:
            for i in range(csv_list_of_dicts_range):
                run_once(driver, objects, act_obj_list,
                         angle_square_list, filepath, line_num, wait)
        else:
            run_once(driver, objects, act_obj_list,
                     str_in_brackets, filepath, line_num, wait)
    except Exception as e:
        raise e
    finally:
        driver.quit()


def prep_acts_n_objs(filepath, line_num, obj_dict, scenarioSteps):
    str_list = re.split(r'[;,.!?\s]', scenarioSteps)
    actions = [x.lower() for x in str_list
               if x.lower() in backward_action_dict or \
               x.lower() in forward_action_dict]
    objects = [y.strip("#") for y in str_list
               if y.startswith("#")]
    if len(actions) > len(objects):
        raise PomidorSyntaxErrorTooManyActions(path=filepath,
                                               line_num=line_num)
    elif len(objects) > len(actions):
        raise PomidorSyntaxErrorTooManyObjects(path=filepath,
                                               line_num=line_num)
    obj_source = [obj_dict.get(i) for i in objects]
    for enum, i in enumerate(obj_source):
        if i is None:
            raise PomidorObjectDoesNotExistInCSVFile(path=filepath,
                                                     line_num=line_num,
                                                     obj=objects[enum])
    act_obj_list = [list(a) for a in zip(actions, obj_source)]

    return act_obj_list, objects


def combine_angle_n_square_into_list(path, angle_n_square, angle_square_list,
                                     csv_list_of_dicts, line_num, data_mark):
    try:
        for k in csv_list_of_dicts * len(angle_n_square):
            for i in angle_n_square:
                if i[0] == '':
                    angle_square_list.append(i[1])
                else:
                    key = i[0]
                    value = csv_list_of_dicts[0].get(key)
                    if value is None:
                        raise PomidorDataFeedNoKeyError(path, line_num,
                                                        key, data_mark)
                    angle_square_list.append(value)
            del csv_list_of_dicts[0]
    except IndexError as ie:
        # print("Index error", repr(ie))
        pass


def run_once(driver, obj_dict, act_obj_list, str_in_brackets,
             path, line_num, wait):
    type_list = ['type', 'types', 'typed']
    for enum, i in enumerate(act_obj_list):
        acti = i[0]
        page_obj_loc = i[1][0]
        page_object_src = i[1][1]
        obj_name = obj_dict[enum]
        act_func, str_for_send_keys = which_action(
            acti, page_object_src, page_obj_loc, str_in_brackets, wait)

        if acti.startswith("type"):
            try:
                exec(f'WebDriverWait(driver, '
                 f'{wait}).until(ec.visibility_of_element_located('
                 f'(By.{page_obj_loc},\"{page_object_src}\"))).clear()')
            except TimeoutException:
                raise PomidorObjectDoesNotExistOnPage(path, line_num, obj_name)
            # TODO add is_selected and is_enabled asserts
            # TODO add "page_title" assert

        try:
            exec(act_func)
        except TimeoutException:
            raise PomidorObjectDoesNotExistOnPage(path, line_num, obj_name)

        # time.sleep(1)
        if acti in type_list:
            str_in_brackets.pop(0)


def all_markers(base_url, markers_list, urls):
    #   TODO: implement @prereq
    #   TODO: implement @param
    # process all markers with markers_list
    feature_mark_string = ''.join([x for x in
                                   markers_list
                                   if x.startswith("@feature")])
    feature_mark_list = [x.strip(r'[;,]') for x in
                         feature_mark_string.split()]

    prereq_mark_string = ''.join([x for x in
                                  markers_list
                                  if x.startswith("@prereq")])
    prereq_val = prereq_mark_string.strip("@prereq").strip()
    tc_name_line = ''.join([x for x in
                            markers_list
                            if x.startswith("@name")])
    tc_name_value = tc_name_line.replace("@name", '').strip()

    data_mark = ''.join([x.split()[1].strip(r'[;,]') for x in
                         markers_list
                         if x.startswith("@data")])
    url = base_url
    url_mark = ''.join([x.split()[1] for x in markers_list
                        if x.startswith("@url")])
    if url_mark:
        if url_mark.startswith("http") and "://" in url_mark:
            url = url_mark
        else:
            url = urls.get(url_mark)
    return data_mark, feature_mark_list, tc_name_value, url, prereq_val


def get_all_file_paragraphs_into_list(filepath):
    with open(filepath) as file:
        list_of_file = file.read().splitlines()
        enumerated_list = list(enumerate(list_of_file, 1))

        # get all paragraphs of a file as a list of lists
        spl = [list(y)
               for x, y
               in itertools.groupby(enumerated_list, lambda z: z[1] == '')
               if not x]
    return spl


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

    str_list = list(str_list)
    keys_to_send = str_list[0]
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

    def __init__(self, driver, obj_dict, url, urls=None,
                 prerequisites=None):
        self.urls = urls
        self.obj_dict = obj_dict
        self.url = url
        self.driver = driver
        self.prerequisites = prerequisites
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
            chrome_options = Options()
            # chrome_options.add_argument("start-maximized")
            # chrome_options.add_argument("--headless")
            # driver = webdriver.Chrome(options=chrome_options)
            driver = webdriver.Chrome()
        if self.driver == 'Firefox':
            driver = webdriver.Firefox()
        return driver

    @trackcalls
    def close(self):
        self.driver.close()

    #
    # @trackcalls
    # def quit(self):
    #     pass
    #
    # @trackcalls
    # def max_window(self):
    #     pass
    #
    # @trackcalls
    # def fullscreen(self):
    #     pass
    #
    # @trackcalls
    # def delete_all_cookies(self):
    #     pass

    def run(self, dir_path, feature=False, verbose=True, wait=10,
            parallel=None, story=None):
        start = time.perf_counter()
        scenario_number = 0
        file_number = 0
        results = []
        if parallel:
            pom_list = generate_list_of_pomidor_files(dir_path)
            futures_list = []
            with ThreadPoolExecutor(parallel, 'pre') as executor:
                for file_number, pom_file in enumerate(pom_list):
                    futures = executor.submit(
                        go_thru_one_file, self.url, self.driver, feature,
                        story, pom_file, self.obj_dict, self.urls, wait,
                        self.prerequisites)
                    futures_list.append(futures)

                for future in futures_list:
                    result, tc_name, tcs_list = future.result(timeout=60)
                    scenario_number += result
                    results.append(tcs_list)

        else:

            for file_number, pom_file in enumerate(
                    generate_list_of_pomidor_files(dir_path)):
                # print(f'pom_list -> {pom_file}')
                sce_num, tc_name, tcs_list = go_thru_one_file(
                    self.url, self.driver, feature, story, pom_file,
                    self.obj_dict, self.urls, wait, self.prerequisites)
                if tc_name:
                    scenario_number += sce_num
                results.append(tcs_list)

        finish = time.perf_counter()
        t_time = f'{finish - start:0.2f}s'
        if verbose:
            # Use list comprehension to convert a list of lists to a flat list
            results_flat_list = [item for elem in results for item in elem]
            print('\n\n===========pomidor tests ran============= ')
            # TODO: os.get_terminal_size()
            passed = 0
            failed = 0
            for i in results_flat_list:
                if i.startswith("PASS"):
                    print(f'{Colors.OKGREEN}{i}{Colors.ENDC}')
                    passed += 1
                elif i.startswith("FAIL"):
                    print(f'{Colors.FAIL}{i}{Colors.ENDC}')
                    failed += 1
                else:
                    continue
            print('\n===========pomidor files and scenarios involved=========')
            # TODO: os.get_terminal_size()
            print(f'{Colors.OKBLUE}Files used --> {file_number + 1}')  #
            print(f'Number of tests --> {scenario_number}{Colors.ENDC}')
            print('\n===========test summary info============= ')
            # TODO: os.get_terminal_size()
            if failed > 0 and passed > 0:
                print(f'{Colors.FAIL}{failed} failed,{Colors.OKGREEN} {passed}'
                      f' passed {Colors.FAIL} in {t_time} {Colors.ENDC}')
            if failed > 0 and passed == 0:
                print(f'{Colors.FAIL}{failed} failed in {t_time}{Colors.ENDC}')
            if failed == 0 and passed > 0:
                print(f'{Colors.OKGREEN}{passed} passed in '
                      f'{t_time}{Colors.ENDC}')
            if failed == 0 and passed == 0:
                print(f'{Colors.BOLD}Zero tests ran...{Colors.ENDC}')

        return scenario_number

    @staticmethod
    def how_many_files(dir_path):
        a = generate_list_of_pomidor_files(dir_path)

    @staticmethod
    def get_dict_obj(obj_key):  # Needed to print only
        pass
