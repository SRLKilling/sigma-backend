from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.views.sigma_viewset import SigmaViewSet
from sigma_core.importer import load_ressource

Event = load_ressource("Event")

class EventViewSet(SigmaViewSet):

    serializer_class = Event.serializer
    queryset = Event.model.objects.all()

    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    def list(self, request):
        return self.handle_action_list(request, Event.model.get_events)

    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve a chat.
        """
        return self.handle_action_pk('retrieve', request, pk)

    @detail_route(methods=['get'])
    def events(self, request):
        n = 5
        if (request.data.has_key('n')):
            n = request.data.n
        return serialized_response(Event.serializer, Event.model.n_events(request.user, n))

    @detail_route(methods=['get'])
    def events_interesting(self, request):
        n = 5
        if (request.data.has_key('n')):
            n = request.data.n
        return serialized_response(Event.serializer, Event.model.n_events_interesting(request.user, n))

    @detail_route(methods=['get'])
    def date_events(self, request, start, end):
        if (request.data.has_key('start') and request.data.has_key('end')):
            start = request.data.start
            end = request.data.end
            return serialized_response(Event.serializer, Event.model.events_date(request.user, start, end))

    @detail_route(methods=['get'])
    def date_events_interesting(self, request, start, end):
        if (request.data.has_key('start') and request.data.has_key('end')):
            start = request.data.start
            end = request.data.end
            return serialized_response(Event.serializer, Event.model.events_interesting_date(request.user, start, end))

    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    def create(self, request):
        """
            REST create action. Used to create a chat.
            If succeeded, returns HTTP_201_CREATED with the corresponding Chat.
        """
        return self.handle_action('create', request)
