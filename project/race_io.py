import json
import util
import pprint
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
from util import make_list
from util import print_table

pp = pprint.PrettyPrinter()

index_min = 2


def get_betinfo(filename):
    bet = json.load(open(filename, 'r'))
    return bet[0]


def get_raceinfo(url):
    # get response from url
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
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
    tables = []
    while len(tables) < index_min:
        # print(len(tables), end=' ')
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
    # print(len(tables))

    # get race info per race
    info_panel = tables[1]
    info = list(map(lambda x: x.get_text(), info_panel.find_all('td')))
    race_info = {
        'tag': info[6],
        'name': info[9],
        'cond': info[7] + ' ' + info[8],
        'track': info[10] + ' ' + info[11]
    }
    # -------------------------
    # input and process results
    # -------------------------
    index = index_min
    table_results = make_list(tables[index_min])
    # try out the index of the awards table
    while len(table_results) == 0 or len(table_results[0]) == 0 or table_results[0][0] != "名次":
        index = index + 1
        table_results = make_list(tables[index])
    # filter valid rows
    table_results = list(filter(lambda x: len(x) > 10, table_results))
    for i, row in enumerate(table_results):
        if i == 0: continue
        # join the section positions into 1 slot
        table_results[i] = row[:9] + [' '.join(row[10:len(row)-2])] + row[len(row)-2:]

    # -----------------------------
    # input and process award rates
    # -----------------------------
    index = index_min
    table_awards = make_list(tables[index_min])
    # try out the index of the awards table
    while len(table_awards) == 0 or len(table_awards[0]) == 0 or table_awards[0][0] != "派彩":
        index = index + 1
        table_awards = make_list(tables[index])
    # process the awards table
    table_awards = table_awards[1:]
    for i, row in reversed(list(enumerate(table_awards))):
        if i == 0: continue
        if util.is_even(len(row)):
            table_awards[i-1] += row
    table_awards = list(map(
        lambda x: [x[0], list(zip(x[1::2], x[2::2]))],
        list(filter(
            lambda x: not util.is_even(len(x)),
            table_awards
        ))
    ))
    # print_table(table_awards)
    return race_info, table_results, table_awards


def get_racecard(url):
    # get response from url
    tables = []
    while len(tables) < index_min:
        # print(len(tables), end=' ')
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
    # print(len(tables))

    # input and process racecard
    table_racecard = make_list(tables[8])
    return table_racecard
