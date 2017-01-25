from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
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
        return self.handle_action_pk('retrieve', request, pk)

    @list_route(methods=['get'])
    def events(self, request):
        n = 5
        if 'n' in request.data:
            n = request.data.n
        return SigmaViewSet.serialized_response(Event.serializer, Event.model.n_events(request.user, n))

    @list_route(methods=['get'])
    def events_interesting(self, request):
        n = 5
        if 'n' in request.data:
            n = request.data.n
        return SigmaViewSet.serialized_response(Event.serializer, Event.model.n_events_interesting(request.user, n))

    @list_route(methods=['get'])
    def date_events(self, request):
        print(request.data)
        if ('start' in request.data and 'end' in request.data):
            start = request.data.start
            end = request.data.end
            return SigmaViewSet.serialized_response(Event.serializer, Event.model.events_date(request.user, start, end))

    @list_route(methods=['get'])
    def date_events_interesting(self, request):
        if ('start' in request.data and 'end' in request.data):
            start = request.data.start
            end = request.data.end
            return SigmaViewSet.serialized_response(Event.serializer, Event.model.events_interesting_date(request.user, start, end))

    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    def create(self, request):
        return self.handle_action('create', request)
