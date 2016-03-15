#!/usr/bin/python3.5
import json
import os
import re
import sys
import threading
from getopt import getopt, GetoptError
from urllib import request

import requests

usage = 'savethewiki [-q =False] [-n =10] <Number of Search Results> [-r =False] [-s] <Search Query>'

SILENT_MODE = False
NUMBER_OF_SEARCH_RESULTS = 10
LANGUAGE = 'en'
REGEX = False
SEARCH_PARAMETER = ''
INPUT_SEARCH = True
DIRECT_SEARCH = False
URL = ''
remaining = 0


def smart_print(level, msg):
    if not SILENT_MODE:
        tabs = ''
        while level > 0:
            tabs += '\t'
            level -= 1
        print(tabs + msg)


def process_arguments(level, argv):
    global SILENT_MODE, NUMBER_OF_SEARCH_RESULTS, LANGUAGE, REGEX, SEARCH_PARAMETER, INPUT_SEARCH, DIRECT_SEARCH, URL

    try:
        options, args = getopt(argv, "qn:rs:p:",
                               ['--quiet', 'number-search=', 'regex-mode', 'search-parameter=', '--page-name'])
    except GetoptError as err:
        smart_print(level, err)
        smart_print(level, usage)
        sys.exit()

    for opt, arg in options:
        if opt in ('-q', '--quiet'):
            SILENT_MODE = True
        elif opt in ('-n', '--number-search'):
            NUMBER_OF_SEARCH_RESULTS = arg
        elif opt in ('-r', '--regex-mode'):
            REGEX = True
        elif opt in ('-s', '--search-parameter'):
            SEARCH_PARAMETER = arg
            INPUT_SEARCH = False
        elif opt in ('-p', '--page-name'):
            SEARCH_PARAMETER = arg
            DIRECT_SEARCH = True

    URL = 'https://' + LANGUAGE + '.wikipedia.org/w/api.php'


def regex(level):
    smart_print(level, 'Not available right now.')
    return


def normal(level):
    global SEARCH_PARAMETER, INPUT_SEARCH

    if INPUT_SEARCH:
        SEARCH_PARAMETER = input('Enter search parameter : ')

    params_to_put = {
        'action': 'query',
        'list': 'search',
        'srlimit': NUMBER_OF_SEARCH_RESULTS,
        'srsearch': SEARCH_PARAMETER,
        'format': 'json'
    }

    smart_print(level, "Fetching search results")
    response = requests.get(URL, params=params_to_put)
    parsed_json = json.loads(response.text)
    results = parsed_json['query']['search']

    count = 0
    for result in results:
        smart_print(level, '[' + str(count) + ']: ' + result['title'])
        count += 1

    user_response = input('Enter Choice : ')

    responses = user_response.split(' ')

    count = 0
    for result in results:
        title = result['title']
        if str(count) in responses:
            download_page(level, title.replace(' ', '_'))
        count += 1


def download_file(level, src, dst):
    global remaining
    smart_print(level, 'Downloading file ' + src + ' to ' + dst)
    request.urlretrieve(src, dst)
    smart_print(level, 'Downloaded ' + dst )


def download_page(level, pagename):
    params_to_put = {
        'action': 'parse',
        'page': pagename,
        'format': 'json'
    }

    smart_print(level, 'Requesting data for page ' + pagename.replace('_', ' '))
    response = requests.get(URL, params=params_to_put);

    parsed_json = json.loads(response.text)
    if response.status_code != 200:
        smart_print(level + 1, 'Error fetching data.')
        return

    if not os.path.exists('stwdata'):
        os.mkdir('stwdata')

    prefix = 'stwdata/' + pagename

    html_content = parsed_json['parse']['text']['*']

    html_content = html_content \
        .replace('href=\"//', 'href=\"https://') \
        .replace('href=\"/', 'href=\"https://en.wikipedia.org/')

    imgs = re.findall('src="([^"]+)"', html_content)

    if not os.path.exists(prefix):
        os.mkdir(prefix)

    count = 0
    for img in imgs:
        file_name = str(count) + '.' + img.split('/')[-1].split('.')[-1]
        file_name_full = prefix + '/' + file_name
        file_url = 'https:' + img
        download_file(level+1, file_url, file_name_full)
        html_content = html_content.replace(img, os.getcwd() + '/' + file_name_full)
        count += 1

    fo = open(pagename + '.html', "w")
    fo.write(html_content)
    fo.close()

    return


if __name__ == "__main__":
    process_arguments(0, sys.argv[1:])

    if DIRECT_SEARCH:
        download_page(0, SEARCH_PARAMETER)
    else:
        if REGEX:
            regex(0)
        else:
            normal(0)