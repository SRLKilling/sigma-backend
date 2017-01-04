from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.importer import Sigma, load_ressource
from sigma_core.views.sigma_viewset import SigmaViewSet

load_ressource("Group")
load_ressource("GroupMember")
load_ressource("AcknowledgmentInvitation")

class GroupViewSet(SigmaViewSet):

    serializer_class = Sigma.Group.serializer
    queryset = Sigma.Group.model.objects.all()

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    def list(self, request):
        """
            REST list action. Used to list all groups a user can see.
        """
        return self.handle_action_list(request, Sigma.Group.model.get_user_groups_qs)


    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve a group.
        """
        return self.handle_action_pk('retrieve', request, pk)

        
        
        
    @detail_route(methods=['get'])
    def acknowledged(self, request, pk):
        """
            Used to list all the groups that are acknowledged by a group.
        """
        return self.handle_action_list(request, Sigma.Group.model.get_acknowledged_by_qs, pk)
        
    @detail_route(methods=['get'])
    def acknowledged_by(self, request, pk):
        """
            Used to list all the groups that are acknowledging the given group.
        """
        return self.handle_action_list(request, Sigma.Group.model.get_acknowledging_qs, pk)

        
    @detail_route(methods=['get'])
    def acknowledge_invitations(self, request, pk):
        """
            Used to retrieve a list of acknowledgment invitation a group is part of.
            It can be both invited or inviter
        """
        return SigmaViewSet.handle_action_list(Sigma.AcknowledgmentInvitation.serializer, request, Sigma.AcknowledgmentInvitation.model.get_invitations_qs, pk)
        
    @detail_route(methods=['get'])
    def members(self, request, pk):
        """
            Used to retrieve a list of acknowledgment invitation a group is part of.
            It can be both invited or inviter
        """
        return self.handle_action_pk_list(Sigma.GroupMember.serializer, request, pk, Sigma.GroupMember.model.get_scoped_group_members_qs)
        

    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    def create(self, request):
        """
            REST create action. Used to create an group.
            If succeeded, returns HTTP_201_CREATED with the corresponding Group object.
        """
        return self.handle_action('create', request)

    def create_post_handler(self, request, group_serializer, group):
        # Once a group is created, we need to create a membership for the creator (automaticly becoming the super admin)
        GroupMember.create(request.user, group, True)




    def destroy(self, request, pk):
        """
            REST destroy action. Used to decline or cancel an invitation.
            If succeeded, returns HTTP_204_NO_CONTENT.
        """
        return self.handle_action_pk('destroy', request, pk)
