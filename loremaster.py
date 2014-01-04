import praw, time

r = praw.Reddit(user_agent='u/JohnnyNoNumber testing PRAW')

print "\n","Logging into Reddit...","\n"
r.login(username='johnnynonumber',password='toasters8')

if r.is_logged_in() is True:
        print "Yay! We logged in.","\n"
else:
        print "Nooooo!"

already_done = []        
my_keywords = ['Blizzard', 'blizzard', 'Blizzard Entertainment', 'blizzard entertainment']
subreddit_list = open("subreddit_list.txt").read().split("\n")

while True:                
        for i in subreddit_list:
                target_subreddit = r.get_subreddit(i)
                for post in target_subreddit.get_hot(limit=10):
                        op_text = post.selftext.lower()
                        has_my_keywords = any(string in op_text for string in my_keywords)
                        if post.id not in already_done and has_my_keywords:
                                already_done.append(post.id)
                                msg = '[NoNumber Bot] Post of Interest(%s)' % post.short_link
                                r.user.send_message('JohnnyNoNumber', msg)
                                print "Found a post in",i

        print "Waiting 2 minutes.","\n\n"
        time.sleep(120)
