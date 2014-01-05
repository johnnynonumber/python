import urllib2
import re
import time
from datetime import datetime

import praw
from requests.exceptions import HTTPError



def Scrape():
    # Scrape source of a website that lists many subreddits
    # Build a list of all the subreddits, all_reddits
    # If necessary, remove duplicated listings so each subreddit is a unique entry
    pagenumbers = range(1,2)
    all_reddits = []
    print "\n","Scraping redditlist.com for top 5000 subreddits..."
    for page in pagenumbers:
        url = 'http://www.redditlist.com/page-'+str(page)+''
        source = urllib2.urlopen(url).read()
        find_group = re.compile('">(.+?)</a></td>')
        subreddit_per_page = find_group.findall(source)
        for subreddit in subreddit_per_page:
            if subreddit not in all_reddits:
                all_reddits.append(subreddit)
    print "Scraping done!","\n"
    return all_reddits;

def FreshCheck(n):
    # Check a list of reddits for freshness (most recent post made in 2014)
    # Build/Update a list of fresh subreddits
    fresh_subreddits = []
    print "Checking",len(n),"subreddits for freshness. This may take some time...","\n"
    for subreddit in n:
        try: 
            print subreddit
            target_subreddit = r.get_subreddit(subreddit, fetch=True)
            for post in target_subreddit.get_new(limit=1):
                newest_post = r.get_submission(submission_id = post.id)
                if newest_post.created_utc >= 1388534400:
                    fresh_subreddits.append(target_subreddit.display_name)
        except HTTPError:
            print "!! ",subreddit,"gave an error and was not checked !!"
            continue
    print "\n","All subreddits checked for freshness.","\n"
    return fresh_subreddits;
    
def KeywordCheck(n):
    # Check all the fresh subreddits for keywords
    loop_count = 0
    already_done = [] 
    my_keywords = open("tags.txt").read().split("\n")
    start_time = str(datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

    print "\n","Checking",len(n),"fresh subreddits for keywords..."
    while True:
        for fresh in n:
            fresh_subreddit = r.get_subreddit(fresh)
            for post in fresh_subreddit.get_hot(limit=10):
                op_title = post.title
                has_my_keywords = any(string in op_title for string in my_keywords)
                if post.id not in already_done and has_my_keywords:
                    already_done.append(post.id)
                    #msg = '[NoNumber Bot] Post of Interest in r/%s (%s)' % (fresh_subreddit, post.short_link)
                    #r.user.send_message('JohnnyNoNumber', msg)
                    print "\n","Found a post in the subreddit:",fresh_subreddit,"\n"
        loop_count += 1
        print "Checks done since",start_time,"UTC:",loop_count
        print "Waiting 10 seconds before next check.","\n"
        time.sleep(10)



# Define a unique user_agent for reddit API
r = praw.Reddit(user_agent='PRAW tester/Python learner by u/JohnnyNoNumber')

# Login to reddit
print "\n","Logging into Reddit...","\n"
#while r.is_logged_in() is False:
for i in range(0,100):
    while True:
        try:
            r.login(username='johnnynonumber')   
            if r.is_logged_in() is True:
                print "Logged in!","\n"
            else:
        except praw.errors.InvalidUserPass:
            print "Wrong password."
        except HTTPError:
            print "Something went wrong."
        except:
            continue        
        break



# Check if a file of fresh subreddits was already created
print "Checking for previously fresh subreddits..."
try:
    f = open("master_fresh.txt").readlines()
    # If there is a file, check if it has entries
    # If it has entries, pass the contents to Freshcheck(), and pass that output into KeywordCheck()
    if f:
        print "A list is available!","\n"
        master_fresh = open("master_fresh.txt").read().split("\n")
        KeywordCheck(FreshCheck(master_fresh));
    # If the file is empty...
    else:
        print "File found, but it has no entries. Getting new list..."
# If there is no file...
except IOError:
    print "No file found - Getting new list..."

# Pass Scrape() output into FreshCheck(), and pass that output into KeywordCheck()
try:
    KeywordCheck(FreshCheck(Scrape()));
except HTTPConnectionPool:
    print "Possible network connection issues. Retrying..."

# Bot will run until KeyboardInterrupt or network error