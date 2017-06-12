import requests
from bs4 import BeautifulSoup
import re

# sitemap = 'https://www.sharecare.com/sitemap.xml'
# sitemap = "https://www.sharecare.com/sitemap-doctor-3.xml"
# sitemap = "https://www.sharecare.com/sitemap-question-2.xml"
sitemap = "https://www.sharecare.com/sitemap-staticPage-0.xml"
r = requests.get(sitemap)
html = r.content
soup = BeautifulSoup(html, 'html.parser')
# links = soup.findAll(re.compile('^ns2:loc'))
links = soup.findAll(re.compile('^loc'))
urls = []

#Strip text from links and append to the URL list
for item in links:
    urls.append(item.get_text())
    # urls.append(x)
# print urls

# def striphtml(data):
#     for x in range(data):
#     p = re.compile(r'<.*?>')
#     x = p.sub('', str(data))
#     return x
#     z = x.split(",")
#     return z

# urls = [link.get('href') for link in links
#         if link.get('href') and link.get('href')[0:4]=='http']

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
f = open('/Users/will.bryant/Desktop/python/Automation/test.csv', "w")
print('\n==========\n301\'s')
i = 0
for result in results:
    if len(result[1]):
        i += 1
        # print(i, end='. ')
        print i
        for response in result[1]:
            # print('>>', response.url, end='\n\t')
            f.write(str(response.url)+"\n")
            print('>>', response.url)
        f.write(str(result[3])+"\n")
        print('>>>>',result[3])

        ## Python will convert \n to os.linesep
#
# #non-200s
print('\n==========\nERRORS')
for result in results:
    # if result[0] != 200 and result[0] !=0:
    if result[0] != 200:
        f.write(str(result[0])+ "\n" + str(result[2] + "\n\t")) #Give your csv text here.
        print(result[0], '-', result[2])
f.close
