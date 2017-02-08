from django.db import models
from sigma_api.importer import load_ressource

GroupMember = load_ressource("GroupMember")

class GroupFieldValue(models.Model):
    """
        Modelize a group specific field.
        Fields are member's information that makes sense only to that group.
        For exemple, defining a role such as "Project leader" only makes sense inside a specific group representing a project.
    """
    
    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#
    
    class Meta:
        unique_together = (("membership", "field"),)
    
    membership = models.ForeignKey('GroupMember', related_name='field_values')
    field = models.ForeignKey('GroupField', related_name='+')
    
    """ Value is of type text, but should be interpreted using field's type """
    value = models.TextField(blank=True)

        
    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#

    def can_retrieve(self, user):
        """
            Check whether `user` can retrieve a field value.
            One can see field values if and only if he can see the membership
        """
        return self.membership.can_retrieve(user)
            
            
    def can_write(self, user):
        """
            Checke whether `user` can write a field value.
            The user must be the member himself, or an admin if the field is protected
        """
        try:
            if not self.field.is_protected and self.membership.user == user:
                return True
                
            membership = GroupMember.objects.get_membership(self.membership.group, user)
            return (membership.is_administrator or membership.is_super_administrator)
            
        except GroupMember.model.DoesNotExist:
            return False
        
    
    def can_create(self, user):
        return self.can_write(user)
            
    def can_update(self, user):
        return self.can_write(user)
            
    def can_destroy(self, user):
        return self.can_write(user)
