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

def _parse_comment_entitiy(bs4_tag):
    pass

def _find_comment_section(html):
    pass

def get_comments(url):
    """
    Parses subreddit page HTML for article information.

    Returns an array of JSON objects in the form.
    {
        "author":       author,
        "timestamp":    int(timestamp.strftime("%s"))
        "comment":      "you like that you fucking retard?",
        "children":     [],
    }
    """

    reddit_page = _get_page_content(url)

    soup = BeautifulSoup(reddit_page, "html.parser")
    comment_page_id = re.search('^.*comments/([a-z0-9]*)/', url, re.IGNORECASE).group(1)

    # Find table of articles in HTML
    comments = []
    raw_comments = soup.find('div', {'id':'siteTable_t3_{}'.format(comment_page_id)})
    for com in raw_comments:
        if "comment" in com["class"]:
            comments.append(com)

    # Parse Comment Div
    for com in comments:

        # Get Author
        author = com.find_all('a', {'class', 'author'})[0].string

        # Get Comment Text
        text = com.find_all('div', {'class', 'md'})[0].p.string

        # Get Timestamp
        raw_ts = com.find_all('time', {'class', 'live-timestamp'})[0]["datetime"]
        ts = dateutil.parser.parse(raw_ts)
        print(ts)

        # dateutil.parser.parse(ext = com.find_all('div', {'class', 'md'})[0].p.string

    return None

if __name__ == "__main__":
    url = "https://www.reddit.com/r/Showerthoughts/comments/42hs0g/when_its_snowing_in_america_the_whole_world_gets/"
    articles = get_comments(url)

    print(json.dumps(articles, sort_keys=True,
                     indent=4, separators=(',', ': ')))

#     for art in table:
#
#         # Only get articles that have a rank assoc with them
#         # This eliminates sticky posts and sponsored posts
#         real_art = art.find('span', {'class':'rank'})
#         if real_art is not None and real_art.string is not None:
#
#             # Get article title and link
#             title_elem = art.find_all('p', {'class', 'title'})
#             title = title_elem[0].a.string
#             link = title_elem[0].a['href']
#
#             # Get comments link
#             comm_elem = art.find_all('a', {'class', 'comments'})
#             comments = comm_elem[0]['href']
#
#             # Get author and timestamp
#             tagline_elem = art.find_all('p', {'class', 'tagline'})
#             author = tagline_elem[0].a.string
#
#             # Resolve full URL for internal reddit links
#             if re.match('^(/r/)', link) is not None:
#                 link = "https://www.reddit.com" + link
#
#             articles.append({"title":          title,
#                              "link":           link,
#                              "comments_link":  comments,
#                              "author":         author,
#                              "timestamp":      int(timestamp.strftime("%s")),})

