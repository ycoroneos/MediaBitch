# Read username, output from empty factory, drop connections
import sys
sys.path.append(r'modules/')
from multiprocessing import Process, Queue, Value
import handler

from twisted.internet import protocol, reactor
from twisted.protocols import basic
import mbprotocol

class MBFactory(protocol.ServerFactory):
    protocol = mbprotocol.MBProtocol

    def __init__(self):
        self.connections=0
        self.commandq=Queue()
        self.stfu_var=Value('i', 0)
        self.overwatch=Process(target=handler.handler, args=(self.commandq, self.stfu_var,))
        self.overwatch.start()

    def addConnection(self):
        self.connections+=1

    def removeConnection(self):
        self.connections-=1

    def stfu(self):
        self.stfu_var.value=1

    def enq(self):
        #self.commandq.put(command)
        pass

    def showq(self):
        print self.commandq

reactor.listenTCP(1308, MBFactory())
reactor.run()
