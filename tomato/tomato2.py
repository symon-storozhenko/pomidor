import glob
import pathlib
from pytest import mark
import re
from pageObjects.page_factory import PageObject
from tomato.actions import ForwardAction, BackwardAction
# from InstaLogin import login_field
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time


def action_func(objc, act, wait=10, locator='XPATH'):
    return f'WebDriverWait(driver, {wait}).until(ec.presence_of_element_' \
           f'located((By.{locator},\'{objc}\'))).{act}'


# forward_action_dict = {'*click': 'click()', '*type': 'send_keys("Yoyo!!!!")'}
# forward_action_list = [key for key in forward_action_dict.keys()]
#
# backward_actions_dict = {'*visible': 'is_displayed()', '*not visible': 'test'}
# # backward_actions_list = [key for key in backward_actions_dict.keys()]


board_keys = ['Enter', 'Esc']

def iter_dict(*tup):
    for it in tup:
        print(it)
        return it


# iter_dict(forward_action_list)

home_page_dict = {
    'login_field': ['XPATH', "//input[@name=\"username\"]"],
    'password_field': ['XPATH', "//input[@name=\"password\"]"],
    'submit_button': ['CSS', "//button[@type=\"submit\"]"],
}
#


print('\n\n-------\nSTART:\n-------\n\n')

# driver = webdriver.Chrome()
# driver.get("https://www.instagram.com/")
# print("Instagram was opened")

all_tomatoes_dir = '/Users/myco/PycharmProjects/tomato3/tomatoes'
# print(f'Tomatoes folder is found! --> {tomato_dir.exists}')
smoke_tests_dir = '/Users/myco/PycharmProjects/tomato2/tomatoes/SmokeTest'
regression_tests_dir = '/Users/myco/PycharmProjects/tomato2/tomatoes/RegressionSuite'
one = '/Users/myco/PycharmProjects/tomato3/tomatoes/TestCase.pomidor'

extension = '.pomidor'

def generate_list_of_tomato_files(tomato_directory):
    tomato_files_list = []
    tom_dir = pathlib.Path(tomato_directory)
    print(f'List of files: {tom_dir}')
    # one-file scenario
    if tomato_directory.endswith(extension):
        print('Fist!!')
        tomato_files_list.append(tomato_directory)
        print(f'1: {tomato_files_list}')
    for enum, path in enumerate(tom_dir.rglob(f'*{extension}')):  # or use .glob('**/*.oat')
        tomato_files_list.append(path)
        print(f'{enum+1}: {path}')
    print(f'tomato_files_list -> {tomato_files_list}')
    return tomato_files_list


