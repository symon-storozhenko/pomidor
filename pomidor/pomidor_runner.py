import concurrent.futures
import functools
import sys
import time
import traceback
from selenium.webdriver.common.keys import Keys
import pytest
import pathlib
import re
from csv import DictReader
from concurrent.futures import ThreadPoolExecutor
import itertools
from selenium.common.exceptions import TimeoutException, \
    ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from pomidor.actions import ForwardAction, BackwardAction, InputKeys, Locators
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.support.select import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pomidor.pomidor_exceptions import PomidorDataFeedNoKeyError, \
    PomidorDataFeedNoAngleKeysProvidedException, \
    PomidorDataFeedNoCSVFileProvided, \
    PomidorFileNotFoundError, PomidorSyntaxErrorTooManyActions, \
    PomidorSyntaxErrorTooManyObjects, PomidorObjectDoesNotExistInCSVFile, \
    Colors, PageObjectNotFound, \
    PomidorPrerequisiteScenarioNotFoundError, \
    PomidorCantRunOneBrowserInstanceInParallel, PomidorKeyDoesNotExist, \
    PomidorAssertError, ElementNotClickable, PomidorEqualAssertError


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
        tomato_files_list.append(str(path))
    try:
        assert len(tomato_files_list) > 0
    # if not tomato_files_list:
    except Exception as e:
        raise Exception(PomidorFileNotFoundError(str(tom_dir)), e)
    return tomato_files_list


def browser_frequency(po, base_url, driver, feature, prerequisite, filepath,
                      obj_dict,
                      urls, wait, prerequisites, browser,
                      slow_mode, failed_screenshots, passed_screenshots,
                      adhoc_screenshots, headless):
    if browser.lower() == 'per_file':
        driver = po.define_browser(headless)
        with driver:
            scenario_number, tc_name, tcs_list = go_thru_one_file(
                po, base_url, driver, feature, prerequisite, filepath,
                obj_dict, urls, wait, prerequisites, browser, slow_mode,
                failed_screenshots, passed_screenshots, adhoc_screenshots,
                headless)
            return scenario_number, tc_name, tcs_list

        # finally:
        #     if type(driver) == str:
        #         raise Exception(f'{Colors.FAIL}PomidorERROR\n'
        #                         f'Consider updating the '
        #                         f'webdriver{Colors.ENDC}')
        #     driver.quit()
    else:
        scenario_number, tc_name, tcs_list = go_thru_one_file(
            po, base_url, driver, feature, prerequisite, filepath, obj_dict,
            urls, wait, prerequisites, browser, slow_mode, failed_screenshots,
            passed_screenshots, adhoc_screenshots, headless)

        return scenario_number, tc_name, tcs_list


