from tornado import gen, iostream
from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop

import random

class Client():

    def __init__(self, server, stream, address):
        self.server = server
        self.address = address
        self.addrname = address
        self.suscribed_to = []
        
        self.stream = stream
        # self.stream.socket.setsockopt( socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # self.stream.socket.setsockopt( socket.IPPROTO_TCP, socket.SO_KEEPALIVE, 1)
        self.stream.set_close_callback(self.on_disconnect)
    
    
    @gen.coroutine
    def on_connect(self):
        try:
            self.addrname, self.port = self.stream.socket.getpeername()
        except Exception:
            pass
            
        self.log('New client')
        IOLoop.current().add_callback(self.handle)
        

    @gen.coroutine
    def on_disconnect(self):
        self.log("Disconnected")
        yield self.server.on_client_disconnect(self)
        
    #*********************************************************************************************#

    def log(self, str):
        print("[API %s] %s"  % (self.addrname, str), flush=True)
        pass
        
    @gen.coroutine
    def send(self, msg):
        yield self.stream.write(msg)
        
    #*********************************************************************************************#

    @gen.coroutine
    def handle(self):
        try:
            yield self.handle_authentication()
            yield self.handle_messaging()
                
        except iostream.StreamClosedError:
            pass

    @gen.coroutine
    def handle_authentication(self):
        pass
        
    @gen.coroutine
    def handle_messaging(self):
        def next_msg_part(msg):
            i = msg.find(':')
            return msg[:i], msg[i+1:]
            
        while True:
            msg = yield self.stream.read_until(b'\0')
            msg = msg.decode('ascii')
            op, msg = next_msg_part(msg)
            
            if op == 'S':
                chan, msg = next_msg_part(msg)
                if not chan in self.suscribed_to:
                    self.suscribed_to.append(chan)
                    self.server.subscribe(self, chan)
                
            elif op == 'P':
                chan, msg = next_msg_part(msg)
                size, msg = next_msg_part(msg)
                content = yield self.stream.read_bytes(int(size))
                self.server.dispatch(self, chan, content)