import bs4
from urllib.request import urlopen


def data_input(url):
    response = urlopen(url)
    soup = BeautifulSoup(response)
    for table in soup.find_all('table'):
        print(table)

data_input('http://racing.hkjc.com/racing/info/meeting/Results/chinese/')
