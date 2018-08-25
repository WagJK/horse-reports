import pandas as pd
import requests
import pprint
from bs4 import BeautifulSoup
from urllib.request import urlopen

pp = pprint.PrettyPrinter()

def pprint(table):
    for row in table: print(row)


def make_list(table):
    result = []
    allrows = table.findAll('tr')
    for row in allrows:
        result.append([])
        allcols = row.findAll('td')
        for col in allcols:
            thestrings = [str(s).strip('\r\n ') for s in col.findAll(text=True)]
            thetext = ''.join(thestrings)
            result[-1].append(thetext)
    return result


def data_input(url):
    response = urlopen(url)
    soup = BeautifulSoup(response, 'lxml')
    table = make_list(soup.find_all('table')[4])
    table = list(filter(lambda x: len(x) > 5, table))
    pprint(table)
    

data_input('http://racing.hkjc.com/racing/info/meeting/Results/chinese/')
