from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from sigma_core.views.sigma_viewset import SigmaViewSet

from sigma_core.models.group_invitation import GroupInvitation
from sigma_core.serializers.group_invitation import GroupInvitationSerializer


from sigma_core.models.group_member import GroupMember
from sigma_core.views.group_member import GroupMemberViewSet

class GroupInvitationViewSet(SigmaViewSet):
    
    serializer_class = GroupInvitationSerializer
    queryset = GroupInvitation.objects.all()
    
    
    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#
    
    def list(self, request):
        """
            REST list action. Used to list all of a user's invitation.
        """
        return self.handle_action_list(request,GroupInvitation.get_user_invitations_qs)

        
    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve an invitation.
        """
        return self.handle_action_pk('retrieve', request, pk)
    
    
    
    
    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    def create(self, request):
        """
            REST create action. Used to create an invitation.
            If succeeded, returns HTTP_201_CREATED with either the corresponding Invitation object,
            or the GroupMember object if invitation is not needed.
            The invitee must not be already invited or member.
        """
        return self.handle_action('create', request)
            
            
    def create_pre_handler(self, request, invitation_serializer, invitation):
        if GroupMember.is_member(invitation.group, invitation.invitee):
            raise ValidationError("The user is already a member of this group")
            
        elif GroupInvitation.objects.filter(invitee = invitation.invitee, group = invitation.group).exists():
            raise ValidationError("The user is already invited to this group")
        
        elif not invitation.group.need_validation_to_join:
            data = GroupMemberViewSet.create(invitation.invitee, invitation.group)
            return Response(data, status=status.HTTP_201_CREATED)
        
        
        
    
    @detail_route(methods=['post'])
    def accept(self, request, pk):
        """
            Used to accept an invitation.
            If succeeded, returns HTTP_201_CREATED with the corresponding GroupMember object
        """
        invitation = self.get_or_404(pk)
            
        if not invitation.can_accept(request.user):
            raise PermissionDenied()
        
        data = GroupMemberViewSet.create(invitation.invitee, invitation.group)
        invitation.delete()
        return Response(data, status=status.HTTP_201_CREATED)
        
        
    def destroy(self, request, pk):
        """
            REST destroy action. Used to decline or cancel an invitation.
            If succeeded, returns HTTP_204_NO_CONTENT.
        """
        
        return self.handle_action_pk('destroy', request, pk)
        