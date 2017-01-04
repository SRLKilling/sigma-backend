from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response

from sigma_core.views.sigma_viewset import SigmaViewSet
from sigma_core.importer import Sigma, load_ressource

GroupMember = load_ressource("GroupMember")
UserConnection = load_ressource("UserConnection")


class GroupMemberViewSet(SigmaViewSet):

    serializer_class = GroupMember.serializer
    queryset = GroupMember.model.objects.all()

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    def list(self, request):
        """
            REST list action. Used to list all of a user's membership.
        """
        return self.handle_action_list(request, GroupMember.model.get_user_memberships_qs)


    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve a membership.
        """
        return self.handle_action_pk('retrieve', request, pk)


    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#


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
        rights_serializer, rights = SigmaViewSet.get_deserialized(GroupMemberRightsSerializer, request.data)

        if not GroupMember.model.can_change_rights(user, member, rights):
            raise PermissionDenied()

        if rights.is_super_administrator:
            pass                                                                                                # TODO : de-superadminer le gars qui file ses droits

        member_serializer, member = self.get_deserialized(rights, member, partial=True)
        member_serializer.save()
        return Response(member_serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, pk):
        """
            REST destroy action. Used to kick a member.
            If succeeded, returns HTTP_204_NO_CONTENT.
        """

        group_member = self.get_deserialized(request.data)
        UserConnection.model.destroy_gr(group_member.user,group_member.group)
        return self.handle_action_pk('destroy', request, pk)
