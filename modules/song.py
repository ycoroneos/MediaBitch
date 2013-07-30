#I am using pygrooveshark so credit to who ever made that and stuff

from subprocess import call, Popen
from grooveshark import Client
directory='/home/yanni/music/'
use_spotify=False
groovclient=Client()
groovclient.init()

def playSong(song):
    if (use_spotify==False):
        result=groovclient.search(song, Client.SONGS).next()
        print result
        return Popen(["mplayer", result.stream.url])
    else:
        pass
