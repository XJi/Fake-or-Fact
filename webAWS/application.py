# all the imports
import sys, os
import csv
import requests, logging
from HTMLParser import HTMLParser
from urlparse import urlparse
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

h = HTMLParser()
from settings import APP_STATIC
from finalModel import model

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.debug = True

def isInDictionary(d,url):
    list_sites = d.keys()
    #see if the hostname is found in the list provided by open sources
    if url.hostname in list_sites:
        return d[url.hostname]
    else:#loop through all keys and see if there may be a match with the given URL.
        for key in list_sites:
            if key in url.hostname:
                return d[key]
    return -1

def isDomainReputable(url):
    non_credible_news = {}
    credible_news = {}
    #open the list of non credible news sources
    with open(os.path.join(APP_STATIC, 'open_sources_list.csv'), 'r') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        #need to skip the first line of the site
        my_reader.next()
        for row in my_reader:
            non_credible_news[row[0]]=row[1]

    parsed_uri = urlparse(url)
    value = isInDictionary(non_credible_news,parsed_uri)
    if value is not -1:
        return value
    with open(os.path.join(APP_STATIC, 'credible.csv'), 'r') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        #need to skip the first line of the site
        my_reader.next()
        for row in my_reader:
            site = row[0]
            if site.startswith('"') and site.endswith('"'):
                site = site[1:-1]
            credible_news[site]="Credible"
    value = isInDictionary(credible_news,parsed_uri)

    if value is not -1:
        return value
    return "Site Not Found in our data list!"


def getNewsTitle(url):
    try:
        r = requests.get(url)
        if r.status_code == 200 and "Fatal error" not in r.text:
            html = r.text
            start = html.find('<title>') + 7  # Add length of <title> tag
            end = html.find('</title>', start)
            title = html[start:end]
            title = h.unescape(title)

            if " - " in title:
                title = title.rsplit(' - ', 1)[0] # remove last tail if title contains website name

    except requests.exceptions.ConnectionError:
        logging.error('failed to connect to: '+url)
    return title


@application.route('/', methods=['GET', 'POST'])
def show_contents():
    if request.method == 'POST':
        url = request.form['target_url']
        return redirect(url_for('show_contents', url=url))
    else:
        entries = []
        url = request.args.get('url')
        entries.append(url)
        if url is not None:
            title = getNewsTitle(url)
            entries.append(title)
            if(isDomainReputable(url) == "Site Not Found in our data list!"):
                mod = model(fakeFile=os.path.join(APP_STATIC, 'fake2.txt'), realFile=os.path.join(APP_STATIC, 'real2.txt'))
                if mod.query(title) == 1:
                    predict_result = "Real News"
                else:
                    predict_result = "Fake News"
                entries.append(predict_result)
            else:
                entries.append(isDomainReputable(url))
        return render_template('index.html', entries=entries)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()