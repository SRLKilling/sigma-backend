from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from sigma_core.views.sigma_viewset import SigmaViewSet

from sigma_core.models.acknowledgment_invitation import AcknowledgmentInvitation
from sigma_core.serializers.acknowledgment_invitation import AcknowledgmentInvitationSerializer


from sigma_core.models.acknowledgment import Acknowledgment

class AcknowledgmentInvitationViewSet(SigmaViewSet):
    
    serializer_class = AcknowledgmentInvitationSerializer
    queryset = AcknowledgmentInvitation.objects.all()
    
    
    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#
        
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
        if Acknowledgment.is_acknowledged_by(invitation.acknowledged, invitation.acknowledged_by):
            raise ValidationError("The group is already acknowledged.")
            
        elif AcknowledgmentInvitation.is_invited(invitation.acknowledged, invitation.acknowledged_by):
            raise ValidationError("The group is already invited to be acknowledged")
        
        
        
    
    @detail_route(methods=['post'])
    def accept(self, request, pk):
        """
            Used to accept an invitation.
            If succeeded, returns HTTP_201_CREATED with the corresponding Acknowledgment object
        """
        return self.handle_action_pk('accept', request, pk)
        
        
    def accept_handler(self, request, pk, instance):
        data = Acknowledgment.create(instance.aknowledged, instance.acknowledged_by)
        instance.delete()
        return SigmaViewSet.serialized_response(AcknowledgmentSerializer, data, status.HTTP_201_CREATED)
        
        
        
        
    def destroy(self, request, pk):
        """
            REST destroy action. Used to decline or cancel an invitation.
            If succeeded, returns HTTP_204_NO_CONTENT.
        """
        
        return self.handle_action_pk('destroy', request, pk)
        