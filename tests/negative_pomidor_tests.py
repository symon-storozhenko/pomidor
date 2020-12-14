from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from tests.pageObjects.page_factory import PageObject, BaseURL
from pomidor.pomidor_runner import Pomidor
from pomidor.pomidor_runner import PomidorSyntaxErrorTooManyObjects,\
    PomidorSyntaxErrorTooManyActions, PomidorObjectNotFound
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


# to.run(run_story, 'Report')
# to.run_scripts_parallelly(smoke_test_dir, wait=3)


class TestPomidorPro:
    def test_pomidor_pro(self):
        scenario_num = to.run(pro_pomidor, feature='SmokeTest')
        assert scenario_num == 2


class TestPomidor:

    def test_pomidor_empty_dir(self):
        with pytest.raises(FileNotFoundError):
            to.run(empty_str)
            print("Sucess")

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
            to.run(assert_actions, feature="Is_Displayed")

    def test_pomidor_run_not_displayed(self):
        scenario_num = to.run(assert_actions, feature="Not_Displayed")
        assert scenario_num == 1


    def test_pomidor_csv_data(self):
        scenario_num = to.run(data_file, feature="csv_data")
        assert scenario_num == 1

    #
    #
    # def test_pomidor_run_exact_feature_name(self):  # Repo1 not Repo 1 !
    #     scenario_num = to.run(run_story, "Reporting")
    #     assert scenario_num == 1
    #
    # def test_pomidor_list_all_feature_values(self):
    #     marker_list_length, unique_num = \
    #         to.list_all_marker_values(run_story,
    #                                   "@featurE")
    #     assert marker_list_length == 5
    #
    # def test_pomidor_list_unique_feature_values(self):
    #     marker_list_length, unique_num = to.list_all_marker_values(
    #         run_story,
    #         "@featurE")
    #     assert unique_num == 4
    #
    # def test_pomidor_list_unique_url_marker_values(self):
    #     marker_list_length, unique_num = \
    #         to.list_all_marker_values(run_story,
    #                                   "@url")
    #     assert unique_num == 0
    #
    # def test_pomidor_list_all_url_marker_values(self):
    #     marker_list_length, unique_num = \
    #         to.list_all_marker_values(run_story,
    #                                   "@url")
    #     assert marker_list_length == 2


class TestPomidorSyntaxPositive:
    def test_pomidor_last_line_is_read(self):
        scenario_num = to.run(last_line_3_scenarios)
        assert scenario_num == 3


class TestPomidorSyntaxNegative:
    def test_pomidor_more_than_1_obj_bckwrd_action_except(self):
        with pytest.raises(PomidorSyntaxErrorTooManyObjects
                           ):
            to.run(more_than_1_back)

    def test_pomidor_orphan_obj_b4_frwd_action(self):
        with pytest.raises(PomidorSyntaxErrorTooManyActions):
            to.run(orph_obj_b4_frwd_act)

    def test_pomidor_two_actions(self):
        with pytest.raises(PomidorSyntaxErrorTooManyActions):
            to.run(two_actions)

    def test_pomidor_no_obj_found(self):
        with pytest.raises(PomidorSyntaxErrorTooManyActions):
            to.run(no_obj_found)

    def test_pomidor_no_obj_in_page_fctry(self):
        with pytest.raises(PomidorObjectNotFound):
            to.run(no_obj_in_page_fctry)

    def test_pomidor_last_orphan_obj(self):
        with pytest.raises(PomidorSyntaxErrorTooManyObjects):
            to.run(last_orphan_obj)

# driver.quit()
