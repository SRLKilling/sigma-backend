class WSException(Exception):
    """
        Represents any exception that can be raised within the treatment of a websocket message.
        Basic implementation are message and errors.
        It should always have a message function, returning a dictionary that is to be serialized
    """
    def message(self, id):
        return {}



SUCCESS = 0

class Message(WSException):
    """
        Basic implementation of a response message.
        Takes a code number and a dictionnary representing the answer
    """
    def __init__(self, code, msg=None, **kwargs):
        if msg != None:
            self.msg = msg
        else:
            self.msg = kwargs
            
        self.msg["code"] = code
            
    def message(self):
        return self.msg
        
Response = Message