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

        row = row[:26] + [""] + row[26:]

        util.write_table_append([row], "output/Data Base (2018-2019) new.csv")