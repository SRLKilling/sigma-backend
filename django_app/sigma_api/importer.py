import re
from importlib import import_module

# Transform CamelCase name to an underscored file name
def camelToFilename(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()




# Represent a ressource. You can use it to load and access model/serializer/view easily
class Ressource:
    MODEL = 0
    SERIALIZERS = 1
    ENTRIES = 2

    PACKAGE_PATH = "sigma_core"

    def __init__(self, name):
        self.name = name
        self.mods = [None, None, None]
        self.paths = ["models", "serializers", "entries"]
        self.suffixes = ["", "SerializerSet", "EntrySet"]

    def get(self, type):
        if self.mods[type] == None:
            self.mods[type] = import_module(Ressource.PACKAGE_PATH + "." + self.paths[type] + "." + camelToFilename(self.name))
            getattr(self.mods[type], self.name + self.suffixes[type]).ressource = self

        return getattr(self.mods[type], self.name + self.suffixes[type])

    @property
    def model(self):
        return self.get(Ressource.MODEL)

    @property
    def objects(self):
        return self.get(Ressource.MODEL).objects

    @property
    def serializers(self):
        return self.get(Ressource.SERIALIZERS)

    @property
    def serializer(self):
        return self.get(Ressource.SERIALIZERS).default

    @property
    def entries(self):
        return self.get(Ressource.ENTRIES)


Ressources = {}

# Create a ressource and optionnaly pre-import its model/serializer/view
def load_ressource(name):
    if not name in Ressources:
        res = Ressource(name)
        Ressources[name] = res
    else:
        res = Ressources[name]

    return res

def register_model(res_name):
    load_ressource(res_name).model
def register_entry(res_name, base_name):
    Res = load_ressource(res_name)
    Res.entries.register(base_name)
    Res.model
