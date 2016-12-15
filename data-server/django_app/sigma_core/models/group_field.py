from django.db import models

from sigma_core.models import group_member as GroupMember

class GroupField(models.Model):
    """
        Modelize a group specific field.
        Fields are member's information that makes sense only to that group.
        For exemple, defining a role such as "Project leader" only makes sense inside a specific group representing a project.
    """
    
    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#
    
    group = models.ForeignKey('Group', related_name='fields')
    name = models.CharField(max_length=254)
    
    
    """ The type of the field. This allows a corresponding html input, and some validations functions """
    TYPE_NUMBER = 0
    TYPE_STRING = 1
    TYPE_CHOICE = 2 
    TYPE_EMAIL = 3
    TYPES = ( (TYPE_NUMBER, "Number"), (TYPE_STRING, "String"), (TYPE_CHOICE, "Choice"), (TYPE_EMAIL, "Email")  )
    
    type = models.PositiveSmallIntegerField(default=TYPE_NUMBER, choices=TYPES)
    
    """ The accept field is generic and represents data that are used by the validator to check if a field value is acceptable """
    accept = models.TextField(default='', blank=True)
    
    """ If the field is protected, only the group admins will be able to member's values of the field """
    protected = models.BooleanField(default=False)
    
    """ If sets to True, then multiple field_values can be created by the member (e.g. multiple phone numbers) """
    multiple_values_allowed = models.BooleanField(default=False)
    

    
        
    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#
    
    def can_retrieve(self, user):
        """
            Check whether `user` can retrieve a field of a group.
            One can see group fields if and only if he can see the group
        """
        return self.group.can_retrieve(user)
            
    
    def can_create(self, user):
        """
            Check whether `user` can create a group field.
            Only admins are allowed to do so.
        """
        membership = GroupMember.GroupMember.get_membership(self.group, user)
        return (membership != None) and (membership.is_administrator or membership.is_super_administrator)
            
    def can_update(self, user):
        """
            Check whether `user` can update a group field.
            Only admins are allowed to do so.
        """
        membership = GroupMember.GroupMember.get_membership(self.group, user)
        return (membership != None) and (membership.is_administrator or membership.is_super_administrator)
            
    def can_destroy(self, user):
        """
            Check whether `user` can destroy a group field.
            Only admins are allowed to do so.
        """
        membership = GroupMember.GroupMember.get_membership(self.group, user)
        return (membership != None) and (membership.is_administrator or membership.is_super_administrator)
