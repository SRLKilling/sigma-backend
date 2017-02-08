from sigma_api import entries, response
from sigma_api.importer import load_ressource

GroupMember = load_ressource("GroupMember")

class GroupMemberEntrySet(entries.EntrySet):

    create = entries.create(
        GroupMember.serializers.default
    )

    list = entries.list(
        GroupMember.objects.for_user,
        GroupMember.serializers.default
    )

    retrieve = entries.retrieve()

    update = entries.update()

    destroy = entries.destroy()
