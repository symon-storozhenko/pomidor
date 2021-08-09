[![codecov](https://codecov.io/gh/symon-storozhenko/pomidor/branch/master/graph/badge.svg?token=J4KR9CWL9G)](https://codecov.io/gh/symon-storozhenko/pomidor)

# pomidor 0.0.2-Alpha

:tomato:
# **A BDD-style Selenium-driven browser automation(Python) - First Production release coming soon** 
## (with Agile in mind :nerd_face: )
### Fast and flexible approach to automating `click()`, `send_keys()`, `is_displayed()` and many other selenium actions and asserts straight from your Jira/TFS stories 

### Example:
![Pomidor syntax](images/pomidor_2.png)

>In the picture above, you can see that __page objects__ are marked with hashtags. Ex. **#home_page**

### Markers:

>Add __@feature__, __@params__  and __@test__ to personalize your tests:
![Pomidor syntax](images/all_markers.png)

### Quick Start:
Install pomidor

![Page factory](images/pip_install_pomidor2.png)

Create a csv file that contains page objects additional urls. (Example shown below)

![Page factory1](images/page_obj_dict.png)


Write your first test_case.pomidor file (extension must be ".pomidor") and place it in dedicated folder (Ex.: pomidor_files):


![Pomidor syntax](images/pomidor_file.png)


Create a runner file, import Pomidor class and run your first test as shown below:
![Runner file1](images/init_pomidor_class.png)

Add additional functionality to your test:

![Runner file1](images/additional_features.png)


Run your first Automation test! :rocket:

