from tests.pageObjects.page_factory import PageObject, BaseURL
from pomidor.pomidor_runner import Pomidor
from pomidor.pomidor_runner import PomidorSyntaxError, PomidorObjectNotFound
import pytest

art_url = 'https://pomidor-automation.com/'
po = PageObject()
burl = BaseURL()

to = Pomidor('Chrome', po.home_page, art_url, burl.urls)

to.delete_all_cookies()
to.max_window()
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
no_obj_in_page_fctry= 'negative_pomidory/obj_not_found_in_page_factory.pomidor'
last_orphan_obj = 'negative_pomidory/last_orphan_obj.pomidor'
last_line_3_scenarios = 'negative_pomidory/last_line_is_read.pomidor'
run_three_3344_stories = "negative_pomidory/run_story.pomidor"
pro_pomidor = 'negative_pomidory/pro.pomidor'


class TestPomidorPro:
    def test_pomidor_pro(self):
        scenario_num = to.run_story(pro_pomidor, '3422')
        assert scenario_num == 3


class TestPomidor:
    def test_pomidor_empty_dir(self):
        with pytest.raises(FileNotFoundError):
            to.run_scripts(empty_str)
            print("Sucess")

    def test_pomidor_run_story(self):
        scenario_num = to.run_story(run_three_3344_stories, '3344', wait=3)
        assert scenario_num == 3

    def test_pomidor_run_url_story(self):
        scenario_num = to.run_story(run_three_3344_stories, 'JIRA-0044_0',
                                    wait=2)
        assert scenario_num == 1

    def test_pomidor_run_feature(self):
        """Can't run theis yet"""
        scenario_num = to.run_features(run_three_3344_stories, 'Report')
        assert scenario_num == 3

    def test_pomidor_run_story_with_general_script(self):
        scenario_num = to.run_scripts(run_three_3344_stories)
        assert scenario_num == 4

    def test_pomidor_run_exact_story_name(self): # "Jira1 NOT Jira 1 !!
        scenario_num = to.run_story(run_three_3344_stories, "JIRA-3344_2",
                                    exact_match=True)
        assert scenario_num == 1

    def test_pomidor_run_exact_feature_name(self):  # Repo1 not Repo 1 !
        scenario_num = to.run_features(run_three_3344_stories, "Reporting",
                                       exact_match=True)
        assert scenario_num == 2

    def test_pomidor_pass_several_stories_to_run(self):
        # TODO pass_several_stories_to_run
        pass

    def test_pomidor_run_custom_marker(self):
        scenario_num = to.run_custom_identifier(run_three_3344_stories,
                                                "@Custom_Marker", "Get_Marker",
                                                exact_match=True)
        assert scenario_num == 1

    def test_pomidor_several_custom_markers(self):
        # TODO several custom markers
        pass

    def test_pomidor_list_all_story_values(self):
        marker_list_length, unique_num = \
            to.list_all_marker_values(run_three_3344_stories,
                                                "@story")
        assert marker_list_length == 6

    def test_pomidor_list_all_feature_values(self):
        marker_list_length, unique_num = \
            to.list_all_marker_values(run_three_3344_stories,
                                                       "@featurE")
        assert marker_list_length == 5

    def test_pomidor_list_unique_story_values(self):
        marker_list_length, unique_num = \
            to.list_all_marker_values(run_three_3344_stories,
                                                "@story")
        assert unique_num == 5

    def test_pomidor_list_unique_feature_values(self):
        marker_list_length, unique_num = to.list_all_marker_values(run_three_3344_stories,
                                                       "@featurE")
        assert unique_num == 4

    def test_pomidor_list_unique_url_marker_values(self):
        marker_list_length, unique_num = \
            to.list_all_marker_values(run_three_3344_stories,
                                                "@base_url")
        assert unique_num == 1

    def test_pomidor_list_all_url_marker_values(self):
        marker_list_length, unique_num = \
            to.list_all_marker_values(run_three_3344_stories,
                                                "@base_url")
        assert marker_list_length == 2

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