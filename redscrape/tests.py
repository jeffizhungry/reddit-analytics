import articles

def get_articles_legit_tests():
    test_failed = False
    legit_subreddits = ['videos', 'technology', 'askreddit', 'programming',
                        'science', 'Muse', 'nekoatsume']

    for s in legit_subreddits:
        url="https://www.reddit.com/r/{}".format(s)
        print("-- Scraping: {}".format(s))
        arts = articles.get_articles(url)
        if len(arts) != 25:
            test_failed = True
            print("TEST FAILED!")

    if test_failed:
        print("[FAIL] get_articles legit test")
    else:
        print("[PASS] get_articles fake test")

def get_articles_fake_tests():
    test_failed = False
    legit_subreddits = ['djwfojwi', '12312312', 'sdjfkla']
    for s in legit_subreddits:
        url="https://www.reddit.com/r/{}".format(s)
        print("Scraping: {}...".format(s))
        arts = articles.get_articles(url)
        if len(arts) != 0:
            test_failed = True
            print("TEST FAILED!")
    if test_failed:
        print("[FAIL] Fake subreddits test")
    else:
        print("[PASS] Fake subreddits test")

if __name__ == "__main__":
    get_articles_legit_tests()
    get_articles_fake_tests()
