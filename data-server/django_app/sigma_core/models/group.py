from django.db import models
from sigma_core.models.user import User
from sigma_core.models.group_member import GroupMember

class Group(models.Model):
    """
        This model is used to represent any kind of user's group (friends, coworkers, schools, etc...)
    """

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#
    
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    is_protected = models.BooleanField(default=False) # if True, the Group cannot be deleted
    
    """ Determine whether one can ask to join the group, or must be invited """
    can_anyone_ask = models.BooleanField(default=False)
    
    """ Determine whether one can directly join the group, or must send an invitation """
    need_validation_to_join = models.BooleanField(default=False)

    
    VISIBILITY_PUBLIC = 0
    VISIBILITY_NORMAL = 1
    VISIBILITY_PRIVATE = 2
    POSSIBLE_VISIBILITIES = ( (0, 'Public'), (1, 'Normal'), (2, 'Secret'), )
    
    """
        Set the visibility of the group's members
        If set to :
        * `VISIBILITY_PUBLIC` -> The group is public (all members can be seen)
        * `VISIBILITY_NORMAL` -> The group is normal (all members that I am connected to can be seen)
        * `VISIBILITY_PRIVATE` -> The group is private (only the members can see themselves)
    """
    members_visibility = models.PositiveSmallIntegerField(choices=POSSIBLE_VISIBILITIES, default=0)

    """
        Set the visibility of the group itself
        The possible values are :
        * `VISIBILITY_PUBLIC` -> The group can be seen by everyone
        * `VISIBILITY_NORMAL` -> The group can be seen by people from acknowledged groups
        * `VISIBILITY_PRIVATE` -> The group can be seen only by people who are in it
    """
    group_visibility = models.PositiveSmallIntegerField(choices=POSSIBLE_VISIBILITIES,default=0)
    
    
    
    
    #*********************************************************************************************#
    #**                                      Getters                                            **#
    #*********************************************************************************************#
    
    def aknowleding_group_qs(self):
        """
            Returns a Queryset containing the groups that are directly aknowleding this group
        """
        return self.aknowledged_by.select_related('aknowledged_by')
    
    
    #*********************************************************************************************#
    #**                                      Methods                                            **#
    #*********************************************************************************************#    
    
    def can_retrieve(user):
        """
            Returns True if the given user can access the group.
            This can happen in the following cases :
            * The group visibility is set to `VISIBILITY_PUBLIC`
            * I'm a member of the group
            * The group visibility is set to `VISIBILITY_NORMAL` and I'm a member of an aknowledging group
        """
            
        if group.group_visibility == VISIBILITY_PUBLIC or GroupMember.is_member(group, user):
            return True
            
        elif group.group_visibility == VISIBILITY_NORMAL:
            for parent in group.parent_group_qs():
                if GroupMember.is_member(parent, user):
                    return True
            
        return False
