def FreshPost(i):
    t = time.time()
    avg = sum(i) / float(len(i))
    diff = t - avg
    if diff < 604800:
        return True;

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