def define_test_paragraphs(strList, filepath, first_paragraph_line, scenario_title_line_num, scenarioSteps, line_num):
    global action_index
    latest_index = 0
    action_found = False
    total_actions = False
    action_counter = 0
    obj_counter = 0
    object_found = False
    tied_obj = False
    scenario_with_action = False
    for position, strList_item in enumerate(strList[latest_index:]):
        object_found = False
        action_found = False
        if strList_item.startswith("*"):
            scenario_with_action = True
            print(f'\n-Printing from latest index in paragraph -->'
                  f'\n {strList[latest_index:]}')  # whole TC in one string
            total_actions = True
            backward_action = False
            tied_obj = False
            act = ForwardAction()
            bact = BackwardAction()
            backward_action_dict = bact.backward_actions_dictionary
            forward_action_dict = act.forward_action_dictionary
            print(f'FOWRD dICT --> {forward_action_dict}')

            # Iterate over forward actions
            for action_in_bckwrd_list in backward_action_dict.keys():  # look for backward action first
                print(f'SUCCESS -> for action_in_bckwrd_list in backward_actions_dict.keys():')
                if strList_item.lower().startswith(action_in_bckwrd_list):
                    action_counter += 1
                    action_found = True
                    backward_action = True
                    action_index = position
                    action_item = action_in_bckwrd_list
                    bk_obj_count = 0
                    for page_objects in strList[latest_index:action_index]:
                        if page_objects.startswith("#"):  # if back_obj is found
                            page_object = page_objects  # to prevent obj in front to reassign value
                            # print(f'Object is found! --> {page_object}')
                            object_found = True
                            page_obj_bk_index = strList.index(page_object)
                            bk_obj_count += 1
                        else:
                            continue
                    if bk_obj_count > 1:
                        raise Exception(f'\nMore than one object is found! Make sure to put only one '
                                        f'pertinent item before "{action_item}" (backward action) '
                                        f'\nPlease review: "{first_paragraph_line.strip()}"'
                                        f'\nFile name --> {filepath}'
                                        f'\nParagraph starts on line --> {scenario_title_line_num}.\n\n'
                                        f'Examples:'
                                        f'\n*Click on #page and #cart is *visible --> allowed \n'
                                        f'*Click on #page and #profile and #cart is *visible --> '
                                        f'NOT allowed')
                    else:
                        pass
                    break
            if action_found:
                latest_index = action_index + 1
                latest_artifact = strList_item
            if not action_found:
                # Iterate over forward actions
                for action_in_forward_list in forward_action_dict:  # if forward action is found
                    if strList_item.lower().startswith(action_in_forward_list):
                        # print(f'One TUPLE MATCH --> keyword "{strList_item}" '
                        #       f'contains action -> {action_in_forward_list}')
                        action_found = True
                        action_counter += 1
                        action_index = position
                        action_item = action_in_forward_list
                        # search for any orphan objects
                        for orphan_obj in strList[latest_index:action_index]:
                            if orphan_obj.startswith("#"):
                                raise Exception(f'\n\n{"*" * 58}\nOrphan object found -> {orphan_obj}. '
                                                f'Please '
                                                f'associate an action (*) with this object.\n '
                                                f'\nPlease review: "{first_paragraph_line.strip()}"'
                                                f'\nFile name --> {filepath}'
                                                f'\nParagraph starts on line --> '
                                                f'{scenario_title_line_num}')
                        for obj_position, page_object in enumerate(strList[action_index:]):  # frwd obj
                            if page_object.startswith("#"):  # if obj is found
                                object_found = True
                                page_obj_index = position + obj_position
                                latest_index = page_obj_index + 1
                                latest_artifact = page_object
                                for str_slice_item in strList[action_index + 1:page_obj_index]:
                                    if str_slice_item.startswith(
                                            "*"):  # check for any actions left by mistake
                                        raise Exception(f'\n\n{"*" * 58}\nWhich action to use with '
                                                        f'{page_object}? '
                                                        f'{strList_item} (forward action) or '
                                                        f'{str_slice_item} (undefined vector action)? '
                                                        f'\nPlease review: '
                                                        f'"{first_paragraph_line.strip()}"\nFile name '
                                                        f'--> {filepath}\nParagraph starts on line -->'
                                                        f' {scenario_title_line_num}')
                                break
                            else:
                                object_found = False
                                latest_artifact = action_in_forward_list
                                continue
                        break
            # Perform action on the object
            if not object_found:
                raise Exception(f'\n\n{"*" * 58}\nno object found for action "{strList_item}'
                                f'\nPlease review: "{filepath}",--> line {line_num}')
            else:
                obj_counter += 1
                tied_obj = True
                page_object = page_object.strip('#')
                # page_obj_source = home_page_dict[page_object][1]
                po = PageObject(page_object)
                page_object_src = po.home_page[1]
                page_obj_locator = po.home_page[0]
                print(f'Latest index --> {latest_index}')
                print(f'Page Obj Source = {page_object_src}')
                print(f'Page obj Locator = {page_obj_locator}')
                print(f"\nActions and Assertions performed:")
                # if forward or backward action
                if backward_action:
                    b_act = backward_action_dict.get(action_item)
                    print(f'BACKWARD ACTION --> {b_act}')
                    # exec(action_func(page_object_src, backward_actions_dict.get(action_item),
                    #                  locator=home_page_dict[page_object][0]))
                    print(f'- {page_object} is {strList_item.strip("*")} - PASS')
                    latest_index = action_index + 1
                    # del strList[:latest_index]
                else:
                    f_act = forward_action_dict.get(action_item)
                    # act = f_act.forward_action_dictionary
                    print(f'FORWARD ACTION --> {f_act}')
                    # exec(action_func(page_obj_source, forward_action_dict.get(action_item),
                    #                  locator=home_page_dict[page_object][0]))
                    print(f'- {strList_item.strip("*")} on {page_object} - PASS')
                    latest_index = page_obj_index + 1
                    # del strList[:latest_index]
        elif strList_item.startswith('#') and not tied_obj:
            obj_counter += 1
            object_found = True
            object = strList_item
    if action_counter < 1:
        scenarioSteps = scenarioSteps.strip()
        scenario_with_action = False
        print(f'\nNo actions are found in test --> "{first_paragraph_line.strip()}"'
                        f'\nFile name --> {filepath}.\nParagraph starts on line --> '
                        f'{scenario_title_line_num}.\nPlease add actions (*) and their objects (#), '
                        f'otherwise, comment out the whole paragraph with quotes """ <paragraph> """')
    for obj_last in strList[latest_index:]:
        if obj_last.startswith('#'):
            raise Exception(f'\n{"*" * 58}\nOrphan object found -> {obj_last}. '
                            f'Please '
                            f'associate an action (*) with this object.\n '
                            f'\nPlease review: "{first_paragraph_line.strip()}"'
                            f'\nFile name --> {filepath}'
                            f'\nParagraph starts on line --> '
                            f'{scenario_title_line_num}')
    return scenario_with_action


