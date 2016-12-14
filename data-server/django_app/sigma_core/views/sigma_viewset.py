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
        
        
    def serialized_response(obj, data, status=status.HTTP_200_OK):
        """
            Shortcut method to get a 200-OK response with serialized data, out of a model instance or a queryset.
            
            Method version : uses the serializer_class provided in the subclass definition
            Static version : takes the serializer to use as its fist argument.
        """
        if isinstance(obj, SigmaViewSet):
            return SigmaViewSet.serialized_response(obj.__class__.serializer_class, data)
        
        many = (type(data) == QuerySet)
        serializer = obj(data, many=many)
        return Response(serializer.data, status=status)
    
    
        
    def call_method_if_exists(obj, name, *args, **kwargs):
        """
            If the the method identified by the given `name` exists, execute it and returns its result.
            Otherwise, return None.
            
            Method version : try to call the method on self
            Static version : takes the object owning the method we try to call, as its first argument.
        """
        
        if hasattr(obj, name):
            f = getattr(obj, name)                                                                              # LE BUG VIENT DU FAIt QUE LE QUERYSET DONNE UN AKNOW QS ET PAS UN GROUP QS ;)
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
      
    def handle_action_list(self, request, qsgetter, *args, **kwargs):
        """
            Provide a really basic way of handling list actions.
            It will simply serialize the queryset and response its result.
            To obtain the queryset, this method calls 'qsgetter(request.user, *args, **kwargs)'
        """
        qs = qsgetter(request.user, *args, **kwargs)
        return self.serialized_response(qs)
        
    
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
        
      
        
        
    
        
    
    def retrieve_handler(self, request, pk, instance):
        """
            A basic retrieve handler to use with  `handle_action_pk`.
        """      
        return self.serialized_response(instance)
        
        
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
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_200_OK)                                       # TODO : update / patch actions
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
        