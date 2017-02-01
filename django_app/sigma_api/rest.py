from rest_framework import viewsets, status, routers
from rest_framework.response import Response

from sigma_api import response, entries

toRestStatus = {}
toRestStatus[response.Success] = status.HTTP_200_OK
toRestStatus[response.Success_Retrieved] = status.HTTP_200_OK
toRestStatus[response.Success_Created] = status.HTTP_201_CREATED
toRestStatus[response.Success_Updated] = status.HTTP_200_OK
toRestStatus[response.Success_Deleted] = status.HTTP_204_NO_CONTENT

toRestStatus[response.Unauthenticated] = status.HTTP_401_UNAUTHORIZED
toRestStatus[response.Unauthorized] = status.HTTP_403_FORBIDDEN
toRestStatus[response.InvalidLocation] = status.HTTP_404_NOT_FOUND
toRestStatus[response.InvalidRequest] = status.HTTP_400_BAD_REQUEST

#*********************************************************************************************#

def entry_to_view(entry):
    func = entry.func
    def view(self, request, *args, **kwargs):
        resp = None
        try:
            resp = func(request.user, request.data, *args, **kwargs)
        except response.Response as r:
            resp = r
            
        return Response(resp.content, status=toRestStatus[resp.code])
    
    # Simulate detail/list route decorator, only if not an existing entry
    if entry.name not in ["list", "retrieve", "create", "update", "destroy"]:
        view.bind_to_methods = (['get'] if (not "method" in entry.kwargs) else entry.kwargs["method"])
        view.detail = entry.detailed
        view.kwargs = {}
        
    return view
    
#*********************************************************************************************#

def entryset_to_viewset(cls):
    views = {}
    for fn, f in cls.entries():
        views[fn] = entry_to_view(f)
    
    ViewSet = type(cls.ressource.name + "ViewSet", (viewsets.ViewSet,), views)
    return ViewSet
    
#*********************************************************************************************#

def generate_router():
    """ Return a router to all the generated viewsets, from registered entrysets """
    import register_list
    
    router = routers.DefaultRouter()
    for entry_name in entries.entries:
        entry = entries.entries[entry_name]
        router.register( entry_name, entryset_to_viewset(entry), base_name=entry.ressource.name)
        
    return router
    