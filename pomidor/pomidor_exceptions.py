class PomidorDataFeedError(KeyError):
    """ Pomidor syntax error class: more actions than objects """

    def __init__(self, file_path, line_num, data_file, *args, **kwargs):
        self.file_path = file_path
        self.line_num = line_num
        self.data_file = data_file

    def print_error_header(self, line_num, data_file):
        print(f'{Colors.FAIL}PomidorDataFeed ERROR:\nPomidor File Path:'
              f' {self}\nParagraph starts on line: {line_num}\n'
              f'csv file: {data_file}{Colors.ENDC}')


class PomidorDataFeedNoKeyError(PomidorDataFeedError):
    """ Pomidor syntax error class: more actions than objects """

    def __init__(self, path, line_num, key, data_file, *args, **kwargs):
        self.key = key
        PomidorDataFeedError.print_error_header(path, line_num, data_file)
        print(f'{Colors.FAIL}"{data_file}" file doesn\'t have <<{key}>> '
              f'column{Colors.ENDC}')


class PomidorDataFeedNoAngleKeysProvided(PomidorDataFeedError):
    """ PomidorDataFeedNoAngleKeysProvided"""
    def __init__(self, path, line_num, data_file, *args, **kwargs):
        PomidorDataFeedError.print_error_header(path, line_num, data_file)
        print(f'{Colors.FAIL}Please include csv column names in double angle '
              f'quotes: Example: type <<FirstName>>\n{Colors.ENDC}')


class PomidorDataFeedNoCSVFileProvided(PomidorDataFeedError):
    """ PomidorDataFeedNoAngleKeysProvided"""
    def __init__(self, path, line_num, data_file, *args, **kwargs):
        PomidorDataFeedError.print_error_header(path, line_num, data_file)
        print(f'{Colors.FAIL}Please add @data with a csv file in the '
              f'beginning of your paragraph.\nExample: '
              f'\n"@data csv_file_name.csv'
              f'\nSome paragraph text..."{Colors.ENDC}')


class PomidorFileNotFoundError(FileNotFoundError):
    """ Pomidor syntax error class: more actions than objects """

    def __init__(self, path, *args, **kwargs):
        self.path = path
        print(f'{Colors.FAIL}PomidorFileNotFoundError:\nFile Path: '
              f'{path}{Colors.ENDC}')


class PomidorSyntaxErrorTooManyActions(Exception):
    """ Pomidor syntax error class: more actions than objects """

    def __init__(self, path, line_num, *args, **kwargs):
        self.path = path
        self.line_num = line_num
        print(f'{Colors.FAIL}Pomidor Syntax ERROR:\nFile Path: '
              f'{path}\nParagraph starts on line: {line_num}\n'
              f'ERROR: You have more actions than objects. Number of actions '
              f'(click, type, wait, etc.) should match number of your objects '
              f'(Ex. #home_button){Colors.ENDC}')


class PomidorSyntaxErrorTooManyObjects(Exception):
    """ Pomidor syntax error class: more objects than actions """

    def __init__(self, path, line_num, *args, **kwargs):
        self.path = path
        self.line_num = line_num
        print(f'{Colors.FAIL}Pomidor Syntax ERROR:\nFile Path: '
              f'{path}\nParagraph starts on line: {line_num}\n'
              f'ERROR: You have more objects than actions. Number of actions '
              f'(click, type, wait, etc.) should match number of your objects '
              f'(Ex. #home_button){Colors.ENDC}')


class PomidorObjectDoesNotExistOnPage(Exception):
    """ Pomidor syntax error class: Page object does not exist on the page """

    def __init__(self, path, line_num, obj, *args, **kwargs):
        self.path = path
        self.line_num = line_num
        self.obj = obj
        print(f'{Colors.FAIL}Pomidor Syntax ERROR:\nFilePath: {path}\n'
              f'Paragraph starts on line: {line_num}\nERROR:  {Colors.WARNING}'
              f'#{obj}{Colors.FAIL} does not exist on the page or in csv file.'
              f' Please check page object selector and value{Colors.ENDC}')


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