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
    
# def get_instance_from_serializer(serializer):
    # """
        # Return a model instance out of a serializer.
        # Either create a new one, or update the one given to serializer constructor.
        # The object is not save to the database.
        # This can only be used without nested objects.                                               # TODO : pretty sure we could write some code to deal with relations
    # """
    # ModelClass = serializer.__class__.Meta.model
    # if hasattr(serializer, "instance"):
        # instance = ModelClass(serializer.instance)
        # for attr, value in serializer.validated_data.items():
            # setattr(instance, attr, value)
        # return instance
    # else:
        # return ModelClass(**serializer.validated_data)
    
    
    
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