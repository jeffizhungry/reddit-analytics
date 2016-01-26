#!/usr/bin/env python34
from bs4 import BeautifulSoup
from datetime import datetime
import dateutil.parser
import json
import requests
import re
import sys

def _get_page_content(url):
    """ Gets a subreddit front page. """

    # Reddit uses user-agent id as a rudimentary bot checking mech.
    # BEWARE, THERE COULD ME MORE!
    user_agent = {'User-agent': 'Mozilla/5.0'}
    page = requests.get(url, headers = user_agent)
    return page.content

def _parse_article(bs4_tag):

    # Get title and link
    title_elem = bs4_tag.find('p', {'class', 'title'})
    title = title_elem.a.string
    link = title_elem.a["href"]

    # Resolve full URL for internal reddit links
    if re.match('^(/r/)', link) is not None:
        link = "https://www.reddit.com" + link

    # Get Comments Link
    comm_link = bs4_tag.find('a', {'class', 'comments'})["href"]

    # Get author and timestamp
    tagline_elem = bs4_tag.find('p', {'class', 'tagline'})
    author = tagline_elem.a.string
    timestamp = dateutil.parser.parse(tagline_elem.time['datetime'])

    return {"title":          title,
            "link":           link,
            "comments_link":  comm_link,
            "author":         author,
            "timestamp":      int(timestamp.strftime("%s")),}

def get_articles(subreddit_url):
    """
    Parses subreddit page HTML for article information.

    Returns an array of JSON objects in the form.
    {
        "title":            title,
        "link":             link,
        "comments_link":    comments,
        "author":           author,
        "timestamp":        int(timestamp.strftime("%s"))
    }
    """
    reddit_page = _get_page_content(subreddit_url)

    soup = BeautifulSoup(reddit_page, "html.parser")

    articles = []

    # Find table of articles in HTML
    table = soup.find('div', {'id':'siteTable'})
    for art in table:
        if "thing" in art["class"]:
            articles.append(_parse_article(art))

    return articles

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Improper number of arguemnts")
        print("USAGE: python3.4 {} <subreddit>".format(sys.argv[0]))
        sys.exit(1)

    url="https://www.reddit.com/r/{}".format(sys.argv[1])
    articles = get_articles(url)
    print(json.dumps(articles, sort_keys=True,
                     indent=4, separators=(',', ': ')))
    print("Number of articles found: ", len(articles))
