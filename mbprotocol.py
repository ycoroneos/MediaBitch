from twisted.internet import protocol, reactor
from twisted.protocols import basic
import re


#Should soon be improved to queue things to a command queue that's managed by the factory

vol_regex=re.compile('mb vol ')
song_regex=re.compile('mb ')

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
            return
        result=song_regex.match(line)
        if (result!=None):
            #queue song
            self.transport.write('changing song \r\n')
            song=line[len(result.group(0)):]
            return
        self.transport.write('pattern not found \r\n')
        return
