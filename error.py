import urllib2
import re
import time
from datetime import datetime

import praw
import requests
from requests.exceptions import HTTPError

r = praw.Reddit(user_agent='u/JohnnyNoNumber testing PRAW')

print "\n","Logging into Reddit...","\n"
r.login(username='johnnynonumber',password='toasters8')

if r.is_logged_in() is True:
        print "Logged in.","\n"

all_reddits = ['funny', 'barzillax']
fresh_subreddits = []

print "Checking for date of submission for most recent post in every subreddit..."
print "If the post was created in 2014, put that subreddit to a 'fresh' list."
print "This may take some time..."

for subreddit in all_reddits: 
    target_subreddit = r.get_subreddit(subreddit, fetch=True)
    if target_subreddit.status_code != 404:
        for post in target_subreddit.get_new(limit=1):
            newest_post = r.get_submission(submission_id = post.id)
            if newest_post.created_utc >= 1388534400:
                fresh_subreddits.append(target_subreddit.display_name)
