import requests
from bs4 import BeautifulSoup


def trade_spider():
    # page = 1
    # while page < max_pages:
    #     url = "https://www.sharecare.com/topics" + str(page)
    url = "https://www.sharecare.com/topics"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for link in soup.findAll(match_class{'class', 'list__item'}):
        href = link.get('a' , 'shref')
        print href


trade_spider()
