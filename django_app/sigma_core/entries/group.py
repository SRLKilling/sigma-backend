from sigma_api import entries, response
from sigma_api.importer import load_ressource

Group = load_ressource("Group")

class GroupEntrySet(entries.EntrySet):
    
    list = entries.list(
        Group.objects.user_can_see,
        Group.serializers.list
    )
    
    retrieve = entries.retrieve(
        Group.objects,
        Group.serializers.default
    )
    
    create = entries.create(
        Group.serializers.default
    )
    
    # update_right = entries.update(
        # Group.serializers.default,
        # 'update_right'
    # )
    
    destroy = entries.destroy(
        Group.objects
    )