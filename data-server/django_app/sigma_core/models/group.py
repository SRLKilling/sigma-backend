from django.db import models

from sigma_core.models import group_member as GroupMember, acknowledgment as Acknowledgment

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

    def __str__(self):
        return 'Group %d : %s' % (self.pk, self.name)




    #*********************************************************************************************#
    #**                                      Getters                                            **#
    #*********************************************************************************************#

    @staticmethod
    def get_user_groups_qs(user):
        """
            Returns a Queryset containing all the groups a user is member of
        """
        membersof = GroupMember.GroupMember.get_user_memberships_qs(user).values('group')
        memberof_acknowledged = Acknowledgment.Acknowledgment.objects.filter(acknowledged_by__in=membersof).values('acknowledged')
        return Group.objects.all().filter( models.Q(pk__in = membersof) | models.Q(pk__in = memberof_acknowledged) | models.Q(group_visibility=Group.VISIBILITY_PUBLIC))

    @staticmethod
    def get_acknowledged_by_qs(user, group):
        """
            Returns a Queryset containing all the groups that a given group acknowledge
        """
        return Group.objects.filter(pk__in = Acknowledgment.Acknowledgment.get_acknowledged_by_qs(user, group))

    @staticmethod
    def get_acknowledging_qs(user, group):
        """
            Returns a Queryset containing all the groups that acknowledge the given group
        """
        return Group.objects.filter(pk__in = Acknowledgment.get_acknowledging_qs(user, group))


    #*********************************************************************************************#
    #**                                      Methods                                            **#
    #*********************************************************************************************#    

    def can_retrieve(self, user):
        """
            Returns True if the given user can access the group.
            This can happen in the following cases :
            * The group visibility is set to `VISIBILITY_PUBLIC`
            * I'm a member of the group
            * The group visibility is set to `VISIBILITY_NORMAL` and I'm a member of an aknowledging group
        """

        if self.group_visibility == Group.VISIBILITY_PUBLIC or GroupMember.GroupMember.is_member(self, user):
            return True

        elif self.group_visibility == Group.VISIBILITY_NORMAL:
            for parent in Group.get_group_acknowledged_by_qs(None, self):                                       # TODO : Stuff to do here, None is ugly
                if GroupMember.GroupMember.is_member(parent, user):
                    return True

        return False
