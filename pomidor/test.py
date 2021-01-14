import itertools
from collections import defaultdict
from csv import DictReader

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from pomidor.pomidor_init import BrowserInit, PomidorObjAndURL, Pom
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from pomidor.actions import ForwardAction, BackwardAction

# pomi = BrowserInit("Chrome", 'https://pomidor-automation.com/')
# driver = pomi.define_browser()
# with driver as d:
#     d.get('https://pomidor-automation.com/practice/')

act = ForwardAction()
bact = BackwardAction()
backward_action_dict = bact.backward_actions_dictionary
forward_action_dict = act.forward_action_dictionary

d = backward_action_dict.keys()
print(d)

for item in forward_action_dict.values():
    print(item)

if "click()" in forward_action_dict.keys():
    print("yay!")

url = 'https://pomidor-automation.com/'

import numpy as np


def get_csv_data_first_row(file: str) -> dict:
    with open(file) as f:
        csv_reader = DictReader(f, delimiter=',', quotechar='"')
        titles = [list(x.keys()) for x in csv_reader]
        title = titles[0]
        values = [list(y.values()) for y in csv_reader]
        csv_dict = [{k: v for k, v in row.items()}
                    for row in csv_reader]

        print(f'titles -> {title}')
        print(f'values -> {values}')
        print(f'csv_dict -> {csv_dict}')
    return title


print(get_csv_data_first_row("urls.csv"))


def additional_urls(urls_file: str) -> dict:
    with open(urls_file) as csv_url_file:
        csv_reader = DictReader(csv_url_file, delimiter=',', quotechar='"')
        url_dict = {rows['name'].strip(): rows['url'].strip() for rows in
                    csv_reader}
    return url_dict


print(additional_urls("urls.csv"))

f = 'urls.csv'
dr = DictReader(open(f))
dict_of_lists = {}
for k in dict_of_lists.keys():
    dict_of_lists[k] = [dict_of_lists[k]]
for line in dr:
    for k in dict_of_lists.keys():
        dict_of_lists[k].append(line[k])

print(f'dict_of_lists-> {dict_of_lists}')


def get_csv_data_values(file: str, key: str) -> dict:
    with open(file) as csv_file:
        titles = get_csv_data_first_row(file)
        csv_reader = DictReader(csv_file, delimiter=',', quotechar='"')
        print(f'titles -> {titles}')
        url_dict = {}
        values_list = [rows[key] for rows in csv_reader]
        url_dict[key] = values_list
        print(f'url_dic -> {url_dict}')
        print(f'url_dict.values() -> {url_dict.values()}')
        print(f'url_dict.values() list -> {list(url_dict.values())[0]}')

        for enum, i in enumerate(list(url_dict.values())[0]):
            print(f'i -> {i}')
            # print(f'url_dict -> {url_dict}')
            print(
                f'url_dict.values() after delete -> {list(url_dict.values())[0]}')

        #
        # url_dict = {rows['name'].strip(): rows['url'].strip() for rows in
        #             csv_reader}
    return url_dict


print(f'url_dict -> {get_csv_data_values("urls.csv", "url")}')


def get_list_of_dicts_from_csv(file):
    with open(file) as read_obj:
        # pass the file object to DictReader() to get the DictReader object
        dict_reader = DictReader(read_obj)
        # get a list of dictionaries from dct_reader
        list_of_dict = list(dict_reader)
        # print list of dict i.e. rows
        print(list_of_dict)
    return list_of_dict


get_list_of_dicts_from_csv('../tests/pageObjects/csv_data_source.csv')

import sys
import io

old_stdout = sys.stdout  # Memorize the default stdout stream
buffer = io.StringIO()

print(f'sys.stdout -> {buffer.getvalue()}')


def list1(k):
    for i in range(10):
        return k + "{i}"


a = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# for i in range(10):
#     print(a.(i+3).pop(0))

keys = {'ADD': '\ue025',
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
