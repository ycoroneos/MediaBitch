from twisted.internet import protocol, reactor
from twisted.protocols import basic
import re
import volume
import song

#Should soon be improved to queue things to a command queue that's managed by the factory

vol_regex=re.compile('mb vol ')
song_regex=re.compile('mb ')
stfu_regex=re.compile('mb stfu')
playlist_regex=re.compile('mb playlist ')
status_regex=re.compile('mb queue')
pause_regex=re.compile('mb pup')

class MBProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.factory.addConnection()

    def connectionLost(self, reason):
        self.factory.removeConnection()

    def lineReceived(self, line):
        result=None
        result=vol_regex.match(line)
        if (result!=None):
            #change volume
            self.transport.write('changing volume \r\n')
            vol=line[len(result.group(0)):]
            volume.setVolume(vol)
            #self.factory.commandq.put([0,vol])
            return

        result=status_regex.match(line)
        if (result!=None):
            return

        result=stfu_regex.match(line)
        if (result!=None):
            self.transport.write('stfu-ing\r\n')
            self.factory.stfu()
            return

        result=playlist_regex.match(line)
        if (result!=None):
            #queue playlist
            self.transport.write('queuing playlist and caching songs!\r\n')
            playlist=song.playList(int(line[len(result.group(0)):]), True, False)
            self.factory.enq([2,playlist[0]])
            #self.factory.commandq.put([2,playlist[0]])
            command=[[4,song.cacheStreamUrl(x)] for x in playlist[1:]]
            #command=[[3,x] for x in playlist[1:]]
            for i in command:
                #self.factory.commandq.put(i)
                self.factory.enq(i)
            return

        result=pause_regex.match(line)
        if (result!=None):
            self.factory.pup()
            return

        result=song_regex.match(line)
        if (result!=None):
            #queue song
            self.transport.write('queuing song \r\n')
            #song.playSong(line[len(result.group(0)):])
            self.factory.enq([1,line[len(result.group(0)):]])
            #self.factory.commandq.put([1,line[len(result.group(0)):]])
            return


        self.transport.write('pattern not found...\r\n')
        return
