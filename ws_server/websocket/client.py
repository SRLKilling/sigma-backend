import importlib
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from tornado import gen

from websocket import message, errors, transaction
import settings

json = importlib.import_module( getattr(settings, "JSON_LIB", "json") )


class WebSocketClient(WebSocketHandler):

    client_set = set()
    
    @staticmethod
    def publish(chan, msg):
        msg = json.loads(msg)
        if chan == "notification":
            for c in WebSocketClient.client_set:
                c.send_notif(msg)

    #*********************************************************************************************#
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transactions = {}
        self.env = {}
        self.debug = True
        self.nextId = -1
        
    # Used to indicate all origins (i.e. clients) are accepted
    def check_origin(self, origin):
        return True
        
    def open(self):
        WebSocketClient.client_set.add(self)
        self.log("New client connection")
        
    def on_close(self):
        WebSocketClient.client_set.discard(self)
        self.log('Connection closed')
    
    #*********************************************************************************************#
        
    def log(self, msg):
        """
            Log informations to the standard output as well as in the log file                          TODO
        """
        if self.debug:
            print("[WS] %s"  % msg, flush=True)
    
    
    @gen.coroutine
    def send_message(self, msg, id):
        """
            Serialize message to json and then sends it through the websocket
        """
        msg["id"] = id
        msg = json.dumps(msg)
        yield self.write_message(msg)
    
    #*********************************************************************************************#
        
    def get_new_transaction(self, id):
        """
            Create and store a new transaction
        """
        tr = transaction.Transaction(self, id)
        self.transactions[id] = tr
        return tr
        
    @gen.coroutine
    def handle_message(self, msg):
        """
            Handle a message, creating a transaction if needed, or retrieving it, and then,
            yielding a call to the transaction's handler
        """
        # First, try loading the json, and getting the transaction id
        try:
            try:
                msg = json.loads(msg)
            except ValueError:
                raise errors.InputInvalidJSONException()
                
            if not isinstance(msg, dict):
                raise errors.InputInvalidContentException()
                
                
            id = msg.get("id")
            if id == None:
                raise errors.InputMissingIdException()
                
        except Exception as e:
            if isinstance(e, message.WSException):
                IOLoop.current().spawn_callback(self.send_message, e.message(), -1)
            else:
                raise e;
                
        # Then either handle the message on the already existing transaction, or create a new transaction based on the provided protocol
        try:
            tr = None
            if id not in self.transactions:
                tr = self.get_new_transaction(id)
            else:
                tr = self.transactions[id]
            
            yield tr.handle_message(msg)
        
        except Exception as e:
            if isinstance(e, message.WSException):
                IOLoop.current().spawn_callback(self.send_message, e.message(), id)
            else:
                raise e;
      
    def on_message(self, msg):
        """
            This method is used when the websocket receive a message.
            It spawns a callback to the internal coroutine version of message handler
        """
        IOLoop.current().spawn_callback(self.handle_message, msg)
        
        
    #*********************************************************************************************#
    
    def send_notif(self, msg):
        tr = self.get_new_transaction(self.nextId)
        self.transactions[self.nextId] = tr
        
        IOLoop.current().add_callback(self.send_message, msg, self.nextId)
        self.nextId -= 1
        