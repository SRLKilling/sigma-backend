import re
from importlib import import_module

# Transform CamelCase name to an underscored file name
def camelToFilename(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    
    
    
# Represent a ressource. You can use it to load and access model/serializer/view easily
class Ressource:
    MODEL = 0
    SERIALIZER = 1
    VIEW = 2
    
    PACKAGE_PATH = "sigma_core"

    def __init__(self, name):
        self.name = name
        self.mods = [None, None, None]
        self.paths = ["models", "serializers", "views"]
        self.suffixes = ["", "Serializer", "ViewSet"]
    
    def get(self, type):
        if self.mods[type] == None:
            self.mods[type] = import_module(Ressource.PACKAGE_PATH + "." + self.paths[type] + "." + camelToFilename(self.name))
            
        return getattr(self.mods[type], self.name + self.suffixes[type])
        
    @property
    def model(self):
        return self.get(Ressource.MODEL)
        
    @property
    def serializer(self):
        return self.get(Ressource.SERIALIZER)
        
    @property
    def view(self):
        return self.get(Ressource.VIEW)
    

Sigma = type('Sigma', (), {})()

# Create a ressource and optionnaly pre-import its model/serializer/view
def load_ressource(name):
    r = Ressource(name)
    setattr(Sigma, name, r)        
    return r