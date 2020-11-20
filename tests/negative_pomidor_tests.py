from selenium import webdriver
from tests.pageObjects.page_factory import PageObject, BaseURL
from pomidor.pomidor_runner import Pomidor
from pomidor.pomidor_runner import PomidorSyntaxError, PomidorObjectNotFound
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
run_three_3344_stories = "negative_pomidory/run_story.pomidor"
pro_pomidor = 'negative_pomidory/pro.pomidor'
smoke_test_dir = 'negative_pomidory/SmokeTest'


to.run_features(run_three_3344_stories, 'Report')
# to.run_scripts_parallelly(smoke_test_dir, wait=3)


class TestPomidorPro:
    def test_pomidor_pro(self):
        scenario_num = to.run_features(pro_pomidor, 'SmokeTest')
        assert scenario_num == 2


class TestPomidor:

    def test_pomidor_empty_dir(self):
        with pytest.raises(FileNotFoundError):
            to.run_scripts(empty_str)
            print("Sucess")

    def test_pomidor_run_feature(self):
        scenario_num = to.run_features(run_three_3344_stories, 'Report')
        assert scenario_num == 3



    #
    #
    # def test_pomidor_run_exact_feature_name(self):  # Repo1 not Repo 1 !
    #     scenario_num = to.run_features(run_three_3344_stories, "Reporting")
    #     assert scenario_num == 1
    #
    # def test_pomidor_list_all_feature_values(self):
    #     marker_list_length, unique_num = \
    #         to.list_all_marker_values(run_three_3344_stories,
    #                                   "@featurE")
    #     assert marker_list_length == 5
    #
    # def test_pomidor_list_unique_feature_values(self):
    #     marker_list_length, unique_num = to.list_all_marker_values(
    #         run_three_3344_stories,
    #         "@featurE")
    #     assert unique_num == 4
    #
    # def test_pomidor_list_unique_url_marker_values(self):
    #     marker_list_length, unique_num = \
    #         to.list_all_marker_values(run_three_3344_stories,
    #                                   "@url")
    #     assert unique_num == 0
    #
    # def test_pomidor_list_all_url_marker_values(self):
    #     marker_list_length, unique_num = \
    #         to.list_all_marker_values(run_three_3344_stories,
    #                                   "@url")
    #     assert marker_list_length == 2


class TestPomidorSyntaxPositive:
    def test_pomidor_last_line_is_read(self):
        scenario_num = to.run_scripts(last_line_3_scenarios)
        assert scenario_num == 3


class TestPomidorSyntaxNegative:
    def test_pomidor_more_than_1_obj_bckwrd_action_except(self):
        with pytest.raises(PomidorSyntaxError):
            to.run_scripts(more_than_1_back)

    def test_pomidor_orphan_obj_b4_frwd_action(self):
        with pytest.raises(PomidorSyntaxError):
            to.run_scripts(orph_obj_b4_frwd_act)

    def test_pomidor_two_actions(self):
        with pytest.raises(PomidorSyntaxError):
            to.run_scripts(two_actions)

    def test_pomidor_no_obj_found(self):
        with pytest.raises(PomidorSyntaxError):
            to.run_scripts(no_obj_found)

    def test_pomidor_no_obj_in_page_fctry(self):
        with pytest.raises(PomidorObjectNotFound):
            to.run_scripts(no_obj_in_page_fctry)

    def test_pomidor_last_orphan_obj(self):
        with pytest.raises(PomidorSyntaxError):
            to.run_scripts(last_orphan_obj)

# driver.quit()
