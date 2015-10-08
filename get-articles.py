#!/usr/bin/python3.4
from bs4 import BeautifulSoup
from collections import namedtuple
import requests
import sys

Article = namedtuple('Article', ['title', 'link', 'comments_link'])

def getPageContent(url):
    # Reddit uses user-agent id as a rudimentary bot checking mech.
    user_agent = {'User-agent': 'Mozilla/5.0'}
    page = requests.get(url, headers = user_agent)
    return page.content

def getArticles(reddit_page):
    articles = []

    soup = BeautifulSoup(reddit_page)

    # Find Articles Table
    table = soup.find('div', {'id':'siteTable'})
    for art in table:
        # Only get articles that have a rank assoc with them
        # "real" articles
        res = art.find('span', {'class':'rank'})
        if res is not None and res.string is not None:
            res1 = art.find_all('p', {'class', 'title'})
            res2 = art.find_all('a', {'class', 'comments'})
            title = res1[0].a.string
            link = res1[0].a['href']
            comments_link = res2[0]['href']
            articles.append(Article(title=title, link=link, comments_link=comments_link))

    return articles


if __name__ == "__main__":
    url="https://www.reddit.com/r/showerthoughts/?count=25"
    page_content = getPageContent(url)
    articles = getArticles(page_content)

#     with open('content.html', 'r') as f:
#         text = f.read()
#         articles = getArticles(text)

    print("Number of articles found: ", len(articles))
    for a in articles:
        print("title:    ", a.title)
        print("link:     ", a.link)
        print("comments: ", a.comments_link)
        print("")
