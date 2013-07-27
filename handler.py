from multiprocessing import Process, Queue
import volume
import song

#####COMMANDS####
### (0, int)    -> volume
### (1, string) -> song


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
            else:
                pass
        elif (stfu.value==1 and current_process!=None):
            current_process.kill()
            current_process=None
            stfu.value=0
        elif (stfu.value==1 and current_process==None):
            stfu.value=0
        else:
            pass
