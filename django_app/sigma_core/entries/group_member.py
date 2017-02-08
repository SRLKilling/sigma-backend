from sigma_api import entries, response
from sigma_api.importer import load_ressource

GroupMember = load_ressource("GroupMember")

class GroupMemberEntrySet(entries.EntrySet):
    
    list = entries.list(
        queryset = GroupMember.objects.for_user
    )
    
    retrieve = entries.retrieve(
        serializer = GroupMember.serializers.retrieve
    )
    
    update = entries.update()
    
    destroy = entries.destroy()