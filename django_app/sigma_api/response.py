Success = 0
Success_Retrieved = 1
Success_Created = 2
Success_Updated = 3
Success_Deleted = 4

Unauthenticated = 10
Unauthorized = 11
InvalidLocation = 12
InvalidRequest = 13

class Response(Exception):
    def __init__(self, code, content=""):
        self.code = code
        self.content = content
        
#*********************************************************************************************#
        
UnauthenticatedException = Response(Unauthenticated)
UnauthorizedException = Response(Unauthorized)
InvalidLocationException = Response(InvalidLocation)
InvalidRequestException = Response(InvalidRequest)