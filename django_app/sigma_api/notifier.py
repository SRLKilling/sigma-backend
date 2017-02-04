import threading
import socket
import errno
import queue
import time

class DispatcherThread(threading.Thread):
    """
        This class maintains a connection to the central dispatching server.
        It runs in a different thread and can push notifications to the server.
    """
    
    def __init__(self, address, port):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port
        
        self.publish_queue = queue.Queue()
        self.publish_callbacks = [self.send_publish]
        
        self.subscribed_to = []
        self.subscribers = {}
        self.receive_callbacks = []
        
        self.connected = False
        
    def reconnect(self):
        """ This function is used to connect or reconnect to the central dispatch server """
        while not self.connected:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.address, self.port))
                self.sock.setblocking(0)
                self._buffer = b''
                self.connected = True
                
                for chan in self.subscribed_to:
                    self.send_subscribe(chan)
                
            except ConnectionError as e:
                print("Connection failed, trying again in 5s")
                time.sleep(5)
                
        print("Notification client connected to server")
        self.authenticate()
        
    def authenticate(self):
        pass
        
        
    #*********************************************************************************************#
        
    def read_until(self, b):
        """ This function is used to read until we find the given byte """
        while self._buffer.find(b) == -1:
            self._buffer += self.sock.recv(1024)
            
        i = self._buffer.find(b)
        msg, self._buffer = self._buffer[:i+1], self._buffer[i+1:]
        return msg
        
    def read_bytes(self, n):
        """ This function is used to read an array of bytes of given size """
        while len(self._buffer) < n:
            self._buffer += self.sock.recv(1024)
            
        msg, self._buffer = self._buffer[:n], self._buffer[n+1:]
        return msg
        
        
    def run(self):
        self.reconnect()
        
        while True:
            should_wait = True
            
            # Try getting from queue
            try:
                chan, msg = self.publish_queue.get_nowait()
                for cb in self.publish_callbacks:
                    cb(chan, msg)
                self.publish_queue.task_done()
                should_wait = False
            except queue.Empty:
                pass
                
            # Then try getting from socket
            try:
                msg = self.read_until(b'\0').decode('ascii')
                op, msg = next_msg_part(msg)
                if op == 'M':
                    chan, msg = next_msg_part(msg)
                    size, msg = next_msg_part(msg)
                    content = self.read_bytes(int(size)).decode('utf-8')
                    if chan in self.subscribers:
                        for cb in self.subscribers[chan]:
                            cb(chan, content)
                            
                should_wait = False
                
            except BlockingIOError:
                pass
            except socket.error as e:
                if e.errno in (errno.ECONNRESET, errno.ECONNABORTED):
                    self.connected = False
                    self.reconnect()
                elif e.errno == errno.EAGAIN:
                    pass
                else:
                    raise
                    
                    
            if should_wait:
                time.sleep(0.001)
    
    
    #*********************************************************************************************#
    
    def publish(self, chan, message):
        """ Thread-safe function to add a sending message to the queue """
        self.publish_queue.put( (chan, message) )
    
    def send_publish(self, chan, notif):
        """ This function is called within the client thread to actualy send, queue poped messages """
        notif = notif.encode('utf-8')
        header = ("P:"+chan+":" + str(len(notif)) + '\0').encode('ascii')
        self.sock.send(header)
        self.sock.send(notif)
        
    def add_publish_callback(self, cb):
        """ Callbacks will be called when a queued message has been poped and sent """
        self.publish_callbacks.append(cb)
        
    #*********************************************************************************************#
    
    def subscribe(self, chan, cb):
        """ Subscribe to a channel, and specify a callback when a message is read """
        if not chan in self.subscribed_to:
            self.subscribed_to.append(chan)
            if self.connected:
                self.send_subscribe(chan)
            
        if not chan in self.subscribers:
            self.subscribers[chan] = []
        self.subscribers[chan].append(cb)
    
    def send_subscribe(self, chan):
        """ Blocking, but low-latency, function to subscribe to a channel. """ 
        self.sock.send(("S:"+chan+"\0").encode('ascii'))
        
    #*********************************************************************************************#


# Importing the module systematically create a threaded client to the central server
notifier = DispatcherThread("127.0.0.1", 1316)
notifier.start()
def notify(msg):
    notifier.publish("notification", msg)