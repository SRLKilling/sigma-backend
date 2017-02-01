from sigma_api import entries
from sigma_api.importer import load_ressource

Group = load_ressource("Group")

class GroupEntrySet(entries.EntrySet):
    
    list = entries.list(
        lambda user, data: Group.objects,
        Group.serializers.list
    )
    
    # members = entries.colist(
        # GroupMembers.objects
    # )
    
    retrieve = entries.retrieve(
        lambda user, data : Group.objects,
        Group.serializers.default
    )
    
    update_right = entries.update(
        Group.serializers.default,
        'update_right'
    )