from sigma_api import entries, response
from sigma_api.importer import load_ressource

GroupField = load_ressource("GroupField")

class GroupFieldEntrySet(entries.EntrySet):
    
    create = entries.create()
    
    retrieve = entries.retrieve()
    
    update = entries.update()
    
    destroy = entries.destroy()