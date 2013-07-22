from multiprocessing import Process, Queue
import volume
import song

#####COMMANDS####
### (0, int)    -> volume
### (1, string) -> song


def handler(commandq):
    print 'thread func'
    print commandq
    while (1):
        while (commandq.empty==True):
            pass
        command=commandq.get()
        if (command[0]==0):
            pass
            #volume
            #volume.setVolume(command[1]) #this should actually happen immediately
        elif (command[0]==1):
            #song
            song.playSong(command[1])
        else:
            pass
