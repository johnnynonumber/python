import urllib2, re, praw, time
'''
pagenumbers = range(1,9)
redditlist = []

print "\n","Scraping redditlist.com for top ranked subreddits, and saving to redditlist.txt...","\n"

for page in pagenumbers:
        url = 'http://www.redditlist.com/page-'+str(page)+''
        source = urllib2.urlopen(url).read()
        find_group = re.compile('">(.+?)</a></td>')
        subreddit_per_page = find_group.findall(source)
        for subreddit in subreddit_per_page:
                if subreddit not in redditlist:
                        redditlist.append(subreddit)
        print "Page",page,"done!" 

print "\n","Writing to file...","\n"        
with open("redditlist.txt", mode='wt') as myfile:
        myfile.write('\n'.join(redditlist))
        
print "All pages done!"
'''

r = praw.Reddit(user_agent='u/JohnnyNoNumber PRAW bot testing')

print "\n","Logging into Reddit...","\n"
r.login(username='johnnynonumber',password='toasters8')

if r.is_logged_in() is True:
        print "Yay! We logged in.","\n"
else:
        print "Nooooo!"

already_done = []        
my_keywords = ['Blizzard']
redditlist = open("redditlist.txt").read().split("\n")

while True:                
        for i in redditlist:
                subreddit = r.get_subreddit(i)
                print "Checking",subreddit,"\n"
                for post in subreddit.get_hot(limit=10):
                        op_text = post.selftext.lower()
                        has_my_keywords = any(string in op_text for string in my_keywords)
                        if post.id not in already_done and has_my_keywords:
                                already_done.append(post.id)
                                msg = '[NoNumber Bot] Post of Interest(%s)' % post.short_link
                                r.user.send_message('JohnnyNoNumber', msg)

        print "Waiting 2 minutes.","\n\n"
        time.sleep(120)
