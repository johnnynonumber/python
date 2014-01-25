import urllib
import urlparse
import re
import time

def doesExist(channel_link):
        '''
        Takes a YouTube channel link, checks for the "empty channel" message
        Returns True if message isn't found
        ''' 
        i = urllib.urlopen(channel_link).read()
        regex = '<div class="channel-empty-message banner-message">'
        check = re.findall(regex,i)
        if not check:
                return True;

def getPlaylists(channel_link):
        '''
        Takes a channel link and forms the channel playlist gallery URL
        Scrapes the gallery and returns playlist IDs
        '''
        playlist_gallery = ''+ channel_link + 'videos?view=1'''

        playlist_gallery_source = urllib.urlopen(playlist_gallery).read()
        playlist_regex = 'data-context-item-id="(.+?)"'

        playlist_IDs = re.findall(playlist_regex,playlist_gallery_source)
        return playlist_IDs;

def getVideos(playlist_IDs):
        '''
        Takes a list of playlist IDs and forms playlist URLs
        Scrapes the playlist page for video IDs, and form video URLs
        Scrapes each video for the high res image, and adds the image URL to a list

        '''
        for i in playlist_IDs:

                playlist_source = urllib.urlopen('http://www.youtube.com/playlist?list='+i+'').read()
                playlist_title_regex = '<h2 class="epic-nav-item-heading">(.+?)</h2>'
                video_ID_regex = 'data-video-ids="(.+?)"'

                playlist_title_raw = str(re.findall(playlist_title_regex, playlist_source))
                video_IDs = re.findall(video_ID_regex,playlist_source)
     
                imagelist = []
                linklist = []

                for v in video_IDs:
                        video_page = urllib.urlopen('http://www.youtube.com/watch?v='+v+'')
                        video_page_source = video_page.read()
                        image_URL_regex = 'http://i1.ytimg.com/vi/?[a-zA-Z0-9_-]*/maxresdefault.jpg'
                        imagelist.append(re.findall(image_URL_regex,video_page_source))

                for y in imagelist:
                        #print y[0]
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


youtubeuser = raw_input('Type the channel name and press Enter: --> ')
channel_link = 'http://www.youtube.com/user/'+ youtubeuser +'/'

if not doesExist(channel_link):
        print "Doesn't look like a channel."
else:
        print "\n","Looks good! - Checking for images now!","\n"
        getVideos(getPlaylists(channel_link))


'''
http://www.youtube.com/playlist?list=PLDfKAXSi6kUaC_97psoMGgUKjLk7RyXj9
'''
