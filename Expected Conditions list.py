# class selenium.webdriver.support.expected_conditions.alert_is_present[source]
# Expect an alert to be present.


def action_func_visible(act, obj_source, wait, locator):  # TODO implement passing wait parameter
    return f'WebDriverWait(driver, {wait}).until(ec.visibility_of_element_' \
           f'located((By.{locator},\'{obj_source}\'))).{act}'


def send_keys_func(str_list):
    return f"send_keys(\"{str_list.pop(0)}\")"


def action_func_clickable(act, obj_source, locator, wait, *str_list):  # TODO implement passing wait parameter
    if act == "click()" or act == "send_keys()":
        if act == "send_keys()":
            act = send_keys_func(str_list)
    return f'WebDriverWait(driver, {wait}).until(ec.element_to_be_clickable' \
           f'((By.{locator},\'{obj_source}\'))).{act}'


def which_action(act, obj_source, locator, wait=10, *str_list):
    if act == "click()" or act == "send_keys()":
        func = action_func_clickable(act, obj_source, locator, 10, *str_list)
    else:
        func = action_func_visible(act, obj_source, 10, locator)
    return func

#
# TODO #2 class selenium.webdriver.support.expected_conditions.element_to_be_clickable(locator)[source]
# An Expectation for checking an element is visible and enabled such that you can click it.
#
# class selenium.webdriver.support.expected_conditions.element_to_be_selected(element)[source]
# An expectation for checking the selection is selected. element is WebElement object
#
# class selenium.webdriver.support.expected_conditions.invisibility_of_element(locator)[source]
# An Expectation for checking that an element is either invisible or not present on the DOM.
# element is either a locator (text) or an WebElement
#
# class selenium.webdriver.support.expected_conditions.title_is(title)[source]
# An expectation for checking the title of a page. title is the expected title,
# which must be an exact match returns True if the title matches, false otherwise.
#
# TODO #1 class selenium.webdriver.support.expected_conditions.visibility_of_element_located(locator)[source]
# An expectation for checking that an element is present on the DOM of a page and visible. Visibility
# means that the element is not only displayed but also has a height and width that is greater than 0.
# locator - used to find the element returns the WebElement once it is located and visible