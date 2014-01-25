import urllib
import urlparse
import re
import time

def getPlaylists(channel):
	# Get a list of playlists
	channel_page = urllib.urlopen(channel)
	channel_page_source = channel_page.read()

	playlist_regex = 'data-context-item-id="(.+?)"'
	get_playlist_ID = re.findall(playlist_regex,channel_page_source)
	return get_playlist_ID;


def getVideos(playlist):
	for i in playlist:
		playlist_source = urllib.urlopen('http://www.youtube.com/playlist?list='+i+'').read()
		video_ID_regex = 'data-video-ids="(.+?)"'
		get_video_ID = re.findall(video_ID_regex,playlist_source)
		imagelist = []
		linklist = []

		for v in get_video_ID:
			video_page = urllib.urlopen('http://www.youtube.com/watch?v='+v+'')
			video_page_source = video_page.read()
			image_URL_regex = 'http://i1.ytimg.com/vi/?[a-zA-Z0-9_-]*/maxresdefault.jpg'
			imagelist.append(re.findall(image_URL_regex,video_page_source))

		#print len(imagelist)

		for y in imagelist:
			print y[0]
			#linklist.append(y[0])

		#print linklist
'''			


		for x in linklist:
			split = urlparse.urlsplit(x)
			name1 = split.path.split("/vi")[-1]
			name2 = name1.replace("maxresdefault", "", 2)
			save_name = name2.replace("/", "", 2)
			urllib.urlretrieve(''+x+'','img/'+save_name+'')
'''		
getVideos(getPlaylists('http://www.youtube.com/user/MrSuicideSheep/videos?view=1'))


'''
http://www.youtube.com/playlist?list=PLDfKAXSi6kUaC_97psoMGgUKjLk7RyXj9
'''
