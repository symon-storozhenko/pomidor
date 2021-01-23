from selenium.webdriver.support.color import Colors

pomidor = 'Pomidor'


class PomidorKeyDoesNotExist(Exception):
    """PomidorCantRunOneBrowserInstanceInParallel Exception"""

    def __init__(self, key):
        self.key = key

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR\nKeyboard key {self.key} does ' \
               f'not exist{Colors.ENDC}'


class PomidorCantRunOneBrowserInstanceInParallel(Exception):
    """PomidorCantRunOneBrowserInstanceInParallel Exception"""

    def __init__(self):
        pass

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR\nCannot run browser=\'one\' ' \
               f'with parallel enabled.\nEither set browser=\'per_file\' or ' \
               f'browser=\'per_test\' or remove parallel from run(..) function' \
               f'{Colors.ENDC}'


class PomidorDataFeedNoKeyError(Exception):
    """ Pomidor syntax error class: more actions than objects """

    def __init__(self, path, line_num, key, data_file):
        self.key = key
        self.path = path
        self.line_num = line_num
        self.data_file = data_file

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR\n' \
               f'{Colors.FAIL}"PomidorDataFeedNoKeyError\n' \
               f'File Path: {self.path}\nParagraph starts on line: ' \
               f'{self.line_num}\n"{self.data_file}" file doesn\'t have ' \
               f'<<{self.key}>> column{Colors.ENDC}\n'


class PomidorDataFeedNoAngleKeysProvidedException(Exception):
    """ PomidorDataFeedNoAngleKeysProvidedException"""

    def __init__(self, path, line_num, data_file):
        self.path = path
        self.line_num = line_num
        self.data_file = data_file

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR\n' \
               f'PomidorDataFeedNoAngleKeysProvidedException\n' \
               f'File Path: {self.path}\nParagraph starts on line: ' \
               f'{self.line_num}\nPlease include csv column ' \
               f'names in double angle quotes: \nExample: {Colors.WARNING}' \
               f'type <<FirstName>>\n{Colors.ENDC}'


class PomidorDataFeedNoCSVFileProvided(Exception):
    """ PomidorDataFeedNoAngleKeysProvidedException"""

    def __init__(self, path, line_num, data_file):
        self.path = path
        self.line_num = line_num
        self.data_file = data_file

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR\n' \
               f'PomidorDataFeedNoCSVFileProvided\n' \
               f'File Path: {self.path}\nParagraph starts on line: ' \
               f'{self.line_num}\nIf you want to use keys from double angle ' \
               f'brackets {Colors.WARNING}<<key>>{Colors.FAIL}, add ' \
               f'{Colors.WARNING}@data marker {Colors.FAIL} with a csv file ' \
               f'in the beginning of your paragraph.\nExample: ' \
               f'{Colors.WARNING}\n@data csv_file_name.csv{Colors.FAIL}' \
               f'\nSome paragraph text..."{Colors.ENDC}'


class PomidorFileNotFoundError(Exception):
    """ Pomidor syntax error class: more actions than objects """

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR\nPomidorFileNotFoundError' \
               f'No pomidor files found.\nFile Path: {self.path}{Colors.ENDC}'


