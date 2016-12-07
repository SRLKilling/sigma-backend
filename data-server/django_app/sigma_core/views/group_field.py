from rest_framework import status
from rest_framework.decorators import detail_route
from sigma_core.views.sigma_viewset import SigmaViewSet

from sigma_core.models.group_field import GroupField
from sigma_core.serializers.group_field import GroupFieldSerializer


class GroupFieldViewSet(SigmaViewSet):
    
    serializer_class = GroupFieldSerializer
    queryset = GroupField.objects.all()
    
    
    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

        
    def retrieve(self, request, pk):
        """
            REST retrieve action. Used to retrieve a group_field.
        """
        return self.basic_retrieve(request, pk)
    
    
    
    
    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#

    def create(self, request):
        """
            REST create action. Used to create a Group Field.
            If succeeded, returns HTTP_201_CREATED with the newly created Group field object.
        """
        return self.basic_create(request)
        
        
    
    def update(self, request, pk):
        """
            REST update action. Used to update a Group Field.
            If succeeded, returns HTTP_201_SUCCESS with the updated Group field object.
        """
        
        # return self.basic_update(request, pk)                                                                                 # HERE !
        pass
        
        
    def destroy(self, request, pk):
        """
            REST destroy action. Used to update a Group Field.
            If succeeded, returns HTTP_204_NO_CONTENT.
        """
        
        return self.basic_destroy(request, pk)
        