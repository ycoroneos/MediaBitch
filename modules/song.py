#I am using pygrooveshark so credit to who ever made that and stuff

from subprocess import call, Popen
from grooveshark import Client
import random
counter=0
directory='/home/yanni/music/' #im not using this but change it to whatever
use_spotify=False
groovclient=Client()
groovclient.init()

def playSong(song):
    if (use_spotify==False):
        result=groovclient.search(song, Client.SONGS).next()
        try:
            return Popen(["cvlc", "--play-and-exit", result.stream.url])
        except:
            pass
    else:
        pass

def playStreamUrl(url):
    return Popen(["cvlc", "--play-and-exit", url])

def playList(playlist_id, shuffle, repeat): #the id is an int, others are bool
    result=groovclient.playlist(playlist_id)
    songs=list(result.songs)
    if (shuffle==True):
        random.shuffle(songs, random.random)
    if (repeat==True):
        #yeah so I'm not quite sure how to _best_ implement this feature yet
        pass
    return [i.stream.url for i in songs]

def cacheStreamUrl(url):
    global counter
    print 'caching song ' + url + '\r\n'
    savename="song"+str(counter)+".ogg"
    call(["cvlc", "--play-and-exit", url, "--sout", "file/ogg:"+str(savename)])
    counter+=1
    return str(savename)

def playCachedSong(filename):
    print "attempting to play" + filename + " locally\r\n"
    return Popen(["cvlc", "--play-and-exit", filename])
