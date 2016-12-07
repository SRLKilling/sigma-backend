from django.db.models.query import QuerySet
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from push_app.notify import notify

class SigmaViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    
    #*********************************************************************************************#
    #**                                    Useful methods                                       **#
    #*********************************************************************************************#
    
    def get_or_404(self, pk):
        """
            This method can be used to get a model instance based on it's primary key.
            If the instance does not exists, it will automatically throws a 404 error.
            
            Static version : takes the model to use as its first argument.
        """
        return SigmaViewSet.get_or_404(self.model_class, pk)
    
    @staticmethod
    def get_or_404(model_class, pk):
        try:
            instance = model_class.object.get(pk=pk)
        except model_class.DoesNotExist:
            raise NotFound()
            
        return instance
    
    
        
    def get_deserialized(self, data, *args, **kwargs):
        """
            Shortcut method to get model instance, and serializer corresponding to the request.
            
            Static version : takes the serializer to use as its first argument.
        """
        return SigmaViewSet.get_deserialized(self.serializer_class, data, *args, **kwargs)
        
    @staticmethod
    def get_deserialized(serializer_class, data, *args, **kwargs):
        serializer = serializer_class(data=data, *args, **kwargs)
        serializer.is_valid(raise_exceptions=True)
        instance = serializer.validated_data
        return serializer, instance
        
        
        
    def serialized_response(self, data):
        """
            Shortcut method to get a 200-OK response with serialized data, out of a model instance or a queryset.
            
            Static version : takes the serializer to use as its fist argument.
        """
        return SigmaViewSet.serialized_response(self.serializer_class, data)
        
    @staticmethod
    def serialized_response(serializer_class, data):
        many = (type(data) == QuerySet)
        serializer = serializer_class(data, many=many)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    def call_if_exists(self, name, *args, **kwargs):
        """
            If the the method identified by the given `name` exists, execute it and returns its result.
            Otherwise, return None.
            
            Static version : takes the object owning the method we try to call, as its first argument.
        """
        return SigmaViewSet.call_method_if_exists(self, name, *args, **kwargs)
    
    @staticmethod
    def call_method_if_exists(obj, name, *args, **kwargs):
        if hasattr(obj, name)
            f = getattr(obj, name)
            return f(obj, *args, **kwargs)
        return None
        
        
        
    @staticmethod
    def check_permission(user, instance, actionname, *args, **kwargs):
        """
            Given action `actionname`, try to call `instance.can_actionname(user, *args, **kwargs)`
            If it exists and returns False, then a PermissionDenied exception is raised.
            
            Static version : takes the model containing the `can_actionname` function, as its first argument.
        """
        if hasattr(instance, 'can_' + actionname)
            f = getattr(instance, 'can_' + actionname)
            if not f(instance, user, *args, **kwargs):
                raise PermissionDenied()
    
    #*********************************************************************************************#
    #**                           Pre-defined basic views helpers                               **#
    #*********************************************************************************************#        
        
    
    def basic_retrieve(self, request, pk, *args, **kwargs):
        """
            Provide a basic retrieve handler.
            It will try to get the requested object, then if it exists, apply can_retrieve to check
            permissions, and then return the object.
        """
        instance = self.get_or_404(pk)
        SigmaViewSet.check_permission(request.user, instance, 'retrieve', *args, **kwargs)        
        return self.serialized_response(instance)
    
    
    
    def basic_create(self, request, *args, **kwargs):
        """
            Provide a basic handler for a create action.
            In order, if those functions exists, it will :
            * create model_instance `instance` using `serializer_class` and `request.data`
            * call `instance.can_create` to check perms
            * call `instance.create_pre_handler`, and if nothing is returned
            * save the `instance`
            * call `instance.create_post_handler`
        """
        serializer, instance = self.get_deserialized(request)
        SigmaViewSet.check_permission(request.user, instance, 'create', *args, **kwargs)
        
        ret = self.call_if_exists('create_pre_handler', request, serializer, instance, *args, **kwargs)
        if ret != None:
            return Ret
        
        serializer.save()
        
        ret = self.call_if_exists('create_post_handler', request, serializer, instance, *args, **kwargs)
        if ret != None:
            return Ret
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
    
    def basic_destroy(self, request, pk, *args, **kwargs):
        """
            Provide a basic handler for a destroy action.
            It will try to get the requested object, then if it exists, apply can_destroy to check
            permissions.
            If it exists, destroy_handler is then called, and if it returns anything but True,
            this value is returned. Otherwise, the requested object is destroyed
        """
            
        instance = self.get_or_404(pk)
        SigmaViewSet.check_permission(request.user, instance, 'destroy', *args, **kwargs)
            
        ret = self.call_if_exists('destroy_pre_handler', request, serializer, instance, *args, **kwargs)
        if ret != None:
            return Ret
        
        instance.delete()
        
        ret = self.call_if_exists('destroy_post_handler', request, serializer, instance, *args, **kwargs)
        if ret != None:
            return Ret
            
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
    #*********************************************************************************************#
    #**                                   Notifications                                         **#
    #*********************************************************************************************#
        
        
    def notify_update(self, pk):
        """
            This function can be used by subclasses to notify clients of modifications using push servers
        """
        notify(self.__class__.__name__ + ' ' + pk)
        