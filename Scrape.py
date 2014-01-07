import urllib2
import re

def Scrape():
    '''
    Scrape source of a website that lists many subreddits and return a
    list of subreddits, with no duplicate entries.
    '''
    all_reddits = []
    print "\n","Scraping http://www.reddit.com/r/gaming/wiki/faq for gaming reddits..."
    url = 'http://www.reddit.com/r/gaming/wiki/faq'
    source = urllib2.urlopen(url).read()
    find_group = re.compile('<a href="/r/(.+?)"')
    subfound = find_group.findall(source)
    for subreddit in subfound:
        if subreddit not in all_reddits:
            all_reddits.append(subreddit)
    print "Scraping done!","\n"
    return all_reddits;
