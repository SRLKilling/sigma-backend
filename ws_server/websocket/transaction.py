from tornado import gen

from websocket import message, errors
from sigma_api.authenticate import authenticate as django_authenticate
from sigma_api import entries, response

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
        rest_location = msg.get("REST_location")
        rest_action = msg.get("REST_action")
        rest_data = msg.get("REST_data", {})
        rest_pk = msg.get("REST_pk", None)
        
        if rest_action == None:
            raise errors.ProtocolMissingRESTActionException()
        if rest_location == None:
            raise errors.ProtocolMissingRESTLocationException()
        
        entry = entries.route_to_entry(rest_location, rest_action)
        user = self.env.get('user', None)
        
        try:
            if entry.detailed and rest_pk != None:
                resp = entry(user, rest_data, rest_pk)
            else:
                resp = entry(user, rest_data)
                
            raise message.Message(message.SUCCESS, response = {"code": resp.code, "content": resp.content})
            
        except entries.InvalidLocEntryException:
            raise errors.ProtocolInvalidRESTLocationException;
        except entries.InvalidActionEntryException:
            raise errors.ProtocolInvalidRESTActionException;
        except response.Response as resp:
            raise message.Message(message.SUCCESS, response = {"code": resp.code, "content": resp.content})
        
    @gen.coroutine
    def post_message(self, msg):
        # Si je lai, ok, je gère, si pas dans redis,
        # Je demande à django de me la mettre en cache
        pass
            
        