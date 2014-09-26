# Read username, output from empty factory, drop connections
import sys
sys.path.append(r'modules/')
from multiprocessing import Process, Queue, Value
import handler

from twisted.internet import protocol, reactor
from twisted.protocols import basic
import mbprotocol

#for websockets
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
import websocketmbprotocol

commandq=Queue()
stfu_var=Value('i', 0)
pause_var=Value('i', 0)
overwatch=Process(target=handler.handler, args=(commandq, stfu_var, pause_var,))
overwatch.start()

class WebSocketMBFactory(WebSocketServerFactory):
    protocol=websocketmbprotocol.MBProtocol

    def __init__(self, url, debug=False, debugCodepaths=False):
        WebSocketServerFactory.__init__(self, url)

    def addConnection(self):
        self.connections+=1

    def removeConnection(self):
        self.connections-=1

    def stfu(self):
        stfu_var.value=1

    def pup(self):
        pause_var=not pause_var
    
    def enq(self, command):
        commandq.put(command)

class MBFactory(protocol.ServerFactory):
    protocol = mbprotocol.MBProtocol

    def __init__(self):
        self.connections=0
        '''self.commandq=commandq
        self.stfu_var=stfu_var
        self.pause_var=pause_var'''

    def addConnection(self):
        self.connections+=1

    def removeConnection(self):
        self.connections-=1

    def stfu(self):
        stfu_var.value=1

    def pup(self):
        pause_var=not pause_var
    
    def enq(self, command):
        commandq.put(command)

    def showq(self):
        print commandq

reactor.listenTCP(666, MBFactory())
listenWS(WebSocketMBFactory("ws://localhost:1308", True, True))
reactor.run()
