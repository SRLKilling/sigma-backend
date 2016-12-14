from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response

from sigma_core.views.sigma_viewset import SigmaViewSet

from sigma_core.models.group_member import GroupMember
from sigma_core.serializers.group_member import GroupMemberSerializer

class GroupMemberViewSet(SigmaViewSet):

    serializer_class = GroupMemberSerializer
    queryset = GroupMember.objects.all()

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    def list(self, request):
        """
            REST list action. Used to list all of a user's membership.
        """
        return self.handle_action_list(request, GroupMember.get_user_memberships_qs)


    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve a membership.
        """
        return self.handle_action_pk('retrieve', request, pk)




    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    @staticmethod
    def create(user, group, sa = False):
        """
            Create a membership based on the given user an group.
            This static method is not an API entry. It is used by others view :
            * InvitationView create members once an invitation is accepted
            * GroupView create super admin right after creating a group
        """
        member = GroupMember(user=user, group=group)
        if sa:
            member.is_super_administrator = True
            member.is_administrator = True
        member.save()
        UserConnectionViewSet.create_new_connections_gr(user,group)
        serializer = GroupMemberSerializer(member)
        return serializer.data


    @detail_route(methods=['patch'])
    def change_rights(self, request, pk):
        """
            Used to change a member's rights.
            Only administrators can change member's rights.
            Only super-administrator can change admin's rights.
            If the super-administrator right is requested, then it must come from the current
            super-administrator whose thus, losing his status.

            If succeeded, returns HTTP_200_OK with the updated GroupMember object
        """
        user = request.user
        member = self.get_or_404(pk)
        rights_serializer, rights = self.get_deserialized(GroupMemberRightsSerializer, request.data)

        if not GroupMember.can_change_rights(user, member, rights):
            raise PermissionDenied()

        if rights.is_super_administrator:
            pass                                                                                                # TODO : de-superadminer le gars qui file ses droits

        member_serializer, member = self.get_deserialized(GroupMember, rights, member, partial=True)
        member_serializer.save()
        return Response(member_serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, pk):
        """
            REST destroy action. Used to kick a member.
            If succeeded, returns HTTP_204_NO_CONTENT.
        """

        group_member = self.get_deserialized(GroupMemberSerializer, request.data)
        UserConnectionViewSet.destroy_gr(group_member.user,group_member.group)
        return self.handle_action_pk('destroy', request, pk)
