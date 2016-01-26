#!/usr/bin/env python34
from bs4 import BeautifulSoup
from datetime import datetime
import dateutil.parser
import json
import requests
import re
import sys

def _parse_comment(com):

    # Get Author
    author = bs4_tag.find('a', {'class', 'author'}).string

    # Get Comment Text
    text = bs4_tag.find('div', {'class', 'md'}).p.string

    # Get Timestamp
    raw_ts = bs4_tag.find_all('time', {'class', 'live-timestamp'})[0]["datetime"]
    ts = dateutil.parser.parse(raw_ts)

    # Get Comment ID
    comm_id = bs4_tag.p.a["name"]

    # Get Children
    children = []
    children_elem = bs4_tag.find_all('div', {'id':'siteTable_t1_{}'.format(comm_id)})
    if len(children_elem) > 0:
        for rc in children_elem[0]:
            if "comment" in rc["class"]:
                children.append(_parse_comment(rc))

    return {
        "id":           comm_id,
        "author":       author,
        "text":         text,
        "timestamp":    int(ts.strftime("%s")),
        "children":     children,
    }

def get_comments(url):
    """
    Parses comment's page HTML for comments.

    Returns an array of JSON objects in the form.
    {
        "id":           comment_id
        "author":       author,
        "timestamp":    int(timestamp.strftime("%s"))
        "comment":      "you like that you fucking retard?",
        "children":     [],
    }
    """

    # Reddit uses user-agent id as a rudimentary bot checking mech.
    # BEWARE, THERE COULD ME MORE!
    user_agent = {'User-agent': 'Mozilla/5.0'}
    reddit_page = requests.get(url, headers = user_agent).content
    soup = BeautifulSoup(reddit_page, "html.parser")

    # Extract comment page ID from link
    comm_page_id = re.search('^.*comments/([a-z0-9]*)/', url, re.IGNORECASE).group(1)
    if comm_page_id is None:
        return None

    comments = []

    # Find table of articles in HTML
    comm_elems = soup.find('div', {'id':'siteTable_t3_{}'.format(comm_page_id)})
    if len(comm_elems) > 0:
        for c in comm_elems:
            if "comment" in c["class"]:
                comments.append(_parse_comment(c))

    return comments

if __name__ == "__main__":
    url = "https://www.reddit.com/r/Showerthoughts/comments/42hs0g/when_its_snowing_in_america_the_whole_world_gets/"
    url = "https://www.reddit.com/r/Showerthoughts/comments/42nmgq/smoking_is_one_of_the_leading_causes_of_statistics/"
    articles = get_comments(url)

    print(json.dumps(articles, sort_keys=True,
                     indent=4, separators=(',', ': ')))
