from django.db.models.query import QuerySet
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response


from push_app.notify import notify

class SigmaViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    #*********************************************************************************************#
    #**                                    Useful methods                                       **#
    #*********************************************************************************************#

    def try_to_get(obj, pk):
        """
            This method can be used to get a model instance based on it's primary key.
            If the instance does not exists, it will automatically throws a 404 error.

            Method version : uses the queryset provided in the subclass definition
            Static version : takes the queryset to use as its first argument.
        """
        if isinstance(obj, SigmaViewSet):
            return SigmaViewSet.try_to_get(obj.__class__.queryset, pk)

        try:
            instance = obj.get(pk=pk)
        except obj.model.DoesNotExist:
            raise NotFound()

        return instance


    def get_deserialized(obj, data, *args, **kwargs):
        """
            Shortcut method to get model instance, and serializer corresponding to the request.

            Method version : uses the serializer_class provided in the subclass definition
            Static version : takes the serializer to use as its first argument.
        """
        if isinstance(obj, SigmaViewSet):
            return SigmaViewSet.get_deserialized(obj.__class__.serializer_class, data, *args, **kwargs)

        serializer = obj(data=data, *args, **kwargs)
        serializer.is_valid(raise_exception=True)
        instance = obj.Meta.model(**serializer.validated_data)
        return serializer, instance


    def serialized_response(obj, data, status=status.HTTP_200_OK, *args, **kwargs):
        """
            Shortcut method to get a 200-OK response with serialized data, out of a model instance or a queryset.

            Method version : uses the serializer_class provided in the subclass definition
            Static version : takes the serializer to use as its fist argument.
        """

        #TODO : OPTIMIZE HOW THE SERIALIZERS WORK
        if isinstance(obj, SigmaViewSet):
            serializer = SigmaViewSet.serialized_response(obj.__class__.serializer_class, data)
            for key,values in kwargs.items():
                if key.startswith("extra_"):
                    serializer.data[key.split('_')[2]]=values
            return serializer

        many = (type(data) == QuerySet)
        serializer = obj(data, many=many)

        l = [dict()] #list of dict for the data to add according to the pk
        # l[pk] -> all the variables to add -> l[pk]["name of the variable"]=value of the variable
        flag=False
        for key,value in kwargs.items():
            if key.startswith("extra_"):
                flag=True
                while int(key.split('_')[1])+1>len(l):
                    l.append(dict())
                l[int(key.split('_')[1])][str(key.split('_')[2])]=value

        if flag:
            for d in serializer.data:
                for key,value in l[d["pk"]].items():
                    d[key]=value

        return Response(serializer.data, status=status)



    def call_method_if_exists(obj, name, *args, **kwargs):
        """
            If the the method identified by the given `name` exists, execute it and returns its result.
            Otherwise, return None.

            Method version : try to call the method on self
            Static version : takes the object owning the method we try to call, as its first argument.
        """

        if hasattr(obj, name):
            f = getattr(obj, name)
            return f(*args, **kwargs)
        return None




    @staticmethod
    def check_permission(user, instance, actionname, *args, **kwargs):
        """
            Given action `actionname`, try to call `instance.can_actionname(user, *args, **kwargs)`
            If it exists and returns False, then a PermissionDenied exception is raised.

            Static version : takes the model containing the `can_actionname` function, as its first argument.
        """
        if hasattr(instance, 'can_' + actionname):
            f = getattr(instance, 'can_' + actionname)
            if not f(user, *args, **kwargs):
                raise PermissionDenied()

    #*********************************************************************************************#
    #**                           Pre-defined basic views helpers                               **#
    #*********************************************************************************************#

    def handle_action_list(obj, request, qsgetter, *args, **kwargs):
        """
            Provide a really basic way of handling list actions.
            It will simply serialize the queryset and response its result.
            To obtain the queryset, this method calls 'qsgetter(request.user, *args, **kwargs)'

            Method version : uses the serializer_class provided in the subclass definition.
            Static version : uses the serializer given as the first argument.
        """

        if isinstance(obj, SigmaViewSet):
            return SigmaViewSet.handle_action_list(obj.__class__.serializer_class, request, qsgetter, *args, **kwargs)

        qs = qsgetter(request.user)
        return SigmaViewSet.list_handler(obj, request, qs,*args,**kwargs)


    def handle_action(self, action, request, *args, **kwargs):
        """
            Provide a basic handler for actions, using the following steps :
            * create model_instance `instance` using `serializer_class` and `request.data`
            * call `instance.can_action` to check perms.
            * run the `action_handling_process`
        """
        serializer, instance = self.get_deserialized(request.data)
        SigmaViewSet.check_permission(request.user, instance, action, *args, **kwargs)
        return self.action_handling_process(action, request, serializer, instance, *args, **kwargs)


    def handle_action_pk_list(obj, serializer, request, pk, qsgetter, *args, **kwargs):
        """
            Provide a really basic way of handling list actions that apply on a specific ressource.
            It will check permissions to retrieve the specific ressource.
            If success, it will get the instance, get the queryset, and response its result.
            To obtain the queryset, this method calls 'qsgetter(request.user, instance, *args, **kwargs)'

            Method version : uses the queryset provided in the subclass definition.
            Static version : uses the queryset given as the first argument.
        """

        if isinstance(obj, SigmaViewSet):
            return SigmaViewSet.handle_action_pk_list(obj.__class__.queryset, serializer, request, pk, qsgetter, *args, **kwargs)

        instance = SigmaViewSet.try_to_get(obj, pk)
        SigmaViewSet.check_permission(request.user, instance, 'retrieve', *args, **kwargs)

        qs = qsgetter(request.user, instance, *args, **kwargs)
        return SigmaViewSet.serialized_response(serializer, qs)


    def handle_action_pk(self, action, request, pk, *args, **kwargs):
        """
            Provide a basic handler for pk actions, using the following steps :
            * create model_instance `instance` using `serializer_class` and `pk`
            * call `instance.can_action` to check perms.
            * run the `action_handling_process`
        """
        instance = self.try_to_get(pk)
        SigmaViewSet.check_permission(request.user, instance, action, *args, **kwargs)
        return self.action_handling_process(action, request, pk, instance, *args, **kwargs)


    def action_handling_process(self, action, request, *args, **kwargs):
        """
            A basic handling process for actions :
            * if it exists, call `instance.action_pre_handler`, and returns its result if there's any.
            * call `instance.action_handler`, and save the `response` or raise 500 if there's no response.
            * if it exists, call `instance.action_post_handler`, and returns its result if there's any
            * return the previously saved `response`
        """

        ret = self.call_method_if_exists(action + '_pre_handler', request, *args, **kwargs)
        if ret != None:
            return ret

        resp = self.call_method_if_exists(action + '_handler', request, *args, **kwargs)
        if resp == None:
            raise

        ret = self.call_method_if_exists(action + '_post_handler', request, *args, **kwargs)
        if ret != None:
            return ret

        return resp





    def list_handler(obj, request, qs, *args, **kwargs):
        """
            A basic retrieve handler to use with  `handle_action_list`.
        """
        return SigmaViewSet.serialized_response(obj, qs, *args, **kwargs)

    def retrieve_handler(self, request, pk, instance, *args, **kwargs):
        """
            A basic retrieve handler to use with  `handle_action_pk`.
        """
        return self.serialized_response(instance, **kwargs)


    def create_handler(self, request, serializer, instance):
        """
            A basic create handler to use with `handle_action`.
        """
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update_handler(self, request, pk, instance):
        """
            A basic update handler to use with `handle_action_pk`.
        """
        # serializer.save().
        # return Response(serializer.data, status=status.HTTP_200_OK)              # TODO : update / patch actions
        return Response(status=status.HTTP_200_OK)

    def destroy_handler(self, request, pk, instance):
        """
            A basic destroy handler to use with `handle_action_pk`.
        """
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    #*********************************************************************************************#
    #**                                   Notifications                                         **#
    #*********************************************************************************************#


    def notify_update(self, pk):
        """
            This function can be used by subclasses to notify clients of modifications using push servers
        """
        notify(self.__class__.__name__ + ' ' + pk)
