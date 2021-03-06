from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from sigma_core.views.sigma_viewset import SigmaViewSet
from sigma_core.importer import Sigma, load_ressource

GroupInvitation = load_ressource("GroupInvitation")
GroupMember = load_ressource("GroupMember")


class GroupInvitationViewSet(SigmaViewSet):
    
    serializer_class = GroupInvitation.serializer
    queryset = GroupInvitation.model.objects.all()
    
    
    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#
    
    def list(self, request):
        """
            REST list action. Used to list all of a user's invitation.
        """
        return self.handle_action_list(request, GroupInvitation.model.get_user_invitations_qs)

        
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
        if GroupMember.model.is_member(invitation.group, invitation.invitee):
            raise ValidationError("The user is already a member of this group")
            
        elif GroupInvitation.model.objects.filter(invitee = invitation.invitee, group = invitation.group).exists():
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
        return self.handle_action_pk('accept', request, pk)
        
        
    def accept_handler(self, request, pk, instance):
        data = GroupMember.model.create(invitation.invitee, invitation.group)
        instance.delete()
        return SigmaViewSet.serialized_response(GroupMember.serializer, data, status.HTTP_201_CREATED)
        
        
        
    def destroy(self, request, pk):
        """
            REST destroy action. Used to decline or cancel an invitation.
            If succeeded, returns HTTP_204_NO_CONTENT.
        """
        
        return self.handle_action_pk('destroy', request, pk)
        