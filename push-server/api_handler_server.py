from tornado import gen
from tornado.tcpserver import TCPServer

from api_handler import APIHandler

class APIHandlerServer(TCPServer):

    def __init__(self):
        super().__init__()
        self.clients = set()
        
    @gen.coroutine
    def on_client_disconnect(self, client):
        self.clients.discard(client)
        pass
    
    @gen.coroutine
    def handle_stream(self, stream, address):
        client = APIHandler(self, stream, address)
        self.clients.add(client)
        
        yield client.on_connect()