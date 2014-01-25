import urllib
import urlparse
import re
import time

import ytgets


youtubeuser = raw_input('Type the channel name and press Enter: --> ')
channel_link = 'http://www.youtube.com/user/'+ youtubeuser +'/'

if not ytgets.doesExist(channel_link):
    print "Doesn't look like a channel."
else:
    print "\n","Looks good! - Checking for images now!","\n"
    ytgets.getVideos(ytgets.getPlaylists(channel_link))
