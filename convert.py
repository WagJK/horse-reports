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

# read csv
filename = sys.argv[1]
table_main = []
with open(filename) as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    cnt = -1
    min, max = 1, 2147483647
    for row in spamreader:
        cnt += 1
        if cnt == 0: continue
        if cnt < min or cnt > max: continue
        place = row[24]
        track = row[6]

        combined = ""
        if place == "沙田":
            combined += "田"
        else:
            combined += "谷"

        if track[0] == "草":
            combined += "草"
            combined += track.split("\"")[1]
        else:
            combined += "泥"

        row[6] = combined
        row = row[:24] + ["", ""] + row[25:]
        util.write_table_append([row], "output/Data Base (2018-2019) new.csv")