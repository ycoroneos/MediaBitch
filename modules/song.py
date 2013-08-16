#I am using pygrooveshark so credit to who ever made that and stuff

from subprocess import call, Popen
from grooveshark import Client
import random
directory='/home/yanni/music/'
use_spotify=False
groovclient=Client()
groovclient.init()

def playSong(song):
    if (use_spotify==False):
        result=groovclient.search(song, Client.SONGS).next()
        if (result!=None):
            print result
            return Popen(["cvlc", "--play-and-exit", result.stream.url])
        else:
            pass
    else:
        pass

def playStreamUrl(url):
    return Popen(["cvlc", "--play-and-exit", result.stream.url])

def playList(playlist_id, shuffle, repeat): #the id is an int, others are bool
    result=groovclient.playlist(playlist_id)
    songs=list(result.songs)
    if (shuffle==True):
        random.shuffle(songs, random.random)
    if (repeat==True):
        pass
    return [i.stream.url for i in songs]
