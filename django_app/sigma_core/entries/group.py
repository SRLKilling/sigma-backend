from sigma_api import entries, response, shortcuts
from sigma_api.importer import load_ressource

Group = load_ressource("Group")
GroupMember = load_ressource("GroupMember")
GroupInvitation = load_ressource("GroupInvitation")
Publication = load_ressource("Publication")
Chat = load_ressource("Chat")
ChatMember = load_ressource("ChatMember")
User = load_ressource("User")

class GroupEntrySet(entries.EntrySet):


    list = entries.list(
        Group.objects.user_can_see,
        Group.serializers.list
    )

    retrieve = entries.retrieve()

    members = entries.sub_list(
        sub_queryset = GroupMember.objects.user_can_see,
        serializer = GroupMember.serializer
    )

    publications = entries.sub_list(
        sub_queryset = lambda user, group: Publication.objects.in_group(group).sort(),
        serializer = Publication.serializer
    )

    invitations = entries.sub_list(
        sub_queryset = GroupInvitation.objects.get_group_invitations_pending,
        serializer = GroupInvitation.serializer
    )

    @entries.global_entry(bind_set=True, methods=["post"])
    def create(self, user, data):
        ''' modified to put the creator as a superadmin'''
        #Can we access easily data.group without deserializing?
        s=shortcuts.create(user, data, self.get_serializer(None), "create")
        g = Group.objects.latest("pk")
        GroupMember.model.create_admin(user, g)
        Chat.model.create_chat(g)
        ChatMember.model.add_new_member(user,g)
        return s

    update = entries.update(Group.serializer.update)

    destroy = entries.destroy()

    my_groups = entries.list(
        queryset = Group.objects.user_is_member,
        serializer = Group.serializer.list
    )
