from sigma_api import response, shortcuts

#*********************************************************************************************#

entries = {}

class EntryException(Exception):
    pass

class InvalidLocEntryException(EntryException):
    pass

class InvalidActionEntryException(EntryException):
    pass

def route_to_entry(loc, action):
    if not route_to_entry.__registered:
        import register_list
        route_to_entry.__registered = True

    if not loc in entries:
        raise InvalidLocEntryException()

    entryset = entries[loc]
    if not hasattr(entryset, action):
        raise InvalidActionEntryException()

    return getattr(entryset, action)

route_to_entry.__registered = False

#*********************************************************************************************#

class Entry(object):
    """ This class wraps an entry function """

    def __init__(self, name, func, detailed, bind_set = False, **kwargs):
        self.name = name
        self.func = func
        self.detailed = detailed
        self.bind_set = bind_set
        self.kwargs = kwargs

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        self.set = klass
        return self

    def __call__(self, *args, **kwargs):
        if self.bind_set:
            return self.func(self, *args, **kwargs)
        else:
            return self.func(*args, **kwargs)


#*********************************************************************************************#


def global_entry(name = None, **kwargs):
    """ This is the decorator used to generate global entries (i.e. not bound to a specific ressource) """
    def decorator(func):
        # n = (name) if (name != None) else (func.__name__)
        return Entry(name, func, False, **kwargs)
    return decorator

def detailed_entry(name = None, **kwargs):
    """ Generate a detailed entry (i.e. with a pk) """
    def decorator(func):
        # n = (name) if (name != None) else (func.__name__)
        return Entry(name, func, True, **kwargs)
    return decorator

#*********************************************************************************************#

def retrieve(queryset=None, serializer=None, action_name=None):
    @detailed_entry(name=action_name, bind_set=True)
    def entry(entry, user, data, pk):
        return shortcuts.retrieve(user, data, pk, entry.set.get_queryset(queryset), entry.set.get_serializer(serializer), entry.name)
    return entry

def list(queryset=None, serializer=None, filter_class = None, action_name=None):
    @global_entry(name=action_name, bind_set=True)
    def entry(entry, user, data):
        return shortcuts.list(user, data, entry.set.get_queryset(queryset), entry.set.get_serializer(serializer))
    return entry

def sub_list(res_queryset=None, sub_queryset=None, serializer=None, filter_class = None, action_name = None):
    @detailed_entry(name=action_name, bind_set=True)
    def entry(entry, user, data, pk):
        return shortcuts.sub_list(user, data, pk, entry.set.get_queryset(res_queryset), entry.set.get_queryset(sub_queryset), entry.set.get_serializer(serializer))
    return entry

def create(serializer=None, action_name=None):
    @global_entry(name=action_name, bind_set=True, methods=["post"])
    def entry(entry, user, data):
        return shortcuts.create(user, data, entry.set.get_serializer(serializer), entry.name)
    return entry

def update(serializer=None, action_name=None):
    @detailed_entry(name=action_name, bind_set=True, methods=["post"])
    def entry(entry, user, data, pk):
        return shortcuts.update(user, data, pk, entry.set.get_serializer(serializer), entry.name)
    return entry

def destroy(queryset=None, action_name=None):
    @detailed_entry(name=action_name, bind_set=True, methods=["post"])
    def entry(entry, user, data, pk):
        return shortcuts.destroy(user, data, pk, entry.set.get_queryset(queryset), entry.name)
    return entry

#*********************************************************************************************#

class EntrySet():
    """ This class wraps a set of entries and provide a way to turn it to a DRF Viewset """

    @classmethod
    def entries(cls):
        if not hasattr(cls, "_entries"):
            cls._entries = []
            for fn in cls.__dict__:
                if not hasattr(cls, fn):
                    continue
                f = getattr(cls, fn)
                if isinstance(f, Entry):
                    if f.name == None:
                        f.name = fn
                    cls._entries.append((fn, f))

        return cls._entries

    @classmethod
    def register(cls, name):
        entries[name] = cls

    @classmethod
    def get_queryset(cls, qs = None):
        if qs != None:
            return qs
        if hasattr(cls, "default_queryset"):
            return cls.default_queryset
        elif hasattr(cls, "ressource"):
            return cls.ressource.model.objects
        else:
            raise ValueError("Cannot automatically retrieve entryset queryset, must specify 'default_queryset', or 'ressource' class attribute")

    @classmethod
    def get_serializer(cls, ser = None):
        if ser != None:
            return ser
        if hasattr(cls, "default_serializer"):
            return cls.default_serializer
        elif hasattr(cls, "ressource"):
            return cls.ressource.serializers.default
        else:
            raise ValueError("Cannot automatically retrieve entryset serializer, must specify 'default_serializer', or 'ressource' class attribute")