def go_thru_tomato_file(func):
    scenario_number = 0
    for file_number, filepath in enumerate(func):
        # scenario_number = 0
        with open(filepath) as file:
            for total_lines_count, row in enumerate(file, 1):
                continue
        with open(filepath) as tomato_file:
            print(f'\nOpening file --> {filepath}\n')
            scenarioSteps = ''
            first_paragraph_line = ''
            for line_num, line in enumerate(tomato_file):
                if scenarioSteps == '' and (line in ['\n', '\r\n'] or line.startswith('--')):
                    continue
                else:
                    if scenarioSteps == '':
                        first_paragraph_line = line
                        scenario_title_line_num = line_num
                    if scenarioSteps != '' and line.startswith('--'):
                        continue
                    scenarioSteps += line
                if (scenarioSteps != '' and line in ['\n', '\r\n']) or (
                        scenarioSteps != '' and line_num == total_lines_count):
                    print(f'LINE IS -----> {line}')
                    print(f"\nBegin test:\n ----{first_paragraph_line.strip()}----"
                          f"\nActions and Assertions performed:")
                    scenarioSteps += line
                    # with regex
                    str_list = re.split(r'[;,.!?\s]', scenarioSteps)
                    # print(f'srtList --> {strList}')
                    latest_index = 0
                    action_counter = 0
                    test_paragraph = define_test_paragraphs(str_list, filepath,
                                                            first_paragraph_line, scenario_title_line_num,
                                           scenarioSteps, line_num)
                    if test_paragraph:
                        scenario_number += 1
                    scenarioSteps = ''
    return file_number, scenario_number


def go_thru_tomato_file_with_feature(func, feature):    # TODO needs removal
    scenario_number = 0
    for file_number, filepath in enumerate(func):
        with open(filepath) as file:
            for total_lines_count, row in enumerate(file, 1):
                continue
        with open(filepath) as tomato_file:
            print(f'\nOpening file --> {filepath}\n')
            scenarioSteps = ''
            first_paragraph_line = ''
            feature_instances = 0
            for line_num, line in enumerate(tomato_file):
                if line.lower().startswith('feature'):
                    line_list = re.split(r'[;,.!?\s]', line)
                    # print(f'Line List! --> {line_list}')
                    for f in line_list:
                        if f == feature:
                            print(f'Found feature!!!!!!!!')
                            print(f'Line before inner loop--> {line}')
                            feature_instances += 1
                            for line_num_in, line in enumerate(tomato_file, line_num):
                                print(f'Line is - >{line}. Line num --> {line_num}')

                            # if feature_bool:
                                if scenarioSteps == '' and (line in ['\n', '\r\n'] or line.startswith('--')):
                                    continue
                                else:
                                    if scenarioSteps == '':
                                        first_paragraph_line = line
                                        scenario_title_line_num = line_num
                                    if scenarioSteps != '' and line.startswith('--'):
                                        continue
                                    scenarioSteps += line
                                if (scenarioSteps != '' and line in ['\n', '\r\n']) or (
                                        scenarioSteps != '' and line_num == total_lines_count):
                                    print(f'LINE IS -----> {line}')
                                    print(f"\nBegin test:\n ----{first_paragraph_line.strip()}----"
                                          f"\nActions and Assertions performed:")
                                    scenarioSteps += line
                                    # strList = scenarioSteps.split()  # implement re.split
                                    # with regex
                                    str_list = re.split(r'[;,.!?\s]', scenarioSteps)
                                    # print(f'srtList --> {strList}')
                                    latest_index = 0
                                    action_counter = 0
                                    test_paragraph = define_test_paragraphs(str_list, filepath,
                                                                            first_paragraph_line, scenario_title_line_num,
                                                           scenarioSteps, line_num)
                                    scenarioSteps = ''
                                    scenario_number += 1
                                    break
                        else:
                            continue
                else:
                    continue
    return file_number, scenario_number



