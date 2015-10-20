#!/usr/bin/python3.4
from bs4 import BeautifulSoup
from datetime import datetime
import dateutil.parser
import json
import requests
import re
import sys

def getPageContent(url):
    # Reddit uses user-agent id as a rudimentary bot checking mech.
    user_agent = {'User-agent': 'Mozilla/5.0'}
    page = requests.get(url, headers = user_agent)
    return page.content

def getArticles(reddit_page):
    articles = []
    soup = BeautifulSoup(reddit_page)

    # Find Articles Table in HTML
    table = soup.find('div', {'id':'siteTable'})
    for art in table:

        # Only get articles that have a rank assoc with them
        # This eliminates sticky posts and sponsored posts
        real_art = art.find('span', {'class':'rank'})
        if real_art is not None and real_art.string is not None:

            # Get article title and link
            title_elem = art.find_all('p', {'class', 'title'})
            title = title_elem[0].a.string
            link = title_elem[0].a['href']

            # Get comments link
            comm_elem = art.find_all('a', {'class', 'comments'})
            comments = comm_elem[0]['href']

            # Get author and timestamp under tagline div
            tagline_elem = art.find_all('p', {'class', 'tagline'})
            author = tagline_elem[0].a.string
            timestamp = dateutil.parser.parse(tagline_elem[0].time['datetime'])

            # Resolve full URL for reddit links
            if re.match('^(/r/)', link) is not None:
                link = "https://www.reddit.com" + link

            articles.append({"title":     title,
                             "link":      link,
                             "comments":  comments,
                             "author":    author,
                             "timestamp": int(timestamp.strftime("%s")),})


    return articles


if __name__ == "__main__":
    url="https://www.reddit.com/r/AskReddit"
    page_content = getPageContent(url)
    articles = getArticles(page_content)

#     with open('content.html', 'r') as f:
#         text = f.read()
#         articles = getArticles(text)

    print("Number of articles found: ", len(articles))
    print(json.dumps(articles, sort_keys=True,
                     indent=4, separators=(',', ': ')))
