from selenium.webdriver.common.keys import Keys

#direct driver.actions
# driver.get("http://www.python.org")
# driver.title
# driver.close()


#operations on objects
class ForwardAction:
    def __init__(self):
        self.forward_action_dictionary = {
            '*click': 'click()',
            '*type': 'send_keys()',
            '*clear': 'clear()',
        #     ActionChains:
        }


class BackwardAction:
    def __init__(self):
        self.backward_actions_dictionary = {
            '*page_title': 'title',
            '*visible': 'is_displayed()',
            '*not visible': 'test',
            '*enabled': 'is_enabled()',
            '*selected': 'is_selected()',
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

print(act.forward_action_dictionary)
