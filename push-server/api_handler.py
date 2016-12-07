import socket

import tornado.gen
import tornado.ioloop
import tornado.iostream
import tornado.tcpserver

from websocket_client import WebSocketClient

class APIHandler():

    def __init__(self, server, stream, address):
        self.server = server
        self.address = address
        self.addrname = address
        
        self.debug = True
        
        self.stream = stream
        # self.stream.socket.setsockopt( socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # self.stream.socket.setsockopt( socket.IPPROTO_TCP, socket.SO_KEEPALIVE, 1)
        self.stream.set_close_callback(self.on_disconnect)

    def log(self, str):
        if self.debug:
            print("[API %s] %s"  % (self.addrname, str), flush=True)
    
    
    @tornado.gen.coroutine
    def on_connect(self):
        try:
            self.addrname, self.port = self.stream.socket.getpeername()
        except Exception:
            pass
            
        self.log('New client')
        yield self.handle()
        

    @tornado.gen.coroutine
    def on_disconnect(self):
        self.log("Disconnected")
        yield self.server.on_client_disconnect(self)
        

    @tornado.gen.coroutine
    def handle(self):
        try:
            while True:
                line = yield self.stream.read_until(b'\n')
                WebSocketClient.sendToAll(line)
                
        except tornado.iostream.StreamClosedError:
            pass
