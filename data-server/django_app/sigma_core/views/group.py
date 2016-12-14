from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.views.sigma_viewset import SigmaViewSet

from sigma_core.models.group import Group
from sigma_core.serializers.group import GroupSerializer


from sigma_core.models.group_member import GroupMember

class GroupViewSet(SigmaViewSet):

    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    def list(self, request):
        """
            REST list action. Used to list all groups a user can see.
        """
        return self.handle_action_list(request, Group.get_user_groups_qs)


    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve a group.
        """
        return self.handle_action_pk('retrieve', request, pk)

    @detail_route(methods=['get'])
    def acknowledged_groups(self,request,pk):
        return GroupSerializer(GroupAcknowledgment.objects.filter(acknowledged_by=group).values('acknowledged'), many=True)


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
        return self.handle_action_pk('destroy', request, pk)                                                                          # TODO : check that CASCADE destroy stuff are enabled ?
