import csv
import cPickle as pickle
from urlparse import urlparse
import sys
import whois

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
	with open('open_sources_list.csv','r') as csvfile:
		my_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		#need to skip the first line of the site
		my_reader.next()
		for row in my_reader:
			non_credible_news[row[0]]=row[1]

	parsed_uri = urlparse(url)
	value = isInDictionary(non_credible_news,parsed_uri)
	if value is not -1:
		return value	
	with open('credible.csv','r') as csvfile:
		my_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		#need to skip the first line of the site
		my_reader.next()
		for row in my_reader:
			site = row[0]
			if site.startswith('"') and site.endswith('"'):
			    site = site[1:-1]
			credible_news[site]="credible"
	value = isInDictionary(credible_news,parsed_uri)
	
	if value is not -1:
		return value
	return "Site Not Found in our data list!"

#returns a dictioanry of relevant whois information to help 
def getWhoisCreationDate(hostname):
	whois_d = {}
	w = whois.whois(hostname)
	creation_date = w['creation_date']
	#print creation_date
	#print hostname
	if hostname == 'independent.co.uk':
		yr = 1996
		return yr
	yr = 0	
	try:
		for obj in creation_date:
			if yr< obj.year:
				yr = obj.year
	except TypeError:
		yr = creation_date.year	
	return yr

def calcAvgCreationDateAge(list_domains):
	list_dates = []
	sum = 0
	for dom in list_domains:
		yr = getWhoisCreationDate(dom)
		print yr, dom
		sum+=yr
		list_dates.append(yr)
	return float(sum)/float(len(list_dates))	
#	pickle.dump(list_dates,'creation_dates.cp')
#	print list_dates

def getListOfNewsDomains(file_path):
	list_dom =[]
	with open(file_path,'r') as csvfile:
		my_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		#need to skip the first line of the site
		my_reader.next()
		for row in my_reader:
			site = row[0]
			if site.startswith('"') and site.endswith('"'):
			    site = site[1:-1]
			list_dom.append(site)
	return list_dom	



if __name__ == "__main__":
	if len(sys.argv)<2:
		url1 = "http://breitbart.com/big-government/2017/04/08/sen-mcconnell-supreme-court-vacancy-key-president-trumps-win/"
		url2 = "https://www.nytimes.com/2017/04/08/world/middleeast/us-strike-on-syria-brings-fleeting-hope-to-those-caught-in-brutal-conflict.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news"
		print "Beginning Domain Analysis... "
		print urlparse(url1).hostname + " is considered "+isDomainReputable(url1)
		print urlparse(url2).hostname + " is considered "+isDomainReputable(url2)
	else:
		url= sys.argv[1]
		news_hostname = urlparse(url).hostname 
		print news_hostname+ " is considered "+isDomainReputable(url)
		#print "News Domain was created on "+str( getWhoisInformation(news_hostname))
		list_credible_domains = getListOfNewsDomains('credible.csv')
		print('Avg Domain Creation Date of Credible News Sites is 1994.95 ')
		print(news_hostname+' was first registered on '+str(getWhoisCreationDate(news_hostname)))
