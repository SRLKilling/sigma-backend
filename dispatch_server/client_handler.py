from tornado import gen
from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop

from client import Client

class ClientHandler(TCPServer):

    def __init__(self):
        super().__init__()
        self.clients = set()
        self.listeners = {}
        
    @gen.coroutine
    def on_client_disconnect(self, client):
        for channels in client.suscribed_to:
            self.listeners[channels].remove(client)
        self.clients.discard(client)
    
    @gen.coroutine
    def handle_stream(self, stream, address):
        client = Client(self, stream, address)
        self.clients.add(client)
        
        IOLoop.current().add_callback(client.on_connect)
        
    #*********************************************************************************************#
    
    @gen.coroutine
    def subscribe(self, listener, chan):
        print("SUSCRIBED to", chan)
        if not chan in self.listeners:
            self.listeners[chan] = []
        self.listeners[chan].append(listener)
        
    @gen.coroutine
    def dispatch(self, publisher, chan, msg):
        if not chan in self.listeners:
            return
            
        content = msg
        header = ('M:'+chan+':'+str(len(content))+'\0').encode('ascii')
        print(header)
        for client in self.listeners[chan]:
            print(publisher)
            print(client)
            if client != publisher:
                yield client.send(header)
                yield client.send(content)