from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from tests.pageObjects.page_factory import PageObject, BaseURL
from pomidor.pomidor_runner import Pomidor
from pomidor.pomidor_exceptions import PomidorDataFeedNoKeyError, \
    PomidorDataFeedNoAngleKeysProvided, PomidorDataFeedNoCSVFileProvided, \
    PomidorSyntaxErrorTooManyActions, PomidorSyntaxErrorTooManyObjects, \
    PomidorObjectDoesNotExistInCSVFile, PomidorObjectDoesNotExistOnPage, \
    PomidorPrerequisiteScenarioNotFoundError
import pytest
import concurrent.futures

url = 'https://pomidor-automation.com/'
page_obj = Pomidor.get_page_objects("pageObjects/page_objects.csv")
addtl_urls = Pomidor.additional_urls("pageObjects/urls.csv")
prereqs = "pageObjects/prerequisites.pomidor"
# driver = webdriver.Chrome()

po = Pomidor("Chrome", page_obj, url, urls=addtl_urls, prerequisites=prereqs)

root_dir = ''
empty_str = 'negative_pomidory/empty_dir'
nested_dir = 'negative_pomidory/SmokeTest'
nested_dir2 = 'negative_pomidory/SmokeTest2'
nested_dir3 = 'negative_pomidory/SmokeTest3'
nested_dir4 = 'negative_pomidory/SmokeTest4'
all_tomato_scripts = 'tomato3/tests/negative_pomidory'
one_file = 'negative_pomidory/two_actions.pomidor'
more_than_1_back = 'negative_pomidory/' \
                   'more_than_1_obj_bckwrd_action_except.pomidor'
orph_obj_b4_frwd_act = 'negative_pomidory/orphan_obj_b4_frwd_action.pomidor'
two_actions = 'negative_pomidory/two_actions.pomidor'
no_obj_found = 'negative_pomidory/no_obj_found.pomidor'
no_obj_in_page_fctry = 'negative_pomidory/obj_not_found_in_page_factory.pomidor'
last_orphan_obj = 'negative_pomidory/last_orphan_obj.pomidor'
last_line_3_scenarios = 'negative_pomidory/last_line_is_read.pomidor'
run_story = "negative_pomidory/run_story.pomidor"
pro_pomidor = 'negative_pomidory/pro.pomidor'
smoke_test_dir = 'negative_pomidory/SmokeTest'
assert_actions = 'negative_pomidory/assert_actions.pomidor'
data_file = 'negative_pomidory/data_file.pomidor'
prereqs_test = 'negative_pomidory/prereqs_test.pomidor'
prereqs_test2 = 'negative_pomidory/prereqs_test2.pomidor'
prereqs_test3 = 'negative_pomidory/prereqs_test3.pomidor'
prereqs_test4 = 'negative_pomidory/prereqs_test4.pomidor'
obj_in_page_factory_but_not_on_webpage = \
    'negative_pomidory/obj_in_page_factory_but_not_on_webpage.pomidor'
obj_in_page_factory_but_not_on_webpage2 = \
    'negative_pomidory/obj_in_page_factory_but_not_on_webpage2.pomidor'
prereqs2 = "pageObjects/prerequisites2.pomidor"


class TestPomidorRunAll:

    # Browser opens even for empty .pomidor files
    # 30 browser initializations
    # 26 failed, 38 passed - 31 files, 64 scenarios -
    # 102s - with passed'n'failed screenshots with dirs created and all prereqs
    # 76 - 80s - headless, passed'n'failed screenshots with dirs, all prereqs
    def test_pomidor_run_all_browser_per_file(self):
        po.run(parallel=4, browser_per_file=True, prerequisite='Google_search',
               headless=True)

    #     67.84s (-13.00s) without any screenshot logic
    #     77s - 118s with passed and failed screenshots with dirs created
    #     76s - 160.51s with passed and failed screenshots but no dirs created
    #     68.69 - 100.83s with passed and failed screenshots=None

    # Browser opens only for tests with actions and objects
    # 57 browser initializations
    def test_pomidor_run_all_browser_per_each_test(self):
        po.run(parallel=4, browser_per_file=False, headless=True,
               prerequisite='Google_search')  # 79.00s

    #     81.91s with idle screenshots
    #     79s with passed and failed screenshots=None
    #     78.12s -  - 99s with passed and failed screenshots with dirs created
    # 128s - with passed'n'failed screenshots with dirs created and all prereqs
    # 93s - headless, passed'n'failed screenshots with dirs, all prereqs

    def test_pomidor_run_all_one_browser_parallel(self):
        po.run(parallel=4, browser_per_file=True, prerequisite='Google_search',
               headless=0)


