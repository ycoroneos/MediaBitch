# Read username, output from empty factory, drop connections
import sys
sys.path.append(r'modules/')
from multiprocessing import Process, Queue
import handler

from twisted.internet import protocol, reactor
from twisted.protocols import basic
import mbprotocol

class MBFactory(protocol.ServerFactory):
    protocol = mbprotocol.MBProtocol

    def __init__(self):
        self.connections=0
        self.commandq=Queue()
        self.overwatch=Process(target=handler.handler, args=(self.commandq,))
        self.overwatch.start()

    def addConnection(self):
        self.connections+=1

    def removeConnection(self):
        self.connection-=1

    def enq(self):
        #self.commandq.put(command)
        pass

    def showq(self):
        print self.commandq

reactor.listenTCP(1308, MBFactory())
reactor.run()