def go_thru_one_file(po, base_url, driver, feature, default_prerequisite,
                     filepath, obj_dict,
                     urls, wait, prerequisites, browser, slow_mode,
                     failed_screenshots, passed_screenshots,
                     adhoc_screenshots, headless):
    scenario_number = 0
    spl = get_all_file_paragraphs_into_list(filepath)
    counter = 1
    tc_name = ''
    tcs_list = []
    if browser == 'per_test':
        driver = po.driver
    for x in spl:
        line_num = x[0][0]
        list_of_lists_wo_enum = [list(y[1:]) for y in x]
        prgrph_list = [item for t in list_of_lists_wo_enum
                       for item in t]
        markers_list = [y.lower() for y in prgrph_list
                        if y.startswith("@")]
        data_mark, feature_mark_list, tc_name_value, url, prereq, cookie_dict\
            = None, None, None, None, None, None
        data_mark, feature_mark_list, tc_name_value, url, prereq, \
        cookie_dict, param_list = all_markers(base_url, markers_list, urls)
        if prereq:
            prerequisite = prereq
        else:
            prerequisite = default_prerequisite
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
            tc_id_screenshot = f'[{tc_name}] [line {line_num}]'
            filepath_for_screenshot = filepath
            try:
                if "/" in filepath:
                    filepath_for_screenshot = filepath.replace('/', "(slash)")
                if "\\" in filepath:  # TODO: test it on Windows
                    filepath_for_screenshot = filepath.replace('\\', "(slash)")
            except TypeError as te:
                print(te)
            scenario_title_line_num = counter + (len(x) + 1)
            try:
                if feature:
                    if feature.lower() in feature_mark_list:
                        scenario_number += 1
                        if prerequisite:
                            pre_tc_name, pre_tc_str, preq_url, pre_str_in_br, \
                            match, cookie_dict = go_thru_prereq_file(
                                url, prerequisite, prerequisites, urls,
                                line_num, filepath, cookie_dict)
                            if match:
                                if browser == 'per_test':
                                    driver = po.define_browser(headless)
                                    with driver:
                                        test_p = execute_test_paragraph(
                                            test_case_str, filepath,
                                            scenario_title_line_num, tc_name,
                                            line_num,
                                            obj_dict, driver, url, wait,
                                            data_mark,
                                            browser, slow_mode,
                                            failed_screenshots,
                                            passed_screenshots,
                                            adhoc_screenshots, param_list,
                                            cookie_dict, urls,
                                            prereq_tcs=pre_tc_str,
                                            prereq_url=preq_url,
                                            prereq_path=prerequisites,
                                            prereq_str_to_type=pre_str_in_br)
                                else:
                                    test_p = execute_test_paragraph(
                                        test_case_str, filepath,
                                        scenario_title_line_num, tc_name,
                                        line_num,
                                        obj_dict, driver, url, wait, data_mark,
                                        browser, slow_mode,
                                        failed_screenshots, passed_screenshots,
                                        adhoc_screenshots, param_list,
                                        cookie_dict, urls,
                                        prereq_tcs=pre_tc_str,
                                        prereq_url=preq_url,
                                        prereq_path=prerequisites,
                                        prereq_str_to_type=pre_str_in_br)
                        else:
                            if browser == 'per_test':
                                driver = po.define_browser(headless)
                                with driver:
                                    execute_test_paragraph(
                                        test_case_str, filepath, tc_name,
                                        scenario_title_line_num, line_num,
                                        obj_dict,
                                        driver, url, wait, data_mark, browser,
                                        slow_mode, failed_screenshots,
                                        passed_screenshots, adhoc_screenshots,
                                        param_list, cookie_dict, urls)
                            else:
                                test_p = execute_test_paragraph(
                                    test_case_str, filepath, tc_name,
                                    scenario_title_line_num, line_num,
                                    obj_dict,
                                    driver, url, wait, data_mark, browser,
                                    slow_mode, failed_screenshots,
                                    passed_screenshots, adhoc_screenshots,
                                    param_list, cookie_dict, urls)
                        tcs_list.append(f"PASSED {tc_id}")
                    else:
                        pass
                else:
                    scenario_number += 1
                    if prerequisite:
                        pre_tc_name, pre_tc_str, preq_url, pre_str_in_br, \
                        match, cookie_dict = go_thru_prereq_file(
                            url, prerequisite, prerequisites, urls,
                            line_num, filepath, cookie_dict)
                        if match:
                            if browser == 'per_test':
                                driver = po.define_browser(headless)
                                with driver:
                                    test_p = execute_test_paragraph(
                                        test_case_str, filepath,
                                        scenario_title_line_num, tc_name,
                                        line_num,
                                        obj_dict, driver, url, wait, data_mark,
                                        browser, slow_mode,
                                        failed_screenshots, passed_screenshots,
                                        adhoc_screenshots, param_list,
                                        cookie_dict, urls,
                                        prereq_tcs=pre_tc_str,
                                        prereq_url=preq_url,
                                        prereq_path=prerequisites,
                                        prereq_str_to_type=pre_str_in_br)
                            else:
                                test_p = execute_test_paragraph(
                                    test_case_str, filepath,
                                    scenario_title_line_num, tc_name, line_num,
                                    obj_dict, driver, url, wait, data_mark,
                                    browser, slow_mode,
                                    failed_screenshots, passed_screenshots,
                                    adhoc_screenshots, param_list,
                                    cookie_dict, urls,
                                    prereq_tcs=pre_tc_str,
                                    prereq_url=preq_url,
                                    prereq_path=prerequisites,
                                    prereq_str_to_type=pre_str_in_br)
                    else:
                        if browser == 'per_test':
                            driver = po.define_browser(headless)
                            with driver:
                                test_p = execute_test_paragraph(
                                    test_case_str, filepath, tc_name,
                                    scenario_title_line_num, line_num,
                                    obj_dict,
                                    driver, url, wait, data_mark, browser,
                                    slow_mode, failed_screenshots,
                                    passed_screenshots,
                                    adhoc_screenshots, param_list,
                                    cookie_dict, urls)
                        else:
                            test_p = execute_test_paragraph(
                                test_case_str, filepath, tc_name,
                                scenario_title_line_num, line_num, obj_dict,
                                driver, url, wait, data_mark, browser,
                                slow_mode, failed_screenshots,
                                passed_screenshots, adhoc_screenshots,
                                param_list, cookie_dict, urls)
                    tcs_list.append(f"PASSED {tc_id}")
                    if passed_screenshots:
                        driver.save_screenshot(
                            f'{passed_screenshots}/PASS {tc_id_screenshot} '
                            f'[{filepath_for_screenshot}].png')

            except Exception as e:
                tcs_list.append(f"FAILED {tc_id}")  # Research test.html
                if failed_screenshots:
                    driver.save_screenshot(
                        f'{failed_screenshots}/FAIL {tc_id_screenshot} '
                        f'[{filepath_for_screenshot}].png')
                # traceback.print_exc(limit=1)
                # print(e)
                print(repr(e))

    return scenario_number, tc_name, tcs_list


