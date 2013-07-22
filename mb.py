# Read username, output from empty factory, drop connections
from twisted.internet import protocol, reactor
from twisted.protocols import basic
import mbprotocol

class MBFactory(protocol.ServerFactory):
    protocol = mbprotocol.MBProtocol

    def __init__(self):
        self.connections=0

    def addConnection(self):
        self.connections+=1

    def removeConnection(self):
        self.connection-=1

    def getUser(self, user):
        return "No such user"

reactor.listenTCP(1308, MBFactory())
reactor.run()
