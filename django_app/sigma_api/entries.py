from sigma_api import response, shortcuts

#*********************************************************************************************#
    
entries = {}
    
class EntrySet():
    """ This class wraps a set of entries and provide a way to turn it to a DRF Viewset """ 
    
    @classmethod
    def entries(cls):
        for fn in cls.__dict__:
            f = cls.__dict__[fn]
            if isinstance(f, Entry):
                yield (fn, f)
                
    @classmethod
    def register(cls, name):
        entries[name] = cls
        
        

class Entry():
    """ This class wraps an entry function """
    
    def __init__(self, name, func, detailed, **kwargs):
        self.name = name
        self.func = func
        self.detailed = detailed
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)
        
        
#*********************************************************************************************#


def global_entry(name = None, **kwargs):
    """ This is the decorator used to generate global entries (i.e. not bound to a specific ressource) """
    def decorator(func):
        n = (name) if (name != None) else (func.__name__)
        return Entry(n, func, False, **kwargs)
    return decorator

def detailed_entry(name = None, **kwargs):
    """ Generate a detailed entry (i.e. with a pk) """
    def decorator(func):
        n = (name) if (name != None) else (func.__name__)
        return Entry(n, func, True, **kwargs)
    return decorator
    
    
#*********************************************************************************************#


def retrieve(queryset_class, serializer_class, action_name="retrieve"):
    """
        This method returns an entry used to retrieve a ressource.
        It tries to get the pk-ed element, and returns its serialized data
    """
    @detailed_entry(name=action_name)
    def entry(user, data, pk):
        qs = queryset_class(user, data)
        instance = shortcuts.get_or_raise(qs, pk)
        
        shortcuts.check_permission(user, instance, action_name)
        serializer = serializer_class(instance)
        return response.Response(response.Success_Retrieved, serializer.data)
        
    return entry

def list(queryset_class, serializer_class, filter_class = None, action_name="list"):
    """
        This method returns an entry that is used to list a queryset.
        It first get the queryset giving user and data to the given queryset constructor.
        It then eventualy filters the queryset using the provided filter_class, and data.uri_param
        Finally, returns the serialized data using serializer_class
    """
    @global_entry(name=action_name)
    def entry(user, data):
        queryset = queryset_class(user, data)
        if filter_class != None:
            filter = filter_class(queryset=queryset, data=data.uri_param)
            queryset = filter.qs()
        serializer = serializer_class(queryset, many=True)
        return response.Response(response.Success_Retrieved, serializer.data)
        
    return entry
    
    
def create(serializer_class, action_name="create"):
    """
        This method is an entry that create a new ressource.
        It deserialize the data using the provided serializer_class,
        Then check for permissions, and save the object in the database
    """
    @global_entry(name=action_name, methods=["post"])
    def entry(user, data):
        serializer, instance = shortcuts.get_deserialized(serializer_class, data)
        shortcuts.check_permission(user, instance, action_name)
        instance.save()
        return response.Response(response.Success_Created, serializer_class(instance).data)
    
    return entry
    
    
def update(serializer_class, action_name="update"):
    """
        This method is used to perform (potentially partial) updates.
        It first gets a model instance out of the de-serialized data. 
        Then, we try to get the real instance, using the pk.
        We check permissions giving both the to-be-updated, and the original instances.
        If true, we merge them, save the result, and returns the new object serialized
    """
    @detailed_entry(name=action_name, methods=["post"])
    def entry(user, data, pk):
        serializer, instance = shortcuts.get_deserialized(serializer_class, data)
        real_instance = shortcuts.get_or_raise(serializer_class.Meta.model.objects.all(), pk)
        shortcuts.check_permission(user, real_instance, action_name, instance)
        
        resp_serializer, new_instance = shortcuts.get_deserialized(serializer_class, real_instance, instance)
        resp_serializer.save()
        return response.Response(response.Success_Updated, resp_serializer.data)
    
    return entry
    
def destroy(queryset_class, serializer_class, action_name="destroy"):
    """
        This method is an entry that create a new ressource.
        It deserialize the data using the provided serializer_class,
        Then check for permissions, and save the object in the database
    """
    @global_entry(name=action_name, methods=["post"])
    def entry(user, data):
        queryset = queryset_class(user, data)
        instance = shortcuts.get_or_raise(queryset_class, pk)
        shortcuts.check_permission(user, instance, action_name)
        instance.delete()
        return response.Response(response.Success_Deleted)
    
    return entry