def go_thru_prereq_file(base_url, story, prereq_filepath, urls, line_num,
                        path, cookie_dict):
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
        data_mark, feature_mark_list, tc_name_value, url, prereq, cookie_dict,\
        param_list = all_markers(
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
            if story.lower() == tc_name.lower():
                match = True
                break
    if not match:
        raise PomidorPrerequisiteScenarioNotFoundError(
            path, line_num, prereq_filepath, story)
    return tc_name, test_case_str, url, prereq_str_in_brackets, match, \
            cookie_dict


fact = ForwardAction()
bact = BackwardAction()
k = InputKeys()
backward_action_dict = bact.backward_actions_dictionary
forward_action_dict = fact.forward_action_dictionary
keys_dict = k.keys
locator_dict = Locators.locator_dict


def get_list_of_dicts_from_csv(file):
    try:
        with open(file, mode='r', encoding='utf-8-sig') as read_obj:
            dict_reader = DictReader(read_obj)
            list_of_dict = list(dict_reader)
            return list_of_dict
    except PomidorFileNotFoundError(file) as e:
        raise e


def execute_test_paragraph(scenarioSteps, filepath, frst_prgrph_line, tc_name,
                           line_num, obj_dict, driver, url, wait, data_mark,
                           browser, slow_mode, failed_screenshots,
                           passed_screenshots, adhoc_screenshots, params,
                           cookie_dict, urls, prereq_tcs=None, prereq_url=None,
                           prereq_path=None, prereq_str_to_type=None):
    csv_list_of_dicts = []
    prereq_act_obj_list = []
    prereq_objects = []
    csv_list_of_dicts_range = 0
    str_in_angle_brackets = re.findall(r"<<(.+?)>>", scenarioSteps)
    if data_mark and not str_in_angle_brackets:
        raise PomidorDataFeedNoAngleKeysProvidedException(filepath, line_num,
                                                          data_mark)

    if not data_mark and str_in_angle_brackets:
        raise PomidorDataFeedNoCSVFileProvided(filepath, line_num, data_mark)

    if data_mark and str_in_angle_brackets:
        csv_list_of_dicts = get_list_of_dicts_from_csv(data_mark)
        csv_list_of_dicts_range = len(csv_list_of_dicts)

    angle_n_square = re.findall(r" <<(.+?)>>|\[\[(.+?)]]", scenarioSteps)
    angle_square_list = []
    combine_angle_n_square_into_list(filepath, angle_n_square,
                                     angle_square_list,
                                     csv_list_of_dicts, line_num, data_mark)
    str_in_brackets = re.findall(r" \[\[(.+?)]]", scenarioSteps)
    act_obj_list, objects, orig_obj_dict = prep_acts_n_objs(
        filepath, line_num, obj_dict, scenarioSteps)

    # delete if mentioned in @params line
    for i in params:
        if i.startswith('del'):
            driver.delete_all_cookies()
            break
    if prereq_tcs:
        prereq_act_obj_list, prereq_objects, orig_obj_dict = \
        prep_acts_n_objs(prereq_path, line_num, obj_dict, prereq_tcs)

    if prereq_tcs and prereq_act_obj_list[0][0] == 'navigate':
        prereq_url = prereq_act_obj_list[0][1][0]
        driver.get(prereq_url)
    if act_obj_list[0][0] == 'navigate':
        url = act_obj_list[0][1][0]
        driver.get(url)
    else:
        driver.get(url)

    # add cookies from a csv cookie file if mentioned in @params line
    if cookie_dict:
        for cookie in cookie_dict:
            cookie = {k.lower(): v for k, v in cookie.items()}
            driver.add_cookie(cookie)
        driver.refresh()

    if prereq_tcs:
        run_once(driver, prereq_objects, orig_obj_dict,
                 prereq_act_obj_list,
                 prereq_str_to_type, prereq_path, line_num, wait,
                 slow_mode, failed_screenshots, passed_screenshots,
                 adhoc_screenshots, params, cookie_dict, prereq_url,
                 str_in_angle_brackets)
    if str_in_angle_brackets:
        for i in range(csv_list_of_dicts_range):
            if slow_mode:
                time.sleep(slow_mode)
            if driver.current_url == url or \
                    str(driver.current_url).rstrip("/") == url:
                pass
            else:
                driver.get(url)
            run_once(driver, objects, orig_obj_dict, act_obj_list,
                     angle_square_list, filepath, line_num, wait,
                     slow_mode, failed_screenshots, passed_screenshots,
                     adhoc_screenshots, params, cookie_dict, url,
                     str_in_angle_brackets)
    else:
        if slow_mode:
            time.sleep(slow_mode)
        if driver.current_url == url or \
                str(driver.current_url).rstrip("/") == url:
            pass
        else:
            driver.get(url)
        run_once(driver, objects, orig_obj_dict, act_obj_list,
                 str_in_brackets, filepath, line_num, wait, slow_mode,
                 failed_screenshots, passed_screenshots, adhoc_screenshots,
                 params, cookie_dict, url, str_in_angle_brackets)
    # except Exception as e:
    #     driver.save_screenshot(f'{filepath}::{tc_name}')
    #     raise e
    # finally:
    #     pass


def prep_acts_n_objs(filepath, line_num, obj_dict, scenarioSteps):
    str_list = re.split(r'[;,.!?\s]', scenarioSteps)
    actions = [x.lower() for x in str_list
               if x.lower() in backward_action_dict or \
               x.lower() in forward_action_dict]
    objects = [y.strip("#").lower() for y in str_list
               if y.startswith("#")]
    if len(actions) > len(objects):
        raise PomidorSyntaxErrorTooManyActions(path=filepath,
                                               line_num=line_num)
    elif len(objects) > len(actions):
        raise PomidorSyntaxErrorTooManyObjects(path=filepath,
                                               line_num=line_num)
    # obj_source1 = [obj_dict.get(i) for i in objects
    #               if i in obj_dict or
    #               x for x in keys if x in keys]

    obj_source = []
    for i in objects:
        if i in obj_dict:
            obj_source.append(obj_dict.get(i))
        elif i.isdigit():
            obj_source.append(i)
        else:
            obj_source.append(i.upper())

    # for enum, i in enumerate(obj_source):
    #     if i is None:
    #         raise PomidorObjectDoesNotExistInCSVFile(path=filepath,
    #                                                  line_num=line_num,
    #                                                  obj=objects[enum])
    act_obj_list = [list(a) for a in zip(actions, obj_source)]

    return act_obj_list, objects, obj_dict


def combine_angle_n_square_into_list(path, angle_n_square, angle_square_list,
                                     csv_list_of_dicts, line_num, data_mark):
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
        if len(csv_list_of_dicts) == 1:
            del csv_list_of_dicts[0]
            break
        else:
            del csv_list_of_dicts[0]

# just a comment
def run_once(driver, obj_dict, orig_obj_dict, act_obj_list, str_in_brackets,
             path, line_num, wait, present_mode, failed_screenshots,
             passed_screenshots, adhoc_screenshots, params, cookie_dict,
             initial_url, str_in_angle_brackets):
    type_list = ['type', 'types', 'typed']
    assert_list = ['selected', 'equals', 'contains', 'enabled']
    negative_assert_list = ['not_selected', 'not_equals', 'not_contains',
                            'not_enabled']
    scroll_time = None
    web_el = None
    previous_obj = None
    # for t in params:
    #     if t.startswith('del') and cookie_dict:
    #         pass
    #     elif t.startswith('del') and not cookie_dict:
    #         driver.delete_all_cookies()
        # driver.refresh()
    for t in params:
        if t.startswith('scroll'):
            if '=' in t:
                scroll_time = t.replace('scroll=', "")
                scroll_time = re.sub(r'^.*?=', '', t)
            else:
                scroll_time = 0.2
        if t.startswith('max'):
            driver.maximize_window()
    for enum, i in enumerate(act_obj_list):
        act = i[0]
        if enum == 0 and act == 'navigate':
            pass
        elif enum !=0 and act == 'navigate':
            url = i[1][0]
            if driver.current_url == url or \
                    str(driver.current_url).rstrip("/") == url:
                pass
            else:
                driver.get(url)
        elif act.startswith('press'):
            if i[1] not in keys_dict:
                raise PomidorKeyDoesNotExist(i[1])
            key = keys_dict.get(i[1])
            webdriver.ActionChains(driver).key_down(key).perform()
            if present_mode:
                time.sleep(present_mode)
        elif act == 'wait':
            time.sleep(float(i[1]))
        # elif act == ''
        else:
            page_obj_loc = i[1][1].strip()
            page_object_src = i[1][0]
            loc_id = None
            if act in ('contains', 'not_contains', 'equals', 'not_equals',
                        'type', 'types', 'typed'):
                last_str = str_in_brackets.pop(0)
            obj_name = obj_dict[enum]
            if obj_name == 'page_title':
                pass
            elif obj_name not in orig_obj_dict:
                raise PomidorObjectDoesNotExistInCSVFile(path=path,
                                                         line_num=line_num,
                                                         obj=obj_name)
            elif orig_obj_dict.get(obj_name) is None:
                raise PomidorObjectDoesNotExistInCSVFile(path=path,
                                                         line_num=line_num,
                                                         obj=obj_name)
            for p in locator_dict:
                if p == page_obj_loc.upper():
                    loc_id = locator_dict.get(p)
                    break
            if act in assert_list or act in negative_assert_list:
                try:
                    if page_obj_loc.strip().startswith('DROP'):
                        el_text = Select(web_el).first_selected_option.text
                    elif obj_name == 'page_title':
                        el_text = driver.title
                    else:
                        web_el = WebDriverWait(driver, wait).until(
                            ec.presence_of_element_located((
                                loc_id, page_object_src)))
                        el_text = web_el.text
                except TimeoutException:
                    raise PageObjectNotFound(path=path,
                                             line_num=line_num,
                                             obj=obj_name)
                if act in negative_assert_list:
                    try:
                        # negative assert for drop downs
                        if page_obj_loc.strip().startswith('DROP') \
                                and act == 'not_selected':
                            assert el_text != page_object_src
                        else:
                            if act == 'not_equals':
                                assert el_text != last_str
                            elif act == 'not_contains':
                                assert last_str not in el_text
                            else:
                                assert not web_el.is_selected()
                    except AssertionError:
                        if act == 'not_equals' or act == 'not_contains':
                            raise PomidorEqualAssertError(path=path,
                                                          line_num=line_num,
                                                          obj=obj_name,
                                                          act=act,
                                                          string=last_str,
                                                          actual_string=
                                                          el_text)
                        else:
                            raise PomidorAssertError(path=path,
                                                     line_num=line_num,
                                                     obj=obj_name,
                                                     act=act)
                else:
                    try:
                        # negative assert for drop downs
                        if page_obj_loc.strip().startswith('DROP') \
                                and act == 'selected':
                            assert el_text == page_object_src
                        else:
                            if act == 'equals':
                                assert el_text == last_str
                            elif act == 'contains':
                                assert last_str in el_text
                            else:
                                assert web_el.is_selected()
                    except AssertionError:
                        if act == 'equals' or act == 'contains':
                            raise PomidorEqualAssertError(path=path,
                                                          line_num=line_num,
                                                          obj=obj_name,
                                                          act=act,
                                                          string=last_str,
                                                          actual_string=
                                                          el_text)
                        else:
                            raise PomidorAssertError(path=path,
                                                     line_num=line_num,
                                                     obj=obj_name,
                                                     act=act)
            if act == 'select' and \
                    page_obj_loc.strip().startswith(
                        'DROP'):
                # For drop down selection
                if page_obj_loc.strip() == 'DROP_DOWN_VISIBLE_TEXT':
                    Select(web_el).select_by_visible_text(page_object_src)
                if page_obj_loc.strip() == 'DROP_DOWN_INDEX':
                    a = Select(web_el).select_by_index(int(page_object_src))
                if page_obj_loc.strip() == 'DROP_DOWN_VALUE':
                    Select(web_el).select_by_value(page_object_src)

            if act.startswith('click') or \
                    act.startswith('type') or \
                    (act == 'select' and not
                    page_obj_loc.strip().startswith('DROP')):
                try:
                    web_el = WebDriverWait(driver, wait).until(
                        ec.element_to_be_clickable((loc_id, page_object_src)))
                except TimeoutException:
                    raise PageObjectNotFound(path=path,
                                             line_num=line_num,
                                             obj=obj_name)
                # print(f'a - {a.is_enabled()}')
                if scroll_time:
                    webdriver.ActionChains(driver).move_to_element(web_el)
                    driver.execute_script("arguments[0].scrollIntoView();",
                                          web_el)
                    time.sleep(
                        float(scroll_time))
                if act.startswith('type'):
                    web_el.clear()
                    web_el.send_keys(last_str)
                elif act.startswith('click') or \
                        act == 'select':
                    try:
                        web_el.click()
                    except ElementClickInterceptedException:
                        raise ElementNotClickable(path=path,
                                                  line_num=line_num,
                                                  obj=obj_name)
        if present_mode:
            time.sleep(present_mode)

    # TODO add is_enabled asserts


# TODO: add login capability to the website - in progress

def all_markers(base_url, markers_list, urls):
    # process all markers with markers_list
    cookie_dict = ''
    feature_mark_string = ''.join([x for x in
                                   markers_list
                                   if x.startswith("@feature")])
    feature_mark_list = [x.strip(r'[;,]') for x in
                         feature_mark_string.split()]

    urls = {k.lower(): v for k, v in urls.items()}
    # TODO: capture url from page_onjects.csv file

    prereq_mark_string = ''.join([x for x in
                                  markers_list
                                  if x.startswith("@prereq")])
    prereq_val = prereq_mark_string.replace("@prereq", '').strip()

    param_string = ''.join([x for x in
                            markers_list
                            if x.startswith("@params")])
    param = param_string.replace("@params", '').strip()
    param_list = re.split(r'[;,!?\s]', param)
    # print(f'param_list - >{param_list}: {type(param_list)}')  # TODO: print params

    tc_name_line = ''.join([x for x in
                            markers_list
                            if x.startswith("@id")])
    tc_name_value = tc_name_line.replace("@id", '').strip()

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

    for param in param_list:
        if param.startswith('url'):
            url = param.replace("url=", '').strip()
            if url.startswith("http") and "://" in url:
                url = url
            else:
                url = urls.get(url)
        if param.startswith('prereq'):
            prereq_val = param.replace("prereq=", '').strip()
        if param.startswith('data') or param.startswith('<<data>>'):
            data_mark = param.replace("data=", '')
        if param.startswith('cookies'):
            cookie_file = param.replace("cookies=", '')
            cookie_dict = get_list_of_dicts_from_csv(cookie_file)


    # print(f'url - {url} :: prereq - {prereq_val}::data_mark -> {data_mark}')

    return data_mark, feature_mark_list, tc_name_value, url, prereq_val, \
           cookie_dict, param_list


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
                 prerequisite_file=None, passed_screenshots=None,
                 failed_screenshots=None):
        self.urls = urls
        self.obj_dict = obj_dict
        self.url = url
        self.driver = driver
        self.prerequisite_file = prerequisite_file
        self.passed_screenshots = passed_screenshots
        self.failed_screenshots = failed_screenshots
        # self.obj_repo = self.get_page_objects()

    def __repr__(self):
        return f'Pomidor object with page object dictionary:\n' \
               f' {self.obj_dict}' \
               f'and driver {self.driver}'

    @classmethod
    def get_page_objects(cls, obj_d: str) -> dict:
        with open(obj_d) as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',', quotechar='"')
            obj_dicto = {rows['name'].strip().lower():
                             (rows['value'],
                              rows['selector'].strip()) for rows in csv_reader}
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
    def define_browser(self, headless):
        if self.driver.lower() == 'chrome':
            chrome_options = Options()
            # chrome_options.add_argument("--start-maximized") # not working
            if headless:  # TODO: add set_window_size option
                chrome_options.add_argument("--window-size=1400,600")
                chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            # driver.maximize_window()
            # driver.manage().window().maximize();
            # driver = webdriver.Chrome()
            return driver
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

    def run(self, path='', feature=False, verbose=True, wait=10,
            parallel=None, prerequisite=None, browser='per_file',
            slow_mode=False,
            adhoc_screenshots='adhoc_screenshots', headless=False):
        #   TODO: Remove adhoc_screenshot
        start = time.perf_counter()
        scenario_number = 0
        file_number = 0
        results = []
        pom_list = generate_list_of_pomidor_files(path)
        po = Pomidor(self.driver, self.obj_dict, self.url, self.urls)
        if parallel:
            if browser.lower() == 'one':
                raise PomidorCantRunOneBrowserInstanceInParallel
            futures_list = []
            with ThreadPoolExecutor(parallel, 'pre') as executor:
                for file_number, pom_file in enumerate(pom_list):
                    futures = executor.submit(
                        browser_frequency, po, self.url, self.driver, feature,
                        prerequisite, pom_file, self.obj_dict, self.urls, wait,
                        self.prerequisite_file, browser, slow_mode,
                        self.failed_screenshots, self.passed_screenshots,
                        adhoc_screenshots, headless)
                    futures_list.append(futures)

                for future in futures_list:
                    result, tc_name, tcs_list = future.result()
                    scenario_number += result
                    results.append(tcs_list)
        else:
            if browser.lower() == 'one':
                driver = po.define_browser(headless)
            else:
                driver = self.driver
            for file_number, pom_file in enumerate(pom_list):
                sce_num, tc_name, tcs_list = browser_frequency(
                    po, self.url, driver, feature, prerequisite, pom_file,
                    self.obj_dict, self.urls, wait, self.prerequisite_file,
                    browser, slow_mode, self.failed_screenshots,
                    self.passed_screenshots, adhoc_screenshots, headless)
                if tc_name:
                    scenario_number += sce_num
                results.append(tcs_list)
        finish = time.perf_counter()
        t_time = f'{finish - start:0.2f}s'
        if verbose:
            # Use list comprehension to convert a list of lists to a flat list
            results_flat_list = [item for elem in results for item in elem]
            print('\n\n===========pomidor tests ran============= ')
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
            print('\n========= pomidor files and scenarios involved =========')
            print(f'{Colors.OKBLUE}Files used --> {file_number + 1}')  #
            print(f'Number of tests --> {scenario_number}{Colors.ENDC}')
            print('\n=========== test summary info ============= ')
            # TODO: os.get_terminal_size()
            if failed > 0 and passed > 0:
                print(f'{Colors.FAIL}{failed} failed,{Colors.OKGREEN} {passed}'
                      f' passed{Colors.FAIL} in {t_time} {Colors.ENDC}')
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
