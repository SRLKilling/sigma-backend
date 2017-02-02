class _SerializerRepr:
    def __init__(self, cls):
        self.name = cls.__name__
        self.bases = cls.__bases__
        self.attribs = dict(cls.__dict__)
        
def sub(cls):
    return _SerializerRepr(cls)

def base_set(cls):    
    def inherit_meta(attribs):
        if not hasattr(cls, "Meta"):
            return
        for n in attribs:
            if isinstance(attribs[n], type) and attribs[n].__name__ == "Meta":
                name = "Meta"
                bases = (getattr(cls, "Meta"),) + attribs[n].__bases__
                metaattribs = dict(attribs[n].__dict__)
                
                attribs[n] = type(name, bases, metaattribs)
    
    def inherited_sub(sub):
        name = sub.name
        bases = (cls, ) + sub.bases
        attribs = sub.attribs
        inherit_meta(attribs)
                
        return type(name, bases, attribs)
    
    for n in cls.__dict__:
        if isinstance(cls.__dict__[n], _SerializerRepr):
            setattr(cls, n, inherited_sub(cls.__dict__[n]))
            
    return cls
            
        

@base_set
class GroupSerializerSet():
    class Meta:
        model = "Toto"
    
#*********************************************************************************************#

    @sub
    class default():
        class Meta:
            fields = ('pk', 'name', 'description', 'is_protected', 'can_anyone_ask', 'need_validation_to_join', 'members_visibility', 'group_visibility', 'fields')
        test = ""
        
    class list():
        class Meta:
            fields = ('pk', 'name', 'description', 'fields')
            
            
print(GroupSerializerSet)
print(GroupSerializerSet.default)
print(GroupSerializerSet.default.Meta.model)