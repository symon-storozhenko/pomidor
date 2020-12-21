from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from tests.pageObjects.page_factory import PageObject, BaseURL
from pomidor.pomidor_runner import Pomidor
from pomidor.pomidor_exceptions import PomidorDataFeedNoKeyError, \
    PomidorDataFeedNoAngleKeysProvided, PomidorDataFeedNoCSVFileProvided, \
    PomidorSyntaxErrorTooManyActions, PomidorSyntaxErrorTooManyObjects, \
    PomidorObjectDoesNotExistOnPage
import pytest
import concurrent.futures


url = 'https://pomidor-automation.com/'
page_obj = Pomidor.get_page_objects("pageObjects/page_objects.csv")
addtl_urls = Pomidor.additional_urls("pageObjects/urls.csv")

to = Pomidor("Chrome", page_obj, url, urls=addtl_urls)

# to.delete_all_cookies()
# to.max_window()
# to.fullscreen()

# to.before_tests_launch_url()
# to.quit()

empty_str = 'negative_pomidory/empty_dir'
nested_dir = 'negative_pomidory/SmokeTest'
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
obj_in_page_factory_but_not_on_webpage = \
    'negative_pomidory/obj_in_page_factory_but_not_on_webpage.pomidor'


# to.run(run_story, 'Report')


class TestPomidorPro:
    def test_pomidor_pro(self):
        scenario_num = to.run(pro_pomidor, feature='SmokeTest')
        assert scenario_num == 2


class TestPomidor:

    def test_pomidor_empty_dir(self):
        with pytest.raises(FileNotFoundError):
            to.run(empty_str)
            print("Sucess")

    # count = 3
    #
    # # runs the function 3 times
    # @pytest.mark.parametrize("counting", range(count))
    # def test_pomidor_run_all_and_nested_dir(self, counting):
    def test_pomidor_run_all_and_nested_dir(self):
        scenario_num = to.run(nested_dir)
        assert scenario_num == 3

    def test_pomidor_run_feature(self):
        scenario_num = to.run(run_story,
                              feature='Report')
        assert scenario_num == 3

    def test_pomidor_run_is_displayed(self):
        scenario_num = to.run(run_story,
                              feature="Reporting")
        assert scenario_num == 1

    def test_pomidor_run_is_displayed_negative(self):
        with pytest.raises(TimeoutException):
            to.run(assert_actions, feature="Is_displayed")

    def test_pomidor_run_not_displayed(self):
        scenario_num = to.run(assert_actions, feature="Not_Displayed")
        assert scenario_num == 1

    def test_pomidor_csv_data(self):
        scenario_num = to.run(data_file, feature="csv_data")
        assert scenario_num == 1

    def test_pomidor_feature_list_csv_data1(self):
        scenario_num = to.run(data_file, feature="csv_data1")
        assert scenario_num == 1

    def test_pomidor_feature_list_csv_data2(self):
        scenario_num = to.run(data_file, feature="csv_data2")
        assert scenario_num == 1

    def test_pomidor_orphan_obj_b4_frwd_action(self):
        scenario_num = to.run(orph_obj_b4_frwd_act)
        assert scenario_num == 1


class TestPomidorSyntaxPositive:
    def test_pomidor_last_line_is_read(self):
        scenario_num = to.run(last_line_3_scenarios)
        assert scenario_num == 3


class TestPomidorSyntaxNegative:
    def test_pomidor_more_than_1_obj_bckwrd_action_except(self):
        with pytest.raises(PomidorSyntaxErrorTooManyObjects
                           ):
            to.run(more_than_1_back)

    def test_pomidor_two_actions(self):
        with pytest.raises(PomidorSyntaxErrorTooManyActions):
            to.run(two_actions)

    def test_pomidor_no_obj_found(self):
        with pytest.raises(PomidorSyntaxErrorTooManyActions):
            to.run(no_obj_found)

    def test_pomidor_no_obj_in_page_fctry(self):
        with pytest.raises(PomidorObjectDoesNotExistOnPage):
            to.run(no_obj_in_page_fctry)

    def test_pomidor_last_orphan_obj(self):
        with pytest.raises(PomidorSyntaxErrorTooManyObjects):
            to.run(last_orphan_obj)

    def test_pomidor_obj_in_page_factory_but_not_on_webpage(self):
        with pytest.raises(PomidorObjectDoesNotExistOnPage):
            to.run(obj_in_page_factory_but_not_on_webpage)

    def test_pomidor_csv_data_none_key_error(self):
        with pytest.raises(PomidorDataFeedNoKeyError):
            to.run(data_file, feature="csv_data7")

    def test_pomidor_PomidorDataFeedNoAngleKeysProvided(self):
        with pytest.raises(PomidorDataFeedNoAngleKeysProvided):
            to.run(data_file, feature="csv_data3")

    def test_pomidor_PomidorDataFeedNoCSVFileProvided(self):
        with pytest.raises(PomidorDataFeedNoCSVFileProvided):
            to.run(data_file, feature="csv_data4")
# driver.quit()
