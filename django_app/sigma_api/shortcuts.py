from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from sigma_api import response

def get_or_raise(queryset, value, field="pk"):
    """
        Try to make a get on the queryset using given parameters,
        or raise an InvalidLocation error
    """
    try:
        dict = {}
        if type(value) == dict:
            dict = value
        elif type(value) == list and type(field) == list:
            dict = {key: val for (key, val) in (field, value)}
        elif type(field) == str:
            dict = {field: value}
        
        return queryset.get(**dict)
        
    except ObjectDoesNotExist:
        raise response.InvalidLocationException
        

        
def get_deserialized(serializer_class, data, *args, **kwargs):
    """
        Return a serializer and a model instance given the serialized data.
        If validation failed, it raises an InvalidRequest error.
    """
        
    serializer = serializer_class(data=data, *args, **kwargs)
    if not serializer.is_valid():
        raise response.InvalidRequestException(serializer.errors)
        
    instance = serializer_class.Meta.model(**serializer.validated_data)
    return serializer, instance   
    
    
    
def call_method_if_exists(obj, name, *args, **kwargs):
    """
        If the the method identified by the given `name` exists, execute it and returns its result.
        Otherwise, return None.
        
        Method version : try to call the method on self
        Static version : takes the object owning the method we try to call, as its first argument.
    """
    
    if hasattr(obj, name):
        f = getattr(obj, name)
        return f(*args, **kwargs)
    return None

    
def check_permission(user, instance, actionname, *args, **kwargs):
    """
        Given action `actionname`, try to call `instance.can_actionname(user, *args, **kwargs)`
        If it exists and returns False, then a PermissionDenied exception is raised.
        
        Static version : takes the model containing the `can_actionname` function, as its first argument.
    """
    if hasattr(instance, 'can_' + actionname):
        f = getattr(instance, 'can_' + actionname)
        if not f(user, *args, **kwargs):
            raise response.UnauthorizedException