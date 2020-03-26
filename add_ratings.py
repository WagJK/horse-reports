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
filename_rating = sys.argv[1]
filename_others = sys.argv[2]

file_rating = open(filename_rating)
file_others = open(filename_others)

reader_rating = csv.reader(file_rating, delimiter='\t', quotechar='|')
reader_others = csv.reader(file_others, delimiter='\t', quotechar='|')

min, max = 1, 2147483647
table_rating, table_others = [], []

cnt = -1
for row in reader_rating:
    cnt += 1
    if cnt == 0: continue
    if cnt < min or cnt > max: continue
    table_rating.append(row)

cnt = -1
for row in reader_others:
    cnt += 1
    if cnt == 0: continue
    if cnt < min or cnt > max: continue
    table_others.append(row)

cnt_x, cnt_y = 0, 0
for cnt_y in range(len(table_others)):
    while table_rating[cnt_x][9] != table_others[cnt_y][9]:
        cnt_x += 1
    table_others[cnt_y][24] = table_rating[cnt_x][24]
    table_others[cnt_y][25] = table_rating[cnt_x][25]
    util.write_table_append([table_others[cnt_y]], "output/Data Base (2018-2019) new.csv")