from sigma_api import entries, response,shortcuts
from sigma_api.importer import load_ressource

GroupInvitation = load_ressource("GroupInvitation")
GroupMember = load_ressource("GroupMember")

class GroupInvitationEntrySet(entries.EntrySet):

    retrieve = entries.retrieve()
    
    @entries.global_entry(methods=["post"])
    def create(user, data):
        serializer = shortcuts.get_validated_serializer(GroupInvitation.serializer, data=data)
        instance = GroupInvitation.model(**serializer.validated_data)
        shortcuts.check_permission(user, instance, "create")
        if instance.user==user:
            if not instance.group.need_validation_to_join:
                new_instance=GroupMember.model(user=user,group=instance.group)
                new_instance.save()
                return response.Response(response.Success_Created, GroupMember.serializer(new_instance).data)
        instance.save()
        return response.Response(response.Success_Created, GroupInvitation.serializer(instance).data)

    list = entries.list(GroupInvitation.objects.get_user_invitations,GroupInvitation.serializer)

    destroy = entries.destroy()

    @entries.global_entry(methods=["get"])
    def accept(user, data, pk):
        invit = GroupInvitation.objects.get(pk=pk)
        new_instance=GroupMember.model(user=invit.invitee,group=invit.group)
        new_instance.save()
        return response.Response(response.Success_Created, GroupMember.serializer(new_instance).data)
