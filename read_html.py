import sys, os
from HTMLParser import HTMLParser
import requests, logging

h = HTMLParser()

# create logger
logging.basicConfig(filename='fakenews.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

def getFakeNews(my_file):
    list_titles = []
    with open(my_file,'r') as fake_news:
        for url in fake_news:
            try:
                r = requests.get(url)
                if r.status_code == 200 and "Fatal error" not in r.text:
                    html = r.text
                    start = html.find('<title>') + 7  # Add length of <title> tag
                    end = html.find('</title>', start)
                    title = html[start:end]
                    title = h.unescape(title)
                    if "<head>" not in title:
                        list_titles.append(title)

            except requests.exceptions.ConnectionError:
                logging.error('failed to connect to: '+url)
    return list_titles


if __name__ == "__main__":
        f = sys.argv[1]
        headlines = getFakeNews('list_of_fake_news.txt')
        for obj in headlines:
            print obj