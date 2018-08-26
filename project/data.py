import requests
import pprint
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen

from util import print_table
from util import make_list

index_awards_min = 13

pp = pprint.PrettyPrinter()


def data_input_results(url):
    # get response from url
    response = urlopen(url, timeout=10)
    while response.getcode() != 200:
        print("* retry connecting " + url)
        response = urlopen(url, timeout=10)

    # make beautiful soup object
    soup = BeautifulSoup(response, 'lxml')
    tables = soup.find_all('table')
    
    # input and process results
    table_results = make_list(tables[4])
    table_results = list(filter(lambda x: len(x) > 5, table_results))
    for i, row in enumerate(table_results):
        if i == 0: continue
        table_results[i] = row[:9] + [','.join(row[10:15])] + row[15:]
    print_table(table_results)
    
    # input and process award rates
    index = index_awards_min
    table_awards = make_list(tables[20])[1:]
    # try out the index of the awards table
    while len(table_awards) == 0 or len(table_awards[0]) == 0 or table_awards[0][0] != "彩池":
        index = index + 1
        table_awards = make_list(tables[index])[1:]
    for i, row in enumerate(table_awards):
        if i == 0: continue
        if len(row) < 3: table_awards[i] = [''] + row
    print_table(table_awards)
    return table_results, table_awards


def data_input_racecard(url):
    # get response from url
    response = urlopen(url, timeout=10)
    while response.getcode() != 200:
        print("* retry connecting " + url)
        response = urlopen(url, timeout=10)

    # make beautiful soup object
    soup = BeautifulSoup(response, 'lxml')
    tables = soup.find_all('table')
    
    # input and process racecards
    table_racecards = make_list(tables[8])
    print_table(table_racecards)
    return table_racecards





