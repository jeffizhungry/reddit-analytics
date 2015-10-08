#!/usr/bin/python3.4
from bs4 import BeautifulSoup
import requests
import sys

def getPageContent(url):
    url="https://www.reddit.com/r/askreddit/"
    user_agent = {'User-agent': 'Mozilla/5.0'}
    page = requests.get(url, headers = user_agent)
    return page.content

if __name__ == "__main__":
#     page_content = getPageContent('blah')
#     with open('content.html', 'a+') as f:
#         f.write(str(page_content))
#
    with open('content.html', 'r') as f:
        text = f.read()
        soup = BeautifulSoup(text)
        print("")
        print(type(soup))
        res = soup.header
        print("")
        print(type(res))
        print(res)
        print("")
        print(type(res.contents))
        print(len(res.contents))
        print(res.contents)
        for c in res.contents:
            print("")
            print(c)
            print(c.string)
        print("")
        print(type(res.contents[0]))
        print(res.contents[0])
#         print("")
#         print(type(res.contents[0]('h1', {'class':'subscribe-callout')))
#         print(res.contents[0]('h1', {'class':'subscribe-callout'))

