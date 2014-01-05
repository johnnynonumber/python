import urllib2
import re
import time
from datetime import datetime

import praw




r = praw.Reddit(user_agent='u/JohnnyNoNumber testing PRAW')



# Scrape source of a website that lists many subreddits
# Create a text file with all the subreddits listed
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
        print "Page",page,url,"done!" 
        
print "Scraping done!"
print "--------------------------"



# Login to reddit, and get the most recent post of every subreddit in all_reddits.txt
# If the post was made in 2014, consider that subreddit "fresh"
# Build a list of fresh subreddits, and save to a text file
print "\n","Logging into Reddit...","\n"
r.login(username='johnnynonumber',password='toasters8')

if r.is_logged_in() is True:
        print "Logged in.","\n"

fresh_subreddits = []

print "Checking for date of submission for most recent post in every subreddit..."
print "If the post was created in 2014, put that subreddit to a 'fresh' list."
print "This may take some time..."

for subreddit in all_reddits: 
    target_subreddit = r.get_subreddit(subreddit)
    for post in target_subreddit.get_new(limit=1):
        newest_post = r.get_submission(submission_id = post.id)
        if newest_post.created_utc >= 1388534400:
                fresh_subreddits.append(target_subreddit.display_name)



# Now check all the fresh subreddits for keywords
loop_count = 0
already_done = []
# core_list = open("fresh_subreddits.txt").read().split("\n")        
my_keywords = open("tags.txt").read().split("\n")
start_time = str(datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

while True:
    for fresh in fresh_subreddits:
        fresh_subreddit = r.get_subreddit(fresh)
        print "Checking",fresh_subreddit
        for post in fresh_subreddit.get_hot(limit=10):
            op_title = post.title
            has_my_keywords = any(string in op_title for string in my_keywords)
            if post.id not in already_done and has_my_keywords:
                already_done.append(post.id)
                #msg = '[NoNumber Bot] Post of Interest in r/%s (%s)' % (fresh_subreddit, post.short_link)
                #r.user.send_message('JohnnyNoNumber', msg)
                print "\n","Found a post in the subreddit:",fresh_subreddit,"\n"

    loop_count += 1
    print "\n","Checked",loop_count,"times since",start_time,"UTC"
    print "\n","Waiting 5 seconds before next check.","\n\n"
    time.sleep(5)
    print "Checking fresh_subreddits","\n"
