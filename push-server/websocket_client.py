from tornado.websocket import WebSocketHandler

class WebSocketClient(WebSocketHandler):
    
    # Store the list of currently connected websocket
    client_set = set()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug = True
        
    # Used to indicate all origins (i.e. clients) are accepted
    def check_origin(self, origin):
        return True
        
        
    def log(self, msg):
        if self.debug:
            print("[Client] %s"  % msg, flush=True)
    

    def open(self):
        WebSocketClient.client_set.add(self)
        self.log("New client connection")
      
    def on_message(self, message):
        self.log('Message received %s' % message)
 
    def on_close(self):
        WebSocketClient.client_set.discard(self)
        self.log('Connection closed')
 
 
    @staticmethod
    def sendToAll(msg):
        for client in WebSocketClient.client_set:
            client.send(msg)
 
    def send(self, msg):
        self.write_message(msg)