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

        result=stfu_regex.match(line)
        if (result!=None):
            self.transport.write('stfu-ing\r\n')
            self.factory.stfu_var.value=1
            return

        result=playlist_regex.match(line)
        if (result!=None):
            #queue playlist
            self.transport.write('queuing playlist \r\n')
            command=[[2,x] for x in song.playList(int(line[len(result.group(0)):]), True, False)]
            print str(command)+'\r\n'
            self.factory.commandq.put(command[0])
            return

        result=song_regex.match(line)
        if (result!=None):
            #queue song
            self.transport.write('queuing song \r\n')
            #song.playSong(line[len(result.group(0)):])
            self.factory.commandq.put([1,line[len(result.group(0)):]])
            return

        result=playlist_regex.match(line)
        if (result!=None):
            #queue playlist
            self.transport.write('queuing playlist \r\n')
            self.factory.commandq.put([[2,x] for x in song.playList(int(result), True, False)])
            return

        self.transport.write('pattern not found...\r\n')
        return
