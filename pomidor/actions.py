# direct driver.actions
# driver.get("http://www.python.org")
# driver.title
# driver.close()


class InputKeys:
    def __init__(self):
        self.keys = {'ADD': '\ue025',
                     'ALT': '\ue00a',
                     'ARROW_DOWN': '\ue015',
                     'ARROW_LEFT': '\ue012',
                     'ARROW_RIGHT': '\ue014',
                     'ARROW_UP': '\ue013',
                     'BACKSPACE': '\ue003',
                     'BACK_SPACE': '\ue003',
                     'CANCEL': '\ue001',
                     'CLEAR': '\ue005',
                     'COMMAND': '\ue03d',
                     'CONTROL': '\ue009',
                     'DECIMAL': '\ue028',
                     'DELETE': '\ue017',
                     'DIVIDE': '\ue029',
                     'DOWN': '\ue015',
                     'END': '\ue010',
                     'ENTER': '\ue007',
                     'EQUALS': '\ue019',
                     'ESCAPE': '\ue00c',
                     'F1': '\ue031',
                     'F10': '\ue03a',
                     'F11': '\ue03b',
                     'F12': '\ue03c',
                     'F2': '\ue032',
                     'F3': '\ue033',
                     'F4': '\ue034',
                     'F5': '\ue035',
                     'F6': '\ue036',
                     'F7': '\ue037',
                     'F8': '\ue038',
                     'F9': '\ue039',
                     'HELP': '\ue002',
                     'HOME': '\ue011',
                     'INSERT': '\ue016',
                     'LEFT': '\ue012',
                     'LEFT_ALT': '\ue00a',
                     'LEFT_CONTROL': '\ue009',
                     'LEFT_SHIFT': '\ue008',
                     'META': '\ue03d',
                     'MULTIPLY': '\ue024',
                     'NULL': '\ue000',
                     'NUMPAD0': '\ue01a',
                     'NUMPAD1': '\ue01b',
                     'NUMPAD2': '\ue01c',
                     'NUMPAD3': '\ue01d',
                     'NUMPAD4': '\ue01e',
                     'NUMPAD5': '\ue01f',
                     'NUMPAD6': '\ue020',
                     'NUMPAD7': '\ue021',
                     'NUMPAD8': '\ue022',
                     'NUMPAD9': '\ue023',
                     'PAGE_DOWN': '\ue00f',
                     'PAGE_UP': '\ue00e',
                     'PAUSE': '\ue00b',
                     'RETURN': '\ue006',
                     'RIGHT': '\ue014',
                     'SEMICOLON': '\ue018',
                     'SEPARATOR': '\ue026',
                     'SHIFT': '\ue008',
                     'SPACE': '\ue00d',
                     'SUBTRACT': '\ue027',
                     'TAB': '\ue004',
                     'UP': '\ue013', }


class Locators:
    locator_dict = {
        'CLASS_NAME': 'class name',
        'CSS_SELECTOR': 'css selector',
        'ID': 'id',
        'LINK_TEXT': 'link text',
        'NAME': 'name',
        'PARTIAL_LINK_TEXT': 'partial link text',
        'TAG_NAME': 'tag name',
        'XPATH': 'xpath'
    }


# operations on objects
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
            'not_displayed': 'is_displayed()',
            'enabled': 'is_enabled()',
            'not_enabled': 'is_enabled()',
            'selected': 'is_selected()',
            'not_selected': 'is_selected()',
        }


# obj.send_keys(Keys.RETURN)
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