def go_thru_tomato_file_with_story(func, feature_type, story, exact_story_name=False):    # best-working def
    # global file_number
    scenario_number = 0
    for file_number, filepath in enumerate(func):
        # scenario_number = 0
        with open(filepath) as file:
            for total_lines_count, row in enumerate(file, 1):
                continue
        with open(filepath) as tomato_file:
            print(f'\nOpening file --> {filepath}\n')
            scenarioSteps = ''
            first_paragraph_line = ''
            feature_instances = 0
            for line_num, line in enumerate(tomato_file):
                if line.lower().startswith(feature_type.lower()):
                    line_list = re.split(r'[;,.!?\s]', line)
                    print(f'{feature_type} Line ! --> {line_list}')
                    for f in line_list[1:]:
                        if exact_story_name:
                            if f == story:
                                print(f'Found exact {feature_type}!!!!!!!!')
                                feature_instances += 1
                        else:
                            if f.lower().__contains__(story.lower()):
                                print(f'Found {feature_type}!!!!!!!! -> {f}\n')
                                print(f'Line before inner loop--> {line}')
                                feature_instances += 1
                        if feature_instances > 0:
                            for line_num_in, line in enumerate(tomato_file, line_num):
                                print(f'Line is - >{line}. Line num --> {line_num}')

                            # if feature_bool:
                                if scenarioSteps == '' and (line in ['\n', '\r\n'] or line.startswith('--')):
                                    continue
                                else:
                                    if scenarioSteps == '':
                                        first_paragraph_line = line
                                        scenario_title_line_num = line_num
                                    if scenarioSteps != '' and line.startswith('--'):
                                        continue
                                    scenarioSteps += line
                                if (scenarioSteps != '' and line in ['\n', '\r\n']) or (
                                        scenarioSteps != '' and line_num == total_lines_count):
                                    print(f'LINE IS -----> {line}')
                                    print(f"\nBegin test:\n ----{first_paragraph_line.strip()}----"
                                          f"\nActions and Assertions performed:")
                                    scenarioSteps += line
                                    # strList = scenarioSteps.split()  # implement re.split
                                    # with regex
                                    str_list = re.split(r'[;,.!?\s]', scenarioSteps)
                                    # print(f'srtList --> {strList}')
                                    latest_index = 0
                                    action_counter = 0
                                    test_paragraph = define_test_paragraphs(str_list, filepath,
                                                                            first_paragraph_line, scenario_title_line_num,
                                                           scenarioSteps, line_num)
                                    scenarioSteps = ''
                                    scenario_number += 1
                                    feature_instances = 0
                                    break
                            break
                        else:
                            continue
                else:
                    continue
    return file_number, scenario_number


class Tomato:
    @staticmethod
    def run_scripts(dir_path, verbose=True):
        file_num, scenario_number = go_thru_tomato_file(
            generate_list_of_tomato_files(dir_path))
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_num+1}')  #
            print(f'Number of scenarios --> {scenario_number}')


    @staticmethod
    def run_features(dir_path, feature_value, exact_story_name=False, verbose=True):
        file_number, scenario_number = go_thru_tomato_file_with_story(
            generate_list_of_tomato_files(dir_path), "feature", feature_value, exact_story_name)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_number+1}')  #
            print(f'Number of scenarios --> {scenario_number}')


    @staticmethod
    def run_story(dir_path, feature_value, exact_story_name=False, verbose=True): # TODO add one-file scenario
        file_num, scenario_number = go_thru_tomato_file_with_story(
            generate_list_of_tomato_files(dir_path),
            feature_value, exact_story_name)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_num+1}')  #
            print(f'Number of scenarios --> {scenario_number}')


    @staticmethod
    def run_custom_identifier(dir_path, feature_type, feature_value,
                              exact_story_name=False, verbose=True):    # TODO add one-file scenario
        file_num, scenario_number = go_thru_tomato_file_with_story(
            generate_list_of_tomato_files(dir_path), feature_type,
            feature_value, exact_story_name)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_num+1}')  #
            print(f'Number of scenarios --> {scenario_number}')


    @staticmethod
    def run_standalone_custom_identifier(dir_path, feature_value,   # TODO interesting concept
                              exact_story_name=False,
                              verbose=True):  # TODO add one-file scenario
        file_num, scenario_number = go_thru_tomato_file_with_story(
            generate_list_of_tomato_files(dir_path),
            feature_value, exact_story_name)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_num + 1}')  #
            print(f'Number of scenarios --> {scenario_number}')


    @staticmethod
    def how_many_files(dir_path):
        a = generate_list_of_tomato_files(dir_path)
        print(a)


@mark.smoke
def test_smoke_tomato_runner():
    go_thru_tomato_file(generate_list_of_tomato_files(pathlib.Path(smoke_tests_dir)))


@mark.regression
def test_regression_tomato():
    go_thru_tomato_file(generate_list_of_tomato_files(pathlib.Path(all_tomatoes_dir)))


# Tomato.run_features(all_tomatoes_dir, "Home_Page")


# Run the script
# test_regression_tomato()
# test_smoke_tomato_runner(smoke_tests_dir)

# file_number, scenario_number = go_thru_tomato_file(generate_list_of_tomato_files(pathlib.Path(all_tomatoes_dir)))




# time.sleep(3)
# driver.quit()
#
# # find all local vars in func
# func.__code__.co_varnames
