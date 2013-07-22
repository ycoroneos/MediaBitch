from subprocess import call, Popen
directory='/home/yanni/music/'
use_spotify=False

def playSong(song):
    if (use_spotify==False):
        print song
        call(["mpg123", song])
    else:
        pass
