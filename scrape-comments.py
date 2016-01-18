#!/usr/bin/env python3.4
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

VERBOSE = True      # Enable debug output
CLICK_DELAY = 0.5   # Add some delays between clicks to mimic human click
RETRY_COUNT = 1     # Retry on when page taking longer than usual to load
RETRY_SLEEP = 5.0   # Retry sleep and wait on long page load

def debug(*args):
    if VERBOSE:
        print(*args)

def expand_load_comments(browser):
    """ Expand nested reddit comments by clicking load comments. """

    # Load more comments might generate more new nested load comment links
    # So we need to recursively click all these links
    found_link = True
    curr_retry_count = RETRY_COUNT
    while found_link or curr_retry_count + 1 > 0:
        found_link = False
        morecomments = browser.find_elements_by_xpath('.//span[@class = "morecomments"]')
        debug("NUM OF ELEMS IN CLASS (morecomments): {}".format(len(morecomments)))
        for elem in morecomments:
            try:
                # Click loading more comments
                if elem.text.startswith("load more comments"):
                    found_link = True
                    curr_retry_count = RETRY_COUNT
                    debug("CLICKING: {}".format(elem.text))
                    elem.click()
                    sleep(CLICK_DELAY)

                # loading... button indicates we went to fast, sleep to slow down
                elif elem.text.startswith("loading..."):
                    sleep(2.0)
                    found_link = True
                    curr_retry_count = RETRY_COUNT
                    debug("CLICKING: {}".format(elem.text))
                    elem.click()
                    sleep(CLICK_DELAY)

            # Don't care about selenium exceptions, log and move on
            except WebDriverException as e:
                print("EXCEPTION ON CLICK CAUGHT: ", e)

        # Sometimes the page takes longer than usual to load, and no links are
        # available because the page hasn't loaded yet! So try again!
        if not found_link:
            debug("NO MORE LINKS FOUND, GIVE {} MORE CHANCE(S)".format(curr_retry_count))
            sleep(RETRY_SLEEP)
            curr_retry_count = curr_retry_count - 1

    return

def grab_continue_this_thread_links(browser):
    links = set([])

    # Continue this thread might generate more new nested continue this thread links
    found_link = True
    curr_retry_count = RETRY_COUNT
    while found_link or curr_retry_count + 1 > 0:
        found_link = False
        continue_elems = browser.find_elements_by_xpath('.//span[@class = "deepthread"]/a')
        debug("NUM OF ELEMS IN CLASS (deepthread): {}".format(len(continue_elems)))
        for elem in continue_elems:
            try:
                if elem.text.startswith("continue this thread"):
                    href = elem.get_attribute('href')
                    if href not in links:
                        found_link = True
                        links.add(href)
                        debug("FOUND CONTINUE THIS THREAD LINK: ", href)

            # Don't care about selenium exceptions, log and move on
            except WebDriverException as e:
                print("EXCEPTION ON CLICK CAUGHT: ", e)

        # Sometimes the page takes longer than usual to load, and no links are
        # available because the page hasn't loaded yet! So try again!
        if not found_link:
            debug("NO MORE LINKS FOUND, GIVE {} MORE CHANCE(S)".format(curr_retry_count))
            sleep(RETRY_SLEEP)
            curr_retry_count = curr_retry_count - 1

    return links

if __name__ == "__main__":
    url="https://www.reddit.com/r/Showerthoughts/comments/3ph5vg/the_usa_doesnt_have_a_name_for_their_country_they/"
    # url = 'https://www.reddit.com/r/AskReddit/comments/41gg03/whatever_you_were_doing_10_minutes_ago_is_the/'

    browser = webdriver.Firefox()
    browser.get(url)

    expand_load_comments(browser)
    grab_continue_this_thread_links(browser)

    # browser.quit()