class TestPomidorParallel:
    def test_pomidor_run_parallel_one_browser_contexts(self):
        po.run(path='negative_pomidory/SmokeTest4',
               browser='one', prerequisite='google_search')


class TestPomidorPro:
    def test_pomidor_pro(self):
        scenario_num = po.run(pro_pomidor, feature='SmokeTest')
        assert scenario_num == 2


class TestPomidorPrerequisites:

    # Exception is raised. Test summary missing FAILED line,
    # but test total is correct
    def test_pomidor_prerequisite_file_itself(self):
        scenario_num = po.run(prereqs, wait=2)
        assert scenario_num == 4

    def test_pomidor_csv_data_with_prereqs_feature(self):
        scenario_num = po.run(prereqs_test, feature="csv_data", slow_mode=1,
                              prerequisite='GoOgle_search')
        assert scenario_num == 1

    def test_pomidor_csv_data_with_prereqs_all(self):
        scenario_num = po.run(prereqs_test, wait=2, slow_mode=0.5,
                              prerequisite='GoOgle_search')
        assert scenario_num == 3  # one prereq not found, exception printed

    def test_pomidor_csv_data_with_common_prereqs(self):
        scenario_num = po.run(prereqs_test4, wait=6, browser_per_file=True,
                              prerequisite='GoOgle_search', slow_mode=.2)
        assert scenario_num == 3  # one prereq not found, exception printed

    def test_pomidor_csv_data_with_prereqs_all_one_fails(self):
        scenario_num = po.run(prereqs_test2, wait=2, slow_mode=0.2,
                              prerequisite='GooglE_SearcH',
                              feature='CSV_data3', browser_per_file=False)
        assert scenario_num == 3  # Exception on prereq is raised


class TestPomidor:

    def test_pomidor_run_all_and_nested_dir(self):
        scenario_num = po.run(nested_dir)
        assert scenario_num == 4  # 19.5 sec

    def test_pomidor_parallel(self):
        scenario_num = po.run(nested_dir, parallel=4, browser_per_file=1)
        assert scenario_num == 4  # 8.3 sec

    # 3 browsers should invoke simultaneously, skipping one error paragraph
    # 4 scenarios ran total, but 1 fails in the beginning and script continues
    def test_pomidor_parallel_one_fails_but_continue(self):
        scenario_num = po.run(nested_dir3, parallel=4)
        assert scenario_num == 4  # 8.3 sec # Exception printed

    def test_pomidor_parallel_with_feature(self):
        scenario_num = po.run(nested_dir, feature='CSV_data1', headless=True,
                              parallel=4, prerequisite='Google_Search')
        assert scenario_num == 2  # 8.3 sec # Exception printed

    def test_pomidor_run_feature(self):
        scenario_num = po.run(run_story, feature='Report')
        assert scenario_num == 3

    def test_pomidor_run_story(self):
        scenario_num = po.run(run_story)
        assert scenario_num == 1

    def test_pomidor_run_is_displayed(self):
        scenario_num = po.run(run_story,
                              feature="Reporting")
        assert scenario_num == 1

    def test_pomidor_run_not_displayed(self):
        scenario_num = po.run(assert_actions, feature="Not_Displayed", wait=2)
        assert scenario_num == 1  # test summary printed

    def test_pomidor_csv_data(self):
        scenario_num = po.run(data_file, feature="csv_data")
        assert scenario_num == 2

    def test_pomidor_feature_list_csv_data1(self):
        scenario_num = po.run(data_file, feature="csv_data1")
        assert scenario_num == 1

    def test_pomidor_feature_list_csv_data2(self):
        scenario_num = po.run(data_file, feature="csv_data2")
        assert scenario_num == 1

    def test_pomidor_orphan_obj_b4_frwd_action(self):
        scenario_num = po.run(orph_obj_b4_frwd_act)
        assert scenario_num == 1

    def test_pomidor_obj_in_page_factory_but_not_on_webpage_and_continue(self):
        scenario_num = po.run(obj_in_page_factory_but_not_on_webpage2,
                              wait=2)
        assert scenario_num == 2  # prints Exception and Test Summary


