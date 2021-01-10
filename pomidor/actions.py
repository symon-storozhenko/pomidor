
# direct driver.actions
# driver.get("http://www.python.org")
# driver.title
# driver.close()


class InputKeys:
    def __init__(self):
        self.keys = ['ARROW_LEFT']


#operations on objects
class ForwardAction:
    def __init__(self):
        self.forward_action_dictionary = {
            'click': 'click()',
            'clicks': 'click()',
            'clicked': 'click()',
            'type': 'send_keys()',
            'types': 'send_keys()',
            'typed': 'send_keys()',
            'clear': 'clear()',
            'press': "Key",
            'pressed': "Key",
            'presses': "Key",
            'wait': 'wait',

            #     ActionChains:
        }


class BackwardAction:
    def __init__(self):
        self.backward_actions_dictionary = {
            'page_title': 'titles',
            'displayed': 'is_displayed()',
            'enabled': 'is_enabled()',
            'selected': 'is_selected()',
            'not_displayed': 'is_displayed()',
        }


#obj.send_keys(Keys.RETURN)
board_keys = ['RETURN', 'Esc']


# Expected conditions:
# title_is
# title_contains
# presence_of_element_located
# visibility_of_element_located
# visibility_of
# presence_of_all_elements_located
# text_to_be_present_in_element
# text_to_be_present_in_element_value
# frame_to_be_available_and_switch_to_it
# invisibility_of_element_located
# element_to_be_clickable
# staleness_of
# element_to_be_selected
# element_located_to_be_selected
# element_selection_state_to_be
# element_located_selection_state_to_be
# alert_is_present
# from selenium.webdriver.support import expected_conditions as EC
# Example:
# wait = WebDriverWait(driver, 10)
# element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))

vector = 'forward_action_dictionary'

act = ForwardAction()

