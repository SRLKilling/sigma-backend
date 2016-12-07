from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.view.sigma_viewset import SigmaViewSet

from sigma_core.models.group import Group
from sigma_core.serializers.group import GroupSerializer


from sigma_core.views.group_member import GroupMemberView

class GroupViewSet(SigmaViewSet):

    model_class = Group
    serializer_class = GroupSerializer

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#
    
    def list(self, request):
        """
            REST list action. Used to list all groups a user can see.
        """
        # qs = GroupInvitation.get_user_invitations_qs(request.user)
        # return self.serialized_response(qs)
        pass

        
    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve a group.
        """
        return self.basic_retrieve(request, pk)
    
    
    
    
    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    def create(self, request):
        """
            REST create action. Used to create an group.
            If succeeded, returns HTTP_201_CREATED with the corresponding Group object.
        """
        return self.basic_create(request)
        
    
    def create_post(self, request, group_serializer, group):
        # Once a group is created, we need to create a membership for the creator (automaticly becoming the super admin)
        GroupMemberView.create(request.user, group, True)
    
    
        
        
    def destroy(self, request, pk):
        """
            REST destroy action. Used to decline or cancel an invitation.
            If succeeded, returns HTTP_204_NO_CONTENT.
        """
        return self.basic_destroy(request, pk)                                                                          # TODO : check that CASCADE destroy stuff are enabled ?
        