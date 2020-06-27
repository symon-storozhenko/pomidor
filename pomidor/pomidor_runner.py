import glob
import functools
import pathlib
from pytest import mark
import re
from pomidor.actions import ForwardAction, BackwardAction
# from InstaLogin import login_field
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.common.by import By
import time


class PomidorSyntaxError(Exception):
    """ Pomidor syntax error class. """
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class PomidorObjectNotFound(Exception):
    """ Page object error class. """
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

def action_func(objc, act, wait=10,
                locator='XPATH'):  # TODO implement passing wait parameter
    return f'WebDriverWait(driver, {wait}).until(ec.presence_of_element_' \
           f'located((By.{locator},\'{objc}\'))).{act}'

def navigate(driver, url):
    return f'{driver}.get("{url}")'

def quit(driver):
    return  f'{driver}.quit()'


print('\n\n-------\nSTART:\n-------\n\n')

# driver = webdriver.Chrome()
# driver.get("https://www.instagram.com/")
# print("Instagram was opened")

extension = '.pomidor'


def generate_list_of_pomidor_files(tomato_directory):
    tomato_files_list = []
    tom_dir = pathlib.Path(tomato_directory)
    print(f'List of files: {tom_dir}')
    # one-file scenario
    if tomato_directory.endswith(extension):
        print('Fist!!')
        tomato_files_list.append(tomato_directory)
        # print(f'1: {tomato_files_list}')
    for enum, path in enumerate(
            tom_dir.rglob(f'*{extension}')):  # or use .glob('**/*.oat')
        tomato_files_list.append(path)
        print(f'{enum + 1}: {path}')
    # print(f'tomato_files_list -> {tomato_files_list}')
    if tomato_files_list == []:
        raise FileNotFoundError(f'No pomidor files found in the directory')
    return tomato_files_list


def define_test_paragraphs(scenarioSteps, filepath, first_paragraph_line,
                           scenario_title_line_num, line_num,
                           obj_dict, driver):
    latest_index = 0
    action_counter = 0
    obj_counter = 0
    tied_obj = False
    scenario_with_action = False
    str_in_quotes = re.findall(r" \'(.+?)\'", scenarioSteps)
    str_in_brackets = re.findall(r" \[(.+?)\]", scenarioSteps)
    print(f'str_in_brackets --> {str_in_brackets}')
    print(f"str_in_quotes --> {str_in_quotes} ")
    strList = re.split(r'[;,.!?\s]', scenarioSteps)
    tom = Pomidor(driver, obj_dict)

    if tom.before_test.has_been_called: # TODO added before
        print(f'FUnction was called!')
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
                        raise PomidorSyntaxError(   # Negative test covered
                            """ Negative tested in file
                            'more_than_1_obj_bckwrd_action_except.pomidor' """
                            
                            f'\nMore than one object is found! Make sure to '
                            f'put only one '
                            f'pertinent item before "{action_item}"'
                            f' (backward action) ' 
                            f'\nPlease review:"{first_paragraph_line.strip()}"'
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
                for action_in_forward_list in forward_action_dict:
                    # if forward action is found
                    if strList_item.lower().startswith(action_in_forward_list):
                        # print(f'One TUPLE MATCH --> keyword "{strList_item}"
                        #       f'contains action -> {action_in_forward_list}')
                        action_found = True
                        action_counter += 1
                        action_index = position
                        action_item = action_in_forward_list
                        # search for any orphan objects
                        for orphan_obj in strList[latest_index:action_index]:
                            if orphan_obj.startswith("#"):
                                raise PomidorSyntaxError(   #Covered
                                    """ Negative syntax to test located in
                                    'orphan_obj_b4_frwd_action.pomidor' file"""
                                    
                                    f'\n\n{"*" * 58}\nOrphan object found -> {orphan_obj}. '
                                    f'Please '
                                    f'associate an action (*) with this object.\n '
                                    f'\nPlease review: "{first_paragraph_line.strip()}"'
                                    f'\nFile name --> {filepath}'
                                    f'\nParagraph starts on line --> '
                                    f'{scenario_title_line_num}')
                        for obj_position, page_object in enumerate(
                                strList[action_index:]):  # frwd obj
                            if page_object.startswith("#"):  # if obj is found
                                object_found = True
                                page_obj_index = position + obj_position
                                latest_index = page_obj_index + 1
                                for str_slice_item in strList[action_index + 1:
                                page_obj_index]:
                                    if str_slice_item.startswith(
                                            "*"):  # if actions left by mistake
                                        raise PomidorSyntaxError(   # Covered
                                            """ Negative tested with file 
                                            'two_actions.pomidor' """
                                            f'\n\n{"*" * 58}\nWhich action to use with '
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
                                continue
                        break
            # Perform action on the object
            if not object_found:
                raise PomidorSyntaxError(   # Covered
                    """ Negative tested in file 'no_obj_found.pomidor' """
                    
                    f'\n\n{"*" * 58}\nno object found for action "{strList_item}'
                    f'\nPlease review: "{filepath}",--> line {line_num}')
            else:
                obj_counter += 1
                tied_obj = True
                page_object = page_object.strip('#')
                # page_obj_source = home_page_dict[page_object][1]
                print('                check dict first+++++++++++++++')
                if page_object not in tom.obj_dict:
                    raise PomidorObjectNotFound(    # Covered
                        """ Negative tested in file 
                        'obj_not_found_in_page_factory.pomidor' """
                        f'Page object NOT is Found! ---> '
                                    f'#{page_object}'
                                    f'\nPlease review: '
                                    f'"{first_paragraph_line.strip()}"'
                                    f'\nFile name --> {filepath}'
                                    f'\nParagraph starts on line --> '
                                    f'{scenario_title_line_num+1}.\n\n')
                print(f'?????????????Object_source via Tomato class/PO --> '
                      f'{tom.get_dict_obj(page_object)}')
                page_object_src = tom.get_dict_obj(page_object)[1]
                page_obj_locator = tom.get_dict_obj(page_object)[0]
                print(f'page_object_src --> {page_object_src}')
                print(f'page_obj_locator  --> {page_obj_locator}')
                # if page_object_src not in
                print(f'Latest index --> {latest_index}')
                print(f"\nActions and Assertions performed:")
                # if forward or backward action
                if backward_action:
                    b_act = backward_action_dict.get(action_item)
                    print(f'BACKWARD ACTION --> {b_act}')
                    # Perform actual selenium backward action manipulations
                    # exec(action_func(page_object_src,
                    # backward_actions_dict.get(action_item),
                    #                  locator=home_page_dict[page_object][0]))
                    print(
                        f'- {page_object} is {strList_item.strip("*")} - PASS')
                    latest_index = action_index + 1
                    # del strList[:latest_index]
                else:
                    f_act = forward_action_dict.get(action_item)
                    print(f"f_act --> {f_act}")
                    print(f"action_item --> {action_item} ")
                    if action_item == "*type":
                        # Perform actual selenium forward action manipulations
                        print(action_func(page_object_src,
                                          f"send_keys(\"{str_in_quotes.pop(0)}\")",
                                          # locator=home_page_dict[page_object][
                                          #     0]))
                                          ))
                    # act = f_act.forward_action_dictionary
                    print(f'FORWARD ACTION --> {f_act}')
                    # Perform actual selenium forward action manipulations
                    # exec(action_func(page_obj_source,
                    # forward_action_dict.get(action_item),
                    #                  locator=home_page_dict[page_object][0]))
                    print(
                        f'- {strList_item.strip("*")} on {page_object} - PASS')
                    latest_index = page_obj_index + 1
                    # del strList[:latest_index]
        elif strList_item.startswith('#') and not tied_obj:
            obj_counter += 1
            object_found = True
            object = strList_item
    if action_counter < 1:
        scenarioSteps = scenarioSteps.strip()
        scenario_with_action = False
        print(
            f'\nNo actions are found in test --> "{first_paragraph_line.strip()}"'
            f'\nFile name --> {filepath}.\nParagraph starts on line --> '
            f'{scenario_title_line_num}.\nPlease add actions (*) and their objects (#), '
            f'otherwise, comment out the whole paragraph with quotes """ <paragraph> """')
    for obj_last in strList[latest_index:]:
        if obj_last.startswith('#'):
            raise PomidorSyntaxError(   # Covered
                """ Negative tested in file 'last_orphan_obj.pomidor' """
                f'\n{"*" * 58}\nOrphan object found -> {obj_last}. '
                f'Please '
                f'associate an action (*) with this object.\n '
                f'\nPlease review: "{first_paragraph_line.strip()}"'
                f'\nFile name --> {filepath}'
                f'\nParagraph starts on line --> '
                f'{scenario_title_line_num}')
    print('SCENARIO COMPLETED!!!!')
    if tom.after_test.has_been_called:  # TODO added quit
        print("After Test was called!")
        # driver = after_test
        # exec(quit(driver))
    return scenario_with_action


def go_thru_pomidor_file(func, obj_dict, driver):
    scenario_number = 0
    for file_number, filepath in enumerate(func):
        with open(filepath) as file:
            for total_lines_count, row in enumerate(file):
                continue
        with open(filepath) as tomato_file:
            print(f'\nOpening file --> {filepath}\n')
            scenarioSteps = ''
            first_paragraph_line = ''
            for line_num, line in enumerate(tomato_file):
                if scenarioSteps == '' and (
                        line in ['\n', '\r\n'] or line.startswith('--')):
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
                    print(f'LINE IS -----> {line} at {line_num}')
                    print(
                        f"\nBegin test:\n ----{first_paragraph_line.strip()}"
                        f"----\n\n"
                        f"\nActions and Assertions performed:")
                    # scenarioSteps += line
                    # with regex
                    print(f'srtList --> {scenarioSteps}')
                    test_paragraph = \
                        define_test_paragraphs(scenarioSteps, filepath,
                                               first_paragraph_line,
                                               scenario_title_line_num,
                                               line_num, obj_dict, driver)
                    if test_paragraph:
                        scenario_number += 1
                    scenarioSteps = ''
    return file_number, scenario_number


def go_thru_pomidor_file_with_story(func, feature_type, story, obj_dict,
                                    driver, exact_story_name=False):  # best-working
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
            for line_num, line in enumerate(tomato_file):
                if line == 0:
                    continue
                else:
                    line_counter += 1
                print(f'======= ===== General Line #{line_num}====== ======')
                if feature_type.lower() in line.lower():
                    line_list = re.split(r'[;,.!?\s]', line)
                    print(f'{feature_type} \n\n++++++++STORY Line ! --> '
                          f'{line_list}++++++++++\n')
                    # feature_index = line_list.index(feature_type)
                    for f in line_list:
                        if exact_story_name:
                            if f == story:
                                print(f'Found exact {feature_type}!!!!!!!!')
                                feature_instances += 1
                        else:
                            if story.lower() in f.lower():  # f.lower().__contains__(story.lower()):
                                print(f'$@@@@@@@@@@@@$$ FOUND {feature_type}!!!!!!!! -> {f}\n')
                                print(f'Line before inner loop--> {line}')
                                feature_instances += 1
                    if feature_instances > 0:
                        for line_num_in, line in enumerate(tomato_file,
                                                           line_counter):
                            line_counter += 1
                            print(
                                f'Text "{line}" is on line num --> '
                                f'{line_num_in+1}')

                            # if feature_bool:
                            if scenarioSteps == '' and (line in ['\n',
                                                                 '\r\n']
                                                        or line.startswith(
                                        '--')):
                                continue
                            else:
                                if scenarioSteps == '':
                                    first_paragraph_line = line
                                    scenario_title_line_num = line_num
                                if scenarioSteps != '' and line.startswith(
                                        '--'):
                                    continue
                                scenarioSteps += line
                            if (scenarioSteps != '' and line in ['\n',
                                                                 '\r\n']) \
                                    or (
                                    scenarioSteps != '' and line_counter-1 ==
                                    total_lines_count+1):
                                print(f'total_lines_count -> {total_lines_count}')
                                print(f'LINE IS -----> {line} at '
                                      f'{line_num_in}')
                                print(
                                    f"\nBegin test:\n ----"
                                    f"{first_paragraph_line.strip()}----\n"
                                    f"\nActions and Assertions performed:")
                                # scenarioSteps += line
                                # print(f'srtList --> {strList}')
                                latest_index = 0
                                action_counter = 0
                                test_paragraph = define_test_paragraphs(
                                    scenarioSteps, filepath,
                                    first_paragraph_line,
                                    scenario_title_line_num,
                                    line_num, obj_dict, driver)
                                if test_paragraph:
                                    scenario_number += 1
                                scenarioSteps = ''
                                feature_instances = 0
                                break
                            # line_num = line_num_in
                        # break
                    else:
                        line_counter += 1
                        continue
                else:
                    continue
    return file_number, scenario_number


def list_all_mark_values(func, feature_type):  # best-working
    scenario_number = 0
    marker_values = []
    for file_number, filepath in enumerate(func):
        with open(filepath) as file:
            for total_lines_count, row in enumerate(file):
                continue
        with open(filepath) as tomato_file:
            print(f'\nOpening file --> {filepath}\n')
            for line_num, line in enumerate(tomato_file):
                # print(f'======= ===== General MARKER Line #{line_num}====== ======')
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
                    print(f'{feature_type.upper()} \n\n++++++++MARKER Line ! --> '
                          f'{marker_values}++++++++++\n')
    return marker_values, len(marker_values)


def trackcalls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.has_been_called = True
        return func(*args, **kwargs)
    wrapper.has_been_called = False
    return wrapper


class Pomidor:

    def __init__(self, driver, obj_dict):
        self.driver = driver
        self.obj_dict = obj_dict

    def __repr__(self):
        return f'Pomidor object with page object dictionary:\n' \
               f' {self.obj_dict}'

    @trackcalls
    def before_test(self, url):
        self.driver.get(url)
        # pass

    @trackcalls
    def after_test(self):
        self.driver.quit()
        # pass


    def run_scripts(self, dir_path, verbose=True):
        file_num, scenario_number = go_thru_pomidor_file(
            generate_list_of_pomidor_files(dir_path), self.obj_dict,
            self.driver)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_num + 1}')  #
            print(f'Number of scenarios --> {scenario_number}')
        return scenario_number

    def run_features(self, dir_path, feature_value, exact_match=False,
                     verbose=True, before_test=None,
                    after_test=None):
        file_number, scenario_number = go_thru_pomidor_file_with_story(
            generate_list_of_pomidor_files(dir_path), "@feature", feature_value,
            self.obj_dict, self.driver, exact_match,
            before_test, after_test)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_number + 1}')  #
            print(f'Number of scenarios --> {scenario_number}')
        return scenario_number

    def run_story(self, dir_path, feature_value, exact_match=False,
                  verbose=True, before_test=None,
                    after_test=None):
        file_num, scenario_number = go_thru_pomidor_file_with_story(
            generate_list_of_pomidor_files(dir_path), "@story",
            feature_value, self.obj_dict, exact_match,
            before_test, after_test)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_num + 1}')  #
            print(f'Number of scenarios --> {scenario_number}')
        return scenario_number

    def run_custom_identifier(self, dir_path, feature_type, feature_value,
                              exact_match=False, verbose=True):
        file_num, scenario_number = go_thru_pomidor_file_with_story(
            generate_list_of_pomidor_files(dir_path), feature_type,
            feature_value, self.obj_dict, exact_match)
        if verbose:
            print('\n\n-------\nEND -- All tests PASSED\n-------\n')
            print(f'Number of files used --> {file_num + 1}')  #
            print(f'Number of scenarios --> {scenario_number}')
        return scenario_number

    @staticmethod
    def list_all_marker_values(dir_path, feature_type):
        marker_list, markers_num = list_all_mark_values(generate_list_of_pomidor_files(
            dir_path), feature_type)
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

    def get_dict_obj(self, obj_key):
        # print(self.obj_dict.get(obj_key))
        return self.obj_dict.get(obj_key)


# @mark.smoke
def test_smoke_tomato_runner():
    go_thru_pomidor_file(
        generate_list_of_pomidor_files(pathlib.Path(smoke_tests_dir)))


# @mark.regression
def test_regression_tomato():
    go_thru_pomidor_file(
        generate_list_of_pomidor_files(pathlib.Path(all_tomatoes_dir)))


# Pomidor.run_features(all_tomatoes_dir, "Home_Page")


# Run the script
# test_regression_tomato()
# test_smoke_tomato_runner(smoke_tests_dir)

# file_number, scenario_number = go_thru_pomidor_file(generate_list_of_tomato_files(pathlib.Path(all_tomatoes_dir)))


# time.sleep(3)
# driver.quit()
#
# # find all local vars in func
# func.__code__.co_varnames
