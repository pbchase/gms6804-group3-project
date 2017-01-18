#!/usr/local/bin/python

from bs4 import BeautifulSoup
import pycurl
import os.path

def download(url='', name=''):
	with open(name, 'wb') as f:
	    c = pycurl.Curl()
	    c.setopt(c.FOLLOWLOCATION, True)
	    c.setopt(c.URL, url)
	    c.setopt(c.WRITEDATA, f)
	    c.perform()
	    c.close()

limit = 20
soup = BeautifulSoup(open("23andmeHtmlOnly.htm"), "lxml")

#print soup.find('td',attr={'data-summarize-as':"participant"})

filenames = {}
urls = {}
for row in soup.findAll('tr'):
    aux = row.findAll('td')
    if len(aux) > 0:
    	subject = aux[1].a.contents[0]
    	filenames[subject] = subject
    	url = 'https://my.pgp-hms.org' + aux[6].find('a').get('href')
    	urls[subject] = url

print "Subject count: " + str(len(urls))

# download only limit files
download_count=0
for subject in filenames.keys():
	if download_count >= limit:
		break
	myfilename = os.path.join('23andmedata/raw/', filenames[subject])
	if (not os.path.isfile(myfilename)):
		print "Downloading " + urls[subject] + \
			" to " + myfilename
		download(urls[subject], myfilename)
		download_count += 1
	else:
		print "Skipping download of " + myfilename
