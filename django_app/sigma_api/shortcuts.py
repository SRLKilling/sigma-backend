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
        

        
def get_validated_serializer(serializer_class, *args, **kwargs):
    """
        Return a serializer after checking for validation.
        If validation failed, an InvalidRequestException is raised
    """
        
    serializer = serializer_class(*args, **kwargs)
    if not serializer.is_valid():
        raise response.InvalidRequestException(serializer.errors)
    return serializer
    
    
def call_method_if_exists(obj, name, *args, **kwargs):
    """
        If the the method identified by the given `name` exists, execute it and returns its result.
        Otherwise, return None.
    """
    
    if hasattr(obj, name):
        f = getattr(obj, name)
        return f(*args, **kwargs)
    return None

    
def check_permission(user, instance, actionname, *args, **kwargs):
    """
        Given action `actionname`, try to call `instance.can_actionname(user, *args, **kwargs)`
        If it exists and returns False, then a PermissionDenied exception is raised.
    """
    if hasattr(instance, 'can_' + actionname):
        f = getattr(instance, 'can_' + actionname)
        if not f(user, *args, **kwargs):
            raise response.UnauthorizedException
            
            
def get_queryset(queryset_gen, user, data):
    """
        Return a queryset from any valid queryset generator.
        It can be a queryset, a manager, or a function returning a queryset, given the user
    """
        
    if isinstance(queryset_gen, models.QuerySet):
        return queryset_gen
    elif isinstance(queryset_gen, models.Manager):
        return queryset_gen.all()
    else:
        return queryset_gen(user)
        

#*********************************************************************************************#


def retrieve(user, data, pk, queryset_gen, serializer_class, action_name):
    """
        This method returns an entry used to retrieve a ressource.
        It tries to get the pk-ed element, and returns its serialized data
    """
    qs = get_queryset(queryset_gen, user, data)
    instance = get_or_raise(qs, pk)
    
    check_permission(user, instance, action_name)
    serializer = serializer_class(instance)
    return response.Response(response.Success_Retrieved, serializer.data)


def list(user, data, queryset_gen, serializer_class):
    """
        This method returns an entry that is used to list a queryset.
        It first get the queryset giving user and data to the given queryset constructor.
        It then eventualy filters the queryset using the provided filter_class, and data.uri_param
        Finally, returns the serialized data using serializer_class
    """
    queryset = get_queryset(queryset_gen, user, data)
    # if filter_class != None:                                                                                          # TODO : filtering
        # filter = filter_class(queryset=queryset, data=data.uri_param)
        # queryset = filter.qs()
    serializer = serializer_class(queryset, many=True)
    return response.Response(response.Success_Retrieved, serializer.data)
    
    
def create(user, data, serializer_class, action_name):
    """
        This method is an entry that create a new ressource.
        It deserialize the data using the provided serializer_class,
        Then check for permissions, and save the object in the database
    """
    serializer = get_validated_serializer(serializer_class, data=data)
    instance = serializer_class.Meta.model(**serializer.validated_data)
    check_permission(user, instance, action_name)
    instance.save()
    return response.Response(response.Success_Created, serializer_class(instance).data)    
    
def update(user, data, pk, serializer_class, action_name):
    """
        This method is used to perform (potentially partial) updates.
        It first gets a model instance out of the de-serialized data. 
        Then, we try to get the real instance, using the pk.
        We check permissions giving both the to-be-updated, and the original instances.
        If true, we merge them, save the result, and returns the new object serialized
    """
    instance = get_or_raise(serializer_class.Meta.model.objects.all(), pk)
    check_permission(user, instance, action_name, data)
    new_ser = get_validated_serializer(serializer_class, instance, data=data, partial=True)
    new_ser.save()
    return response.Response(response.Success_Updated, new_ser.data)
    
def destroy(user, data, queryset_gen, action_name):
    """
        This method is an entry that create a new ressource.
        Then check for permissions, and save the object in the database
    """
    queryset = get_queryset(queryset_gen, user, data)
    instance = get_or_raise(queryset, pk)
    check_permission(user, instance, action_name)
    instance.delete()
    return response.Response(response.Success_Deleted)
