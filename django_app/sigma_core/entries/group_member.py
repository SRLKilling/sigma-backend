from sigma_api import entries, response, shortcuts
from sigma_api.importer import load_ressource

GroupMember = load_ressource("GroupMember")
UserConnection = load_ressource("UserConnection")

class GroupMemberEntrySet(entries.EntrySet):

    # @entries.global_entry(bind_set=True, methods=["post"])
    # def create(self, user, data):
    #     ''' modified to handle UserConnection'''
    #     #Can we access easily data.group without deserializing?
    #     serializer = shortcuts.get_validated_serializer(GroupMember.serializer, data=data)
    #     my_group = GroupMember.model(**serializer.validated_data).group
    #     UserConnection.model.create_new_connections_gr(user, my_group)
    #     return shortcuts.create(user, data, self.get_serializer(None), "create")

    #no need for create : Group Members are only created via the group_invitation entries

    list = entries.list(
        GroupMember.objects.for_user,
        GroupMember.serializers.default
    )

    retrieve = entries.retrieve()

    update = entries.update()

    destroy = entries.destroy()

    # @entries.detailed_entry(bind_set=True, methods=["post"])
    # def destroy(self, user, data, pk):
    #     '''modified to handle UserConnection'''
    #     instance = GroupMember.objects.get(pk=pk)
    #     shortcuts.check_permission(user, instance, "destroy")
    #     #UserConnection.destroy_gr(instance.user, instance.group)
    #     instance.delete()
    #     return response.Response(response.Success_Deleted)
