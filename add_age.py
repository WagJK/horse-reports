import csv
import sys
import json
import util
import pprint
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
from util import make_list
from util import print_table
import make_main

pp = pprint.PrettyPrinter()

INDEX_MIN = 2

link_horseinfo = "https://racing.hkjc.com/racing/information/chinese/Horse/HorseSearch.aspx?HorseName=&SearchType=BrandNumber&BrandNumber="

def get_age(url, horse_id):
    # get response from url
    tables = []
    while len(tables) < INDEX_MIN:
        # print(len(tables), end=' ')
        driver = webdriver.Chrome()
        driver.get(url + horse_id)
        time.sleep(3)
        # driver.implicitly_wait(3)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
        driver.quit()
    if (len(tables) <= 4):
        return "-"
    if make_list(tables[4])[0][0] != "出生地 / 馬齡":
        return "-"
    age = make_list(tables[4])[0][2].split("/")[1].lstrip(' ')
    # print(horse_id, age)
    return age

# read csv
filename = sys.argv[1]
table_main = []
with open(filename) as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    cnt = -1
    min, max = 0, 2147483647
    for row in spamreader:
        cnt += 1
        if cnt == 0: continue
        if cnt < min or cnt > max: continue
        horse_id = row[9].split('(')[1][:-1]
        if row[23] == "":
            row[23] = get_age(link_horseinfo, horse_id)
        util.write_table_append([row], "output/Data Base (2018-2019) new.csv")