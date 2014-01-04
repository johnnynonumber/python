import urllib2, re

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

for page in pagenumbers:
        url_NSFW = 'http://www.redditlist.com/nsfw/page-'+str(page)+''
        source_NSFW = urllib2.urlopen(url_NSFW).read()
        find_group_NSFW = re.compile('">(.+?)</a></td>')
        subreddit_per_page_NSFW = find_group_NSFW.findall(source_NSFW)
        for subreddit_NSFW in subreddit_per_page_NSFW:
                if subreddit_NSFW not in redditlist:
                        redditlist.append(subreddit_NSFW)
        print "NSFW Page",page,"done!" 

print "\n","Writing to file...","\n"        
with open("redditlist.txt", mode='wt') as myfile:
        myfile.write('\n'.join(redditlist))
        
print "All pages done!"
