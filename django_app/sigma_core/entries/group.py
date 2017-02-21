from sigma_api import entries, response
from sigma_api.importer import load_ressource

Group = load_ressource("Group")
GroupMember = load_ressource("GroupMember")

class GroupEntrySet(entries.EntrySet):

    list = entries.list(
        Group.objects.user_can_see,
        Group.serializers.list
    )

    retrieve = entries.retrieve()

    create = entries.create()

    @entries.global_entry(bind_set=True, methods=["post"])
    def create(self, user, data):
        ''' modified to put the creator as an superadmin'''
        #Can we access easily data.group without deserializing?
        serializer = shortcuts.get_validated_serializer(Group.serializer, data=data)
        group = Group.model(**serializer.validated_data)
        GroupMember.models.create_admin(user, group)
        Chat.models.create_chat(user,group)
        ChatMember.models.add_new_member(user,group)
        return shortcuts.create(user, data, self.get_serializer(None), "create")

    # update_right = entries.update(
        # Group.serializers.default,
        # 'update_right'
    # )

    destroy = entries.destroy()
