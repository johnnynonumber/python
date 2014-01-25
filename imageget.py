import ytgets

print "\n"
youtubeuser = raw_input('Type the channel name and press Enter: --> ')
channel_link = 'http://www.youtube.com/user/'+ youtubeuser +'/'

if not ytgets.does_exist(channel_link):
    print "Doesn't look like a channel."
else:
    print "\n","Looks good! - Checking for images now!","\n"
    ytgets.get_videos(ytgets.get_playlists(channel_link))
