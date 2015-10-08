#!/usr/bin/python3.4
from bs4 import BeautifulSoup
import requests
import sys

def getPageContent(url):
    # Reddit uses user-agent id as a rudimentary bot checking mech.
    user_agent = {'User-agent': 'Mozilla/5.0'}
    page = requests.get(url, headers = user_agent)
    return page.content

if __name__ == "__main__":
#     url="https://www.reddit.com/r/askreddit/"
#     page_content = getPageContent(url)
#     with open('content.html', 'a+') as f:
#         f.write(str(page_content))
#
    with open('content.html', 'r') as f:
        text = f.read()
        soup = BeautifulSoup(text)
        print("--- SOUP --- ")
        table = soup.find('div', {'id':'siteTable'})
        count = 0
        for art in table:
            res = art.find_all('p', {'class', 'title'})
            if len(res) == 1:
                count += 1
                print(res[0])
                print("")
        print("num results found: ", count)
#             res = art.find('div', {'class':'title'})
#             print(type(res))
#             res = art.find('p', {'class':'title'})
#             print(type(res))
#             print(res.prettify())
#         print("--- SOUP HEADER ---")
#         res = soup.header
#         print(type(res))
#         print(res.prettify())
#         print("--- SOUP FIND ALL ---")
#         res = soup.findAll('h1', {'class':'hover redditname'})
#         print(type(res))
#         print(len(res))
#         print(res)
#         res = soup.findAll('h2', {'class':'result-message'})
#         print(type(res))
#         print(len(res))
#         print(res)
#         res = soup.findAll('div', {'class':'subscribe-thanks'})
#         print(type(res))
#         print(len(res))
#         print(res)
#         print("--- SOUP HEADER FIND ALL ---")
#         res = soup.header.findAll('h1', {'class':'subscribe-callout'})
#         print(type(res))
#         print(len(res))
#         print(res)
#         res = soup.header.findAll('h2', {'class':'result-message'})
#         print(type(res))
#         print(len(res))
#         print(res)
#         res = soup.header.findAll('div', {'class':'subscribe-thanks'})
#         print(type(res))
#         print(len(res))
#         print(res)
#         print("--- SOUP HEADER FIND_ALL ---")
#         res = soup.header.find_all('h1', {'class':'subscribe-callout'})
#         print(type(res))
#         print(len(res))
#         print(res)
#         res = soup.header.find_all('h2', {'class':'result-message'})
#         print(type(res))
#         print(len(res))
#         print(res)
#         res = soup.header.find_all('div', {'class':'subscribe-thanks'})
#         print(type(res))
#         print(len(res))
#         print(res)
