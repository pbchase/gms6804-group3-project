#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import pycurl
import os.path


def download(url='', name=''):
    """
    :param url: a URL to read
    :param name: the output file name into which content should be written
    :return: none
    """
    with open(name, 'wb') as f:
        c = pycurl.Curl()
        c.setopt(c.FOLLOWLOCATION, True)
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()


def extract_23andme_data(soup, website_root):
    """
    Scrap a pgp-hms genomics web page of 23andMe data for the URLs to download
    :param soup: the object representing the web page we are scraping
    :param website_root: a protocol and hostname that will be prepended to each URL
    :return file_names, urls: a tuple of dictionaries providing URLS to download
            and the desired local name for each file downloaded
    """
    file_names = {}
    urls = {}

    for row in soup.findAll('tr'):
        # find each table cell in this row
        aux = row.findAll('td')
        if len(aux) > 0:
            subject = aux[1].a.contents[0]
            file_names[subject] = subject
            url = website_root + aux[6].find('a').get('href')
            urls[subject] = url
    return urls, file_names


def download_files(urls, download_directory, file_names, limit):
    """
    :param urls: a dict of the urls to download keyed on the subject to which they apply
    :param download_directory: the local directory into which files should be written
    :param file_names: A dict of the desired local file names keyed on the subject to which they apply
    :param limit: the maximum number of files we should download in this session
    :return:
    """
    download_count = 0
    for subject in list(file_names.keys()):
        if download_count >= limit:
            break
        my_filename = os.path.join(download_directory, file_names[subject])
        if not os.path.isfile(my_filename):
            print("Downloading " + urls[subject] + \
                " to " + my_filename)
            download(urls[subject], my_filename)
            download_count += 1
        else:
            print("Skipping download of " + my_filename)


# prepend this portion of a URL to every URL we read from the file
website_root = 'https://my.pgp-hms.org'

# Download the 23andMe files
soup = BeautifulSoup(open("23andmeHtmlOnly.htm"), "lxml")
download_directory = '23andmedata/raw/'
urls, file_names = extract_23andme_data(soup, website_root)
print("Subject count: " + str(len(urls)))
limit = 705  # only download this many files
download_files(urls, download_directory, file_names, limit)
# for filename in urls.keys():
#     print "%s,download_name,%s" % (filename, urls[filename])
