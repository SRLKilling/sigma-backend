from websocket import message

class WSErrorException(message.WSException):
    """
        Represents any error exception that can occur during the treatment.
    """
    pass
        

        
def createWSException(errcode):
    """
        Out of an error code, create a new WSException class corresponding to the error code
    """
    def message(self):
        return { "code" : errcode }
        
    return type("GeneratedWSException", (WSErrorException,),  { "message" : message })
    
   
   
INPUT_INVALID_JSON = 1
InputInvalidJSONException = createWSException(INPUT_INVALID_JSON)

INPUT_INVALID_CONTENT = 2
InputInvalidContent = createWSException(INPUT_INVALID_CONTENT)

INPUT_MISSING_ID = 3
InputMissingIdException = createWSException(INPUT_MISSING_ID)

INPUT_MISSING_ACTION = 4
InputMissingActionException = createWSException(INPUT_MISSING_ACTION)

INPUT_INVALID_ACTION = 5
InputInvalidActionException = createWSException(INPUT_INVALID_ACTION)



PROTOCOL_MISSING_TOKEN = 111
ProtocolMissingTokenException = createWSException(PROTOCOL_MISSING_TOKEN)

PROTOCOL_INVALID_TOKEN = 112
ProtocolInvalidTokenException = createWSException(PROTOCOL_INVALID_TOKEN)



PROTOCOL_MISSING_REST_ACTION = 121
ProtocolMissingRESTActionException = createWSException(PROTOCOL_MISSING_REST_ACTION)

PROTOCOL_INVALID_REST_ACTION = 122
ProtocolInvalidRESTActionException = createWSException(PROTOCOL_INVALID_REST_ACTION)

PROTOCOL_MISSING_REST_LOCATION = 123
ProtocolMissingRESTLocationException = createWSException(PROTOCOL_MISSING_REST_LOCATION)

PROTOCOL_INVALID_REST_LOCATION = 124
ProtocolInvalidRESTLocationException = createWSException(PROTOCOL_INVALID_REST_LOCATION)