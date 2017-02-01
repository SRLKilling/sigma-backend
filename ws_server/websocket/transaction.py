from tornado import gen

from websocket import message, errors
from sigma_core.actions.authenticate import authenticate as django_authenticate

class Transaction:
    
    def __init__(self, ws, id):
        self.ws = ws
        self.env = ws.env
        self.id = id
        self.response = None
        
        self.actions =  {
            "AUTH" : self.authenticate,
            "REST_API" : self.rest_action,
        }
        
        self.rest_locations = (
            "group",
            "test",
        )
        
    @gen.coroutine
    def handle_message(self, msg):
        if self.response == None:
            action = msg.get("action")
            if action == None:
                raise errors.InputMissingActionException()
            
            action = self.actions.get(action)
            if action == None:
                raise errors.InputInvalidActionException()
                
            yield action(msg)
        
        else:
            yield self.handle_confirmation(msg)
            
            
    @gen.coroutine
    def authenticate(self, msg):
        token = msg.get("token")
        if token == None:
            raise errors.ProtocolMissingTokenException()
        
        auth_info = django_authenticate(token)
        if auth_info == None:
            raise errors.ProtocolInvalidTokenException()
        
        self.env['user'] = auth_info.user
        raise message.Message(message.SUCCESS)
        
        
    @gen.coroutine
    def rest_action(self, msg):
        rest_action = msg.get("REST_action")
        rest_location = msg.get("REST_location")
        
        if rest_action == None:
            raise errors.ProtocolMissingRESTActionException()
        if rest_location == None:
            raise errors.ProtocolMissingRESTLocationException()
            
        from sigma_core.actions.test import GroupActionSet
        r = GroupActionSet.getAvailableGroups(self.env['user'], None)
        
        raise message.Message(message.SUCCESS, response = r)
        
        # if not rest_location in self.rest_locations:
            # raise errors.ProtocolInvalidRESTActionException()
            
        # action_mod = importlib.import_module("sigma_core.actions." + rest_location)
        
    @gen.coroutine
    def post_message(self, msg):
        # Si je lai, ok, je gère, si pas dans redis,
        # Je demande à django de me la mettre en cache
        pass
            
        