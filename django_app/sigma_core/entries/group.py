from sigma_api import entries, response
from sigma_api.importer import load_ressource

Group = load_ressource("Group")
GroupMember = load_ressource("GroupMember")
GroupInvitation = load_ressource("GroupInvitation")

class GroupEntrySet(entries.EntrySet):


    list = entries.list(
        Group.objects.user_can_see,
        Group.serializers.list
    )

    members = entries.sub_list(
        action_name = "members",
        sub_queryset = GroupMember.objects.user_can_see,
        serializer = GroupMember.serializer
    )

    retrieve = entries.retrieve()

    invitations = entries.sub_list(
        action_name = "invitations",
        sub_queryset = GroupInvitation.objects.get_group_invitations_pending,
        serializer = GroupInvitation.serializer
    )


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