class TestPomidorSyntaxPositive:

    def test_pomidor_last_line_is_read(self):
        scenario_num = po.run(last_line_3_scenarios)
        assert scenario_num == 3


class TestPomidorSyntaxExceptions:

    # has 'crazytomato -1' in front
    # 4 scenarios total but one fails, 2 ran in total
    def test_pomidor_parallel_raise_exception_and_continue_and_exception(self):
        with pytest.raises(PomidorSyntaxErrorTooManyObjects):
            po.run(nested_dir2, parallel=4)  # prints Exception

    # has 'crazytomato -1' in front
    def test_pomidor_more_than_1_obj_bckwrd_action_except(self):
        with pytest.raises(PomidorSyntaxErrorTooManyObjects):
            po.run(more_than_1_back)  # prints Exception

    # has 'crazytomato -1' in front
    def test_pomidor_two_actions(self):
        with pytest.raises(PomidorSyntaxErrorTooManyActions):
            po.run(two_actions)  # prints Exception

    # has 'crazytomato -1' in front
    def test_pomidor_no_obj_found(self):
        with pytest.raises(PomidorSyntaxErrorTooManyActions):
            po.run(no_obj_found)  # prints Exception

    # has 'crazytomato -1' in front
    def test_pomidor_no_obj_in_page_fctry(self):
        with pytest.raises(PomidorObjectDoesNotExistInCSVFile):
            po.run(no_obj_in_page_fctry)  # prints Exception

    # has 'crazytomato -1' in front
    def test_pomidor_last_orphan_obj(self):
        with pytest.raises(PomidorSyntaxErrorTooManyObjects):
            po.run(last_orphan_obj)  # prints Exception

    # has 'crazytomato -1' in front
    # prints Exception
    def test_pomidor_obj_in_page_factory_but_not_on_webpage(self):
        with pytest.raises(PomidorObjectDoesNotExistOnPage):
            po.run(obj_in_page_factory_but_not_on_webpage, wait=2)

    # has 'crazytomato -1' in front
    def test_pomidor_csv_data_none_key_error(self):
        with pytest.raises(PomidorDataFeedNoKeyError):
            po.run(data_file, feature="csv_data7")  # prints Exception

    # has 'PomidorError -1' in front
    def test_pomidor_PomidorDataFeedNoAngleKeysProvided(self):
        with pytest.raises(PomidorDataFeedNoAngleKeysProvided):
            po.run(data_file, feature="csv_data3")  # prints Exception

    # has 'PomidorError -1' in front
    def test_pomidor_PomidorDataFeedNoCSVFileProvided(self):
        with pytest.raises(PomidorDataFeedNoCSVFileProvided):
            po.run(data_file, feature="csv_data4")  # prints Exception

    # Final Test Summary NOT printed: crazytomato -1 found
    # prints Exception
    def test_pomidor_run_is_displayed_negative(self):  #
        with pytest.raises(PomidorObjectDoesNotExistOnPage):
            po.run(assert_actions, feature="Is_displayed", wait=3)

    def test_pomidor_prereq_not_found(self):
        with pytest.raises(PomidorPrerequisiteScenarioNotFoundError):
            po.run(prereqs_test3, wait=2)

    def test_pomidor_empty_dir(self):
        with pytest.raises(FileNotFoundError):
            po.run(empty_str)
            print("Sucess")  # Exception printed

    def test_pomidor_prerequisite_file_timeout_on_type_action(self):
        with pytest.raises(PomidorObjectDoesNotExistOnPage):
            po.run(prereqs2, wait=2, feature="timeout_test")  # raised
