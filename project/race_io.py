import json
import pprint
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from util import make_list
from util import print_table

pp = pprint.PrettyPrinter()

index_results_min = 4
index_awards_min = 13


def get_betinfo(filename):
    bet = json.load(open(filename, 'r'))
    return bet


def get_raceinfo(url):
    # get response from url
    response = urlopen(url, timeout=10)
    while response.getcode() != 200:
        print("* retry connecting " + url)
        response = urlopen(url, timeout=10)
    soup = BeautifulSoup(response, 'lxml')
    info_left = soup.find('div', class_='info').find_all('div')[0]

    course = ' '.join(list(map(lambda x: x.get_text(), info_left.find_all('p')[1:-1])))
    place = info_left.find_all('p')[0].find('span').get_text()
    ddy_index = info_left.find('p', class_='f_ffChinese').get_text().replace(" ", "").split("\n")[1]
    return {
        'course': course,
        'place': place,
        'ddy_index': ddy_index
    }


def get_results(url):
    # get response from url
    response = urlopen(url, timeout=10)
    while response.getcode() != 200:
        print("* retry connecting " + url)
        response = urlopen(url, timeout=10)
    soup = BeautifulSoup(response, 'lxml')
    tables = soup.find_all('table')
    
    # get race info per race
    info_panel = tables[3]
    info = list(map(lambda x: x.get_text(), info_panel.find_all('td')[:6]))
    race_info = {
        'tag': info[0],
        'name': info[3],
        'cond': info[1] + ' ' + info[2],
        'track': info[4] + ' ' + info[5]
    }

    # input and process results
    index = index_results_min
    table_results = make_list(tables[4])
    # try out the index of the awards table
    while len(table_results) == 0 or len(table_results[0]) == 0 or table_results[0][0] != "名次":
        index = index + 1
        table_results = make_list(tables[index])
    # filter valid rows
    table_results = list(filter(lambda x: len(x) > 5, table_results))
    for i, row in enumerate(table_results):
        if i == 0:
            continue
        # join the section positions into 1 slot
        table_results[i] = row[:9] + [' '.join(row[10:len(row)-2])] + row[len(row)-2:]
    
    # input and process award rates
    index = index_awards_min
    table_awards = make_list(tables[20])[1:]
    # try out the index of the awards table
    while len(table_awards) == 0 or len(table_awards[0]) == 0 or table_awards[0][0] != "彩池":
        index = index + 1
        table_awards = make_list(tables[index])[1:]
    for i, row in enumerate(table_awards):
        if i == 0:
            continue
        if len(row) < 3:
            table_awards[i] = [''] + row

    return race_info, table_results, table_awards


def get_racecard(url):
    # get response from url
    response = urlopen(url, timeout=10)
    while response.getcode() != 200:
        print("* retry connecting " + url)
        response = urlopen(url, timeout=10)
    soup = BeautifulSoup(response, 'lxml')
    tables = soup.find_all('table')

    # input and process racecard
    table_racecard = make_list(tables[8])
    return table_racecard