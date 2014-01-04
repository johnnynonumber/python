import praw, time

r = praw.Reddit(user_agent='u/JohnnyNoNumber testing PRAW')

print "\n","Logging into Reddit...","\n"
r.login(username='johnnynonumber',password='toasters8')

if r.is_logged_in() is True:
        print "Logged in.","\n"
else:
        print "Nooooo!"

already_done = []        
my_keywords = open("tags.txt").read().split("\n")
subreddit_list = open("subreddit_list.txt").read().split("\n")
loop_count = 0


while True:
    for subreddit in subreddit_list: 
        target_subreddit = r.get_subreddit(subreddit)
        for post in target_subreddit.get_hot(limit=10):
            op_text = post.selftext.lower()
            has_my_keywords = any(string in op_text for string in my_keywords)
            if post.id not in already_done and has_my_keywords:
                already_done.append(post.id)
                msg = '[NoNumber Bot] Post of Interest in r/%s (%s)' % (target_subreddit, post.short_link)
                r.user.send_message('JohnnyNoNumber', msg)
                print "Found a post in the subreddit:",subreddit

    print "Waiting 2 minutes.","\n\n"
    loop_count += 1
    #with open("redditlist.txt", mode='wt') as myfile:
    #myfile.write('\n'.join(redditlist))
    time.sleep(120)
    print "Checking subreddit_list"
