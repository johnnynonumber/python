import praw, time

r = praw.Reddit(user_agent='u/JohnnyNoNumber testing PRAW')
'''
print "\n","Logging into Reddit...","\n"
r.login(username='johnnynonumber',password='toasters8')
if r.is_logged_in() is True:
	print "Yay! We logged in.","\n"
else:
	print "Nooooo!"

'''
already_done = []	
my_keywords = ['game', 'Blizzard Entertainment']

while True:	
	print "\n","I've started doing your things. Please wait.","\n"
	subreddit = r.get_subreddit('truegaming')
	print "Checking Truegaming.","\n"
	
	for post in subreddit.get_hot(limit=10):
		
		op_text = post.selftext.lower()
		has_mywords = any(string in op_text for string in my_keywords)
		
		if post.id not in already_done and has_mywords:
			#msg = '[NoNumber Bot] Post of Interest(%s)' % post.short_link
			#r.user.send_message('JohnnyNoNumber', msg)
			already_done.append(post.id)
			print op_text,"\n"
			
	print "Gonna wait for 2 minutes and check again for you.","\n"
	time.sleep(120)
	print "Checking again now!","\n"
