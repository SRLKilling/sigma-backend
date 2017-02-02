from rest_framework import serializers
drf = serializers


def sub(cls):
    """ Mark a class as a sub-serializer """
    cls.__sub_serializer = True
    return cls


def set(cls):
    """
        Create a serializer set.
        Search for its sub-serializers, make them inherit the serializer_set.
        And make sub-meta inherits the set's meta.
    """
    
    def inherit_meta(attribs):
        if not hasattr(cls, "Meta"):
            return
        for n in attribs:
            if isinstance(attribs[n], type) and attribs[n].__name__ == "Meta":
                name = "Meta"
                bases = ((getattr(cls, "Meta"),) + attribs[n].__bases__) if (not getattr(cls, "Meta") in attribs[n].__bases__) else (attribs[n].__bases__)
                metaattribs = dict(attribs[n].__dict__)
                
                attribs[n] = type(name, bases, metaattribs)
    
    def inherited_sub(sub):
        name = sub.__name__
        bases = ((cls, ) + sub.__bases__) if (not cls in sub.__bases__) else (sub.__bases__)
        attribs = dict(sub.__dict__)
        inherit_meta(attribs)
                
        return type(name, bases, attribs)
    
    for n in cls.__dict__:
        sub = cls.__dict__[n]
        if isinstance(sub, type) and hasattr(sub, "__sub_serializer"):
            setattr(cls, n, inherited_sub(sub))
            
    setattr(cls, "default", cls)
    return cls
    
    
class SerializerSet():
    pass