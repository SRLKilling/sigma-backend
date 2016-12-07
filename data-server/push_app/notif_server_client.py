
from tornado import gen, queues
from tornado.tcpclient import TCPClient
from tornado.ioloop import IOLoop

class NotifServerClient():

    def __init__(self, handler, addr, port):
        self.handler = handler
        self.addr = addr
        self.port = port
        self.retry_time = 10
        
        self.debug = True
        
        self.stream = None
        self.queue = queues.Queue()
        
        IOLoop.current().add_callback(self.connect)
        
    def log(self, str):
        if self.debug:
            print("[%s:%d] %s"  % (self.addr, self.port, str), flush=True)
        
        
        
    @gen.coroutine
    def connect(self):
        while self.stream == None:
            try:
                self.log("Trying to connect...")
                self.stream = yield TCPClient().connect(self.addr, self.port)
                self.stream.set_close_callback(self.on_disconnect)
            
            except Exception as e:
                self.log("Connection failed, trying to reconnect in %d seconds" % self.retry_time)
                yield gen.sleep(self.retry_time)
                
        self.log("Connection succeeded")
        while True:
            data = yield self.queue.get();
            yield self.on_data(data)
        
    @gen.coroutine
    def on_disconnect(self):
        self.stream = None
        self.log("Disconnected, trying to reconnect in %d seconds" % self.retry_time)
        yield gen.sleep(self.retry_time)
        yield self.connect()
        
        
        
    @gen.coroutine
    def on_data(self, data):
        yield self.stream.write( data.encode("utf-8") );