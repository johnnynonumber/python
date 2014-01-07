import os.path as path
import time
import re
from datetime import datetime

import praw
from requests.exceptions import HTTPError

def ModDate(filename):
    t = time.time()
    m = path.getmtime(filename)
    diff = ((t - m) / 60) / 60
    return '%.1f' % diff
    #return datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')

def KeywordCheck(n):
    # Check all the fresh subreddits for keywords
    start_time = str(datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))    
    loop_count = 0
    already_done = []
    of_interest = [] 
    my_keywords = open("tags.txt").read().split("\n")

    print "\n","Checking",len(n),"fresh subreddits for keywords...","\n"
    while True:
        for fresh_subreddit in n:
            print "Checking r/",fresh_subreddit
            fresh_subreddit = r.get_subreddit(fresh_subreddit)
            for post in fresh_subreddit.get_hot(limit=10):
                #op_title = post.title
                has_my_keywords = any(string in post.title for string in my_keywords)
                if post.id not in already_done and has_my_keywords:
                    already_done.append(post.id)
                    of_interest.append((fresh_subreddit.display_name, post.short_link))
        
        print "Sending",len(of_interest),"posts of interest.","\n"
        msg = 'Posts of Interest - (%s)' % (of_interest)
        r.user.send_message('JohnnyNoNumber', msg)

        loop_count += 1
        print "Checks done since",start_time,"UTC:",loop_count
        print "Waiting 30 minutes before next check.","\n"
        time.sleep(1800)







# Define a unique user_agent for reddit API and login
r = praw.Reddit(user_agent='PRAW tester_Python learner/0.3 by u/JohnnyNoNumber')

print "\n","PRAW tester_Python learner/0.4 by u/JohnnyNoNumber","\n","Logging into Reddit...","\n"

try:
    r.login(username='JohnnyNoNumber', password='toasters8')
    if r.is_logged_in() is True:
        print "Logged in!","\n"       
    else:
        print "Something broke!"
except:
    pass

# Check if a file of fresh subreddits was already created
print "Checking for previously fresh subreddits..."
try:
    f = open("gaming.txt").readlines()
    # If it has entries, check when it was last modified.
    # This will tell us when FreshCheck() was last run on the list.
    # FreshCheck() takes a long time to run on large lists!
    if f:
        print "A list is available!","\n"
        d = ModDate('gaming.txt')
        print "List last modified:",d,"hours ago."
        gaming = open("gaming.txt").read().split("\n")
        KeywordCheck(gaming);
    # If the file is empty...
    # else:
        # Do some other thing
        # print "File found, but it has no entries. Getting new list..."
# If there is no file...
except IOError:
    print "No file found - Error:",IOError,"\n"