import requests
from bs4 import BeautifulSoup
import random
import re


sitemap = 'https://www.sharecare.com/sitemap.xml'

r = requests.get(sitemap)
html = r.content
soup = BeautifulSoup(html, 'html.parser')
siteMapLinks = soup.findAll(re.compile('^ns2:loc'))
linksToChoose = []
for item in siteMapLinks:
    linksToChoose.append(item.get_text())

# print links
secure_random = random.SystemRandom()
newSitemap = (secure_random.choice(linksToChoose))
print newSitemap


r = requests.get(newSitemap)
html = r.content
soup = BeautifulSoup(html, 'html.parser')
links = soup.findAll(re.compile('^loc'))
urls = []

#Strip text from links and append to the URL list
for item in links:
    urls.append(item.get_text())
    # urls.append(x)
# print urls

results = []
for i, url in enumerate(urls,1):
    try:
        r = requests.get(url)
        report = str(r.status_code)
        # print report
        # print r.history
        if r.history:
            history_status_codes = [str(h.status_code) for h in r.history]
            report += ' [HISTORY: ' + ', '.join(history_status_codes) + ']'
            result = (r.status_code, r.history, url, 'No error. Redirect to ' + r.url)
        elif r.status_code == 200:
            result = (r.status_code, r.history, url, 'No error. No redirect.')
            print result
        else:
            result = (r.status_code, r.history, url, 'Error?')
    except Exception as e:
        result = (0, [], url, e)

    results.append(result)
#     # print results
# #Sort by status and then by history length
# results.sort(key=lambda result:(result[0],len(result[1])))
#
# #301s - may want to clean up 301s if you have multiple redirects
print('\n==========\n301\'s')
i = 0
for result in results:
    if len(result[1]):
        i += 1
        # print(i, end='. ')
        print i
        for response in result[1]:
            # print('>>', response.url, end='\n\t')
             print('>>', response.url)
        print('>>>>',result[3])
#
# #non-200s
print('\n==========\nERRORS')
for result in results:
    # if result[0] != 200 and result[0] !=0:
    if result[0] != 200:
        print(result[0], '-', result[2])
