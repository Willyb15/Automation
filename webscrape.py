from bs4 import BeautifulSoup
# import urllib.request
from urllib2 import urlopen

sauce = urlopen('https://pythonprogramming.net/parsememcparseface/').read()

soup = BeautifulSoup(sauce, 'lxml')

# print soup
# print (soup.title)
# print soup.title.name
# print soup.title.text
# print soup.title.string

# print soup.p
# # print soup.findAll('p')
# for paragraph in soup.findAll('p'):
#     # print paragraph.string
#     print paragraph.text

# print soup.get_text

for url in soup.findAll('a'):
    print url.get('href')
