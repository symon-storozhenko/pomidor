
def go_thru_pomidor_file(func, obj_dict):
    scenario_number = 0
    for file_number, filepath in enumerate(func):
        with open(filepath) as file:
            for total_lines_count, row in enumerate(file):
                continue
        with open(filepath) as tomato_file:
            print(f'\nOpening file --> {filepath}\n')
            scenarioSteps = ''
            first_paragraph_line = ''
            for line_num, line in enumerate(tomato_file):
                if scenarioSteps == '' and (
                        line in ['\n', '\r\n'] or line.startswith('--')):
                    continue
                else:
                    if scenarioSteps == '':
                        first_paragraph_line = line
                        scenario_title_line_num = line_num
                    if scenarioSteps != '' and line.startswith('--'):
                        continue
                    scenarioSteps += line
                if (scenarioSteps != '' and line in ['\n', '\r\n']) or (
                        scenarioSteps != '' and line_num == total_lines_count):
                    print(f'LINE IS -----> {line} at {line_num}')
                    print(
                        f"\nBegin test:\n ----{first_paragraph_line.strip()}----"
                        f"\nActions and Assertions performed:")
                    # scenarioSteps += line
                    # with regex
                    print(f'srtList --> {scenarioSteps}')
                    test_paragraph = \
                        define_test_paragraphs(scenarioSteps, filepath,
                                               first_paragraph_line,
                                               scenario_title_line_num,
                                               line_num, obj_dict)
                    if test_paragraph:
                        scenario_number += 1
                    scenarioSteps = ''
    return file_number, scenario_number

