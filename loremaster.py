import os.path as path
import urllib2
import re
import time
from datetime import datetime

import praw
from requests.exceptions import HTTPError

def modification_date(filename):
    t = path.getmtime(filename)
    return datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')

def Scrape():
    # Scrape source of a website that lists many subreddits
    # Build a list of all the subreddits, all_reddits
    # If necessary, remove duplicated listings so each subreddit is a unique entry
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

def FreshCheck(n):
    # Check a list of reddits for freshness (latest post < 1 week old)
    # Build/Update a list of fresh subreddits
    fresh_subreddits = []
    print "Checking",len(n),"subreddits for freshness. This may take some time...","\n"
    for x in n:
        try:
            target_subreddit = r.get_subreddit(x, fetch=True)
            avg_age = [] 
            for post in target_subreddit.get_new(limit=10):
                new_post = r.get_submission(submission_id = post.id)
                avg_age.append(new_post.created_utc)
            FreshPost(avg_age)
            if FreshPost(avg_age):
                fresh_subreddits.append(target_subreddit.display_name)
            else: 
                continue
        except HTTPError:
            print "!! ",x,"gave an error and was not checked !!"
        except praw.errors.InvalidSubreddit:
            print "!! ",x,"is not an existing subreddit and was not checked !!"
        except praw.errors.RedirectException:
            print "!! ",x,"tried to redirect. Probably not a subreddit link !!" 
            continue
    print "\n","All subreddits checked for freshness.","\n"
    print "Creating new list with",len(fresh_subreddits),"fresh subreddits..."
    with open('gaming.txt','w') as create:
        create.write("\n".join(fresh_subreddits))
    return fresh_subreddits;
 
def FreshPost(i):
    t = time.time()
    avg = sum(i) / float(len(i))
    diff = t - avg
    if diff < 604800:
        return True;

def KeywordCheck(n):
    # Check all the fresh subreddits for keywords
    loop_count = 0
    already_done = [] 
    my_keywords = open("tags.txt").read().split("\n")
    start_time = str(datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

    print "\n","Checking",len(n),"fresh subreddits for keywords...","\n"
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



# Define a unique user_agent for reddit API and login
r = praw.Reddit(user_agent='PRAW tester_Python learner/0.2 by u/JohnnyNoNumber')
'''
print "\n","Logging into Reddit...","\n"
r.login(username='JohnnyNoNumber', password='toasters8')

if r.is_logged_in() is True:
    print "Logged in.","\n"
'''

# Check if a file of fresh subreddits was already created
print "Checking for previously fresh subreddits..."
try:
    f = open("gaming.txt").readlines()
    # If there is a file, check if it has entries
    # If it has entries, pass the contents to Freshcheck(), and pass that output into KeywordCheck()
    if f:
        print "A list is available!","\n"
        d = modification_date('gaming.txt')
        print "List last modified:",d
        gaming = open("gaming.txt").read().split("\n")
        FreshCheck(gaming);
        #KeywordCheck(FreshCheck(gaming));
    # If the file is empty...
    else:
        print "File found, but it has no entries. Getting new list..."
# If there is no file...
except IOError:
    print "No file found - Getting new list..."

# Pass Scrape() output into FreshCheck(), and pass that output into KeywordCheck()
KeywordCheck(FreshCheck(Scrape()));