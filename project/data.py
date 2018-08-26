import requests
import pprint
import time
import math
from bs4 import BeautifulSoup
from urllib.request import urlopen

from util import *

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
    # filter valid rows
    table_results = list(filter(lambda x: len(x) > 5, table_results))
    for i, row in enumerate(table_results):
        if i == 0: continue
        # join the section positions into 1 slot
        table_results[i] = row[:9] + [' '.join(row[10:len(row)-2])] + row[len(row)-2:]
    # print_table(table_results)
    
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
    # print_table(table_awards)
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
    
    # input and process racecard
    table_racecard = make_list(tables[8])
    # print_table(table_racecard)
    return table_racecard


def combine_tables(table_results, table_awards, table_racecard):
    table = table_results
    # combine hot info
    sort_arr = []
    for row in table:
        if is_float(row[-1]):
            sort_arr.append(float(row[-1]))
    list.sort(sort_arr)
    for i, row in enumerate(table):
        if i == 0: table[i].append("熱門")
        else:
            if is_float(row[-1]):
                if math.isclose(float(row[-1]), sort_arr[0], rel_tol=1e-9): # 1st hot
                    table[i].append("1st Hot")
                elif math.isclose(float(row[-1]), sort_arr[1], rel_tol=1e-9): # 2nd hot
                    table[i].append("2nd Hot")
                else: table[i].append("-")
            else: table[i].append("-")
    
    # TODO: combine bet info
    for i, row in enumerate(table):
        if i == 0: table[i].append("投注")
        else:
            # append bet for this row
            table[i].append("?")
    
    # combine racecard info
    for i, row in enumerate(table):
        if i == 0:
            table[i].append("優先參賽次序")
            table[i].append("配備")
        else:
            if row[1] != '':
                horse_number = int(row[1])
                table[i].append(table_racecard[horse_number][-6]) # 優先參賽次序
                table[i].append(table_racecard[horse_number][-5]) # 配備
            else:
                table[i].append('-')
                table[i].append('-')

    # combine odds
    for i, row in enumerate(table):
        if i == 0:
            table[i].append("P賠率")
            table[i].append("P賠率2")
            table[i].append("P賠率3")
            table[i].append("Queue賠率")
            table[i].append("PQ賠率")
            table[i].append("PQ賠率2")
            table[i].append("PQ賠率3")
        else:
            # P1/2/3
            for j in range(2, 5):
                if table_awards[j][1] == table[i][1]:
                    table[i].append(table_awards[j][2])
                else: table[i].append('')
            # Queue & PQ1/2/3
            for j in range(5, 9):
                horse_number = table_awards[j][1].split(',')
                if horse_number[0] == table[i][1] or horse_number[1] == table[i][1]:
                    table[i].append(table_awards[j][2])
                else: table[i].append('')

    return table