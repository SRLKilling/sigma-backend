from sigma_api import entries, response
from sigma_api.importer import load_ressource

GroupField = load_ressource("GroupField")

class GroupFieldEntrySet(entries.EntrySet):
    
    create = entries.create(
        GroupField.serializer
    )
    
    retrieve = entries.retrieve(
        GroupField.objects,
        GroupField.serializer
    )
    
    update = entries.update(
        GroupField.serializer
    )
    
    destroy = entries.destroy(
        GroupField.objects
    )