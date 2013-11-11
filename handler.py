from multiprocessing import Process, Queue
import volume
import song

#####COMMANDS####
### (0, int)    -> volume
### (1, string) -> song
### (2, string) -> grooveshark stream url
### (3, string) -> cache grooveshark song from url
### (4, string) -> play cached song from file

#This works fairly well now but I anticipate that it will need cleanup in the future
def handler(commandq, stfu):
    print commandq
    current_process=None
    while (1):
        if (current_process==None or current_process.poll()==False):
            command=commandq.get()
            if (command[0]==0):
                #volume
                pass
            elif (command[0]==1):
                #song
                current_process=song.playSong(command[1])
            elif (command[0]==2):
                #play a url
                current_process=song.playStreamUrl(command[1])
            elif (command[0]==3):
                #cache a url
                #this blocks so please don't really use it
                filename=song.cacheStreamUrl(command[1])
                commandq.put([4,filename])
            elif (command[0]==4):
                current_process=song.playCachedSong(command[1])
            else:
                #ummmmm idunnodosumthing
                #antigravity.setLevel(0.1G)
                pass
        elif (stfu.value==1 and current_process!=None):
            current_process.kill()
            current_process=None
            stfu.value=0
        elif (stfu.value==1 and current_process==None):
            stfu.value=0
        else:
            pass
