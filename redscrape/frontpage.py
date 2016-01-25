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

def get_articles(url):
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

    reddit_page = _get_page_content(url)

    articles = []
    soup = BeautifulSoup(reddit_page, "html.parser")

    # Find table of articles in HTML
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

            # Get author and timestamp
            tagline_elem = art.find_all('p', {'class', 'tagline'})
            author = tagline_elem[0].a.string
            timestamp = dateutil.parser.parse(tagline_elem[0].time['datetime'])

            # Resolve full URL for internal reddit links
            if re.match('^(/r/)', link) is not None:
                link = "https://www.reddit.com" + link

            articles.append({"title":          title,
                             "link":           link,
                             "comments_link":  comments,
                             "author":         author,
                             "timestamp":      int(timestamp.strftime("%s")),})
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
