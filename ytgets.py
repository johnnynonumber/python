import urllib
import urlparse
import re
import time

def does_exist(channel_link):
    '''
    Takes a YouTube channel link, checks for the "empty channel" message
    Returns True if message isn't found
    ''' 
    i = urllib.urlopen(channel_link).read()
    regex = '<div class="channel-empty-message banner-message">'
    check = re.findall(regex,i)
    if not check:
        return True;

def get_playlists(channel_link):
    '''
    Takes a channel link and forms the channel playlist gallery URL
    Scrapes the gallery and returns playlist IDs
    '''
    playlist_gallery = ''+ channel_link + 'videos?view=1'''

    playlist_gallery_source = urllib.urlopen(playlist_gallery).read()
    playlist_regex = 'data-context-item-id="(.+?)"'

    playlist_IDs = re.findall(playlist_regex,playlist_gallery_source)
    return playlist_IDs;

def get_videos(playlist_IDs):
    '''
    Takes a list of playlist IDs and forms playlist URLs
    Scrapes the playlist page for video IDs, and form video URLs
    Scrapes each video for the high res image, and adds the image URL to a list
    '''
    imageurl_list = []
    linklist_raw = []
    linklist_striped = []

    for ID in playlist_IDs:

        playlist_source = urllib.urlopen('http://www.youtube.com/playlist?list='+ID+'').read()
        playlist_title_regex = '<h2 class="epic-nav-item-heading">(.+?)</h2>'
        video_ID_regex = 'data-video-ids="(.+?)"'

        playlist_title_raw = re.findall(playlist_title_regex, playlist_source)
        video_IDs = re.findall(video_ID_regex,playlist_source)

        for title in playlist_title_raw:
            print "\n","Playlist is:",title

        for v in video_IDs:
            video_page = urllib.urlopen('http://www.youtube.com/watch?v='+v+'')
            video_page_source = video_page.read()
            image_URL_regex = 'http://i1.ytimg.com/vi/[a-zA-Z0-9_-]*/maxresdefault.jpg'
            f = re.findall(image_URL_regex,video_page_source)
            if f:
                linklist_raw.append(f)
            else:
                pass
            # linklist_raw.append(re.findall(image_URL_regex,video_page_source))
            # print v
    for link in linklist_raw:
                #split = urlparse.urlsplit(link[0])
                #name1 = split.path.split("//")[-1]
                #print name1
                print link[0]
                #name2 = name1.replace("maxresdefault", "", 2)
                #save_name = name2.replace("/", "", 2)
                #urllib.urlretrieve(''+x+'','img/'+save_name+'')

    print "\n","Done!!","\n"
