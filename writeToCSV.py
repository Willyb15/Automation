import requests
from bs4 import BeautifulSoup
import re
import csv
import sys

import csv
data = "Hello suckit"


# with open(r'/Users/will.bryant/Desktop/python/Automation/test.csv') as pagetoWrite:
#     # reader = csv.reader(pagetoWrite)
#     # writer = csv.writer(pagetoWrite)
#     # for row in reader:
#     #     writer.writerow(data)
#         for line in text:
#             file.write(line)
#             file.write('\n')

f = open('/Users/will.bryant/Desktop/python/Automation/test.csv','w')
f.write(data) #Give your csv text here.
## Python will convert \n to os.linesep
f.close()

#
# with open('csvfile.csv','wb') as file:
#     for line in text:
#         file.write(line)
#         file.write('\n')

# with open(r'C:\Users\Mentos\Automated Reports\SEO - Page Speed Report - Daily\Inputs\Pages to Test.csv','r') as pageInputList, open(r'C:\Users\Mentos\Automated Reports\SEO - Page Speed Report - Daily\Raw Data\Page Speed Output.csv', 'a', newline='') as pageOutputList:
    # pages = csv.reader(pageInputList)
    # resultsPage = csv.writer(pageOutputList)
