from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.views.sigma_viewset import SigmaViewSet
from sigma_core.importer import load_ressource

Publication = load_ressource("Publication")
SharedPublication = load_ressource("SharedPublication")
Group = load_ressource("Group")

class SharedPublicationViewSet(SigmaViewSet):

    serializer_class = SharedPublication.serializer
    queryset = SharedPublication.model.objects.all()

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    def list(self, request):
        return self.handle_action_list(request, SharedPublication.model.get_publications_user)

    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve a chat.
        """
        return self.handle_action_pk('retrieve', request, pk)

    @detail_route(methods=['get'])
    def list_publications_group(self, request, pk):
        """
            REST list action. Used to list the chat members of a chat that contains the user.
        """
        return serialized_response(SharedPublication.serializer, SharedPublication.model.get_publications_group(Group.model.objects.get(pk=pk)))

    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    def create(self, request):
        """
            REST create action. Used to create a chat.
            If succeeded, returns HTTP_201_CREATED with the corresponding Chat.
        """
        return self.handle_action('create', request)

#    def create_post_handler(self, request, chat_serializer, chat):
#        # Once a chat is created, we need to create a membership for the creator
#        # ChatMember.view.(chat=char,user=request.user).save()
#        # WTF is this line ?
#        pass