class PomidorSyntaxErrorTooManyActions(Exception):
    """ Pomidor syntax error class: more actions than objects """

    def __init__(self, path, line_num, *args, **kwargs):
        self.path = path
        self.line_num = line_num

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR\n' \
               f'PomidorSyntaxErrorTooManyActions\nFile Path: ' \
               f'{self.path}\nParagraph starts on line: {self.line_num}\n' \
               f'ERROR: You have more actions than objects. Number of actions ' \
               f'(click, type, wait, etc.) should match number of your objects' \
               f' (Ex. #home_button){Colors.ENDC}'


class PomidorSyntaxErrorTooManyObjects(Exception):
    """ Pomidor syntax error class: more objects than actions """

    def __init__(self, path, line_num, *args, **kwargs):
        self.path = path
        self.line_num = line_num

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR\n' \
               f'PomidorSyntaxErrorTooManyObjects' \
               f'\nFile Path: {self.path}\nParagraph ' \
               f'starts on line: {self.line_num}\nERROR: You have more ' \
               f'objects than actions. Number of actions ' \
               f'(click, type, wait, etc.) should match number of your ' \
               f'objects (Ex. #home_button){Colors.ENDC}'


class PomidorObjectDoesNotExistInCSVFile(Exception):
    """ Pomidor syntax error class: Page object does not exist on the page """

    def __init__(self, path, line_num, obj, *args, **kwargs):
        self.path = path
        self.line_num = line_num
        self.obj = obj

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR\n' \
               f'PomidorObjectDoesNotExistInCSVFile\nFilePath: ' \
               f'{self.path}\nParagraph starts on line: {self.line_num}\n' \
               f'ERROR:  {Colors.WARNING}#{self.obj}{Colors.FAIL} does not ' \
               f'exist in page object csv file.' \
               f' Please check page object selector and value{Colors.ENDC}'


class PageObjectNotFound(Exception):
    """ Pomidor syntax error class: Page object does not exist on the page """

    def __init__(self, path, line_num, obj):
        self.path = path
        self.line_num = line_num
        self.obj = obj

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR{Colors.ENDC}\n' \
               f'{Colors.FAIL}PageObjectNotFound{Colors.ENDC}\n' \
               f'{Colors.FAIL}FilePath: {self.path}\n' \
               f'Paragraph starts on line: {self.line_num}\nERROR: {Colors.WARNING}' \
               f'#{self.obj}{Colors.FAIL} was not found on page.' \
               f' Please check page object selector and value{Colors.ENDC}'


class PomidorAssertError(Exception):
    """ Pomidor syntax error class: Page object does not exist on the page """

    def __init__(self, path, line_num, obj, act):
        self.path = path
        self.line_num = line_num
        self.obj = obj
        self.act = act

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR{Colors.ENDC}\n' \
               f'{Colors.FAIL}PomidorAssertError{Colors.ENDC}\n' \
               f'{Colors.FAIL}FilePath: {self.path}\n' \
               f'Paragraph starts on line: {self.line_num}\nERROR:  ' \
               f'{Colors.WARNING}#{self.obj} is {self.act}{Colors.FAIL} ' \
               f'is FALSE {Colors.ENDC}'


class ElementNotClickable(Exception):
    """ Pomidor syntax error class: Page object does not exist on the page """

    def __init__(self, path, line_num, obj):
        self.path = path
        self.line_num = line_num
        self.obj = obj

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR{Colors.ENDC}\n' \
               f'{Colors.FAIL}ElementNotClickable{Colors.ENDC}\n' \
               f'{Colors.FAIL}FilePath: {self.path}\n' \
               f'Paragraph starts on line: {self.line_num}\nERROR:  ' \
               f'{Colors.WARNING}#{self.obj}{Colors.FAIL} is ' \
               f'hidden from view. Consider using \'max\' and/or \'scroll\'\n' \
               f'Example:\n{Colors.WARNING}@params max, scroll\n{Colors.ENDC}'


class PomidorPrerequisiteScenarioNotFoundError(Exception):
    def __init__(self, path, line_num, prereq_path, story, *args, **kwargs):
        self.path = path
        self.line_num = line_num
        self.prereq_path = prereq_path
        self.story = story

    def __repr__(self):
        return f'{Colors.FAIL}\n{pomidor}ERROR\n' \
               f'PomidorPrerequisiteScenarioNotFoundError\n' \
               f'FilePath: {self.path}\nParagraph starts on line ' \
               f'{self.line_num}\nERROR: {Colors.WARNING}{self.story}' \
               f'{Colors.FAIL} prerequisite scenario not found in ' \
               f'prerequisites file ' \
               f'{Colors.WARNING}{self.prereq_path}{Colors.ENDC}'


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[91m'
