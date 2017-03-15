from django.db import models
from sigma_api.importer import load_ressource

GroupMember = load_ressource("GroupMember")
Acknowledgment = load_ressource("Acknowledgment")


class GroupQuerySet(models.QuerySet):

    def user_can_see(self, user):
        """ Filter to get all group a user can see (member, or member of acknowledging group, or public) """
        membersof = GroupMember.objects.for_user(user).values('group')
        memberof_acknowledged = Acknowledgment.objects.filter(acknowledged_by__in=membersof).values('acknowledged')

        return self.filter(
            models.Q(pk__in = membersof) |
            (models.Q(pk__in = memberof_acknowledged) & models.Q(group_visibility=Group.VISIBILITY_NORMAL)) |
            models.Q(group_visibility=Group.VISIBILITY_PUBLIC)
        )

    def acknowledged_by(self, group):
        """ Filter all groups that are aknowledged by a given one """
        return self.filter(pk__in = Acknowledgment.objects.acknowledged_by(group))

    def acknowledging(self, group):
        """ Filter all groups that are aknowledging by a given one """
        return self.filter(pk__in = Acknowledgment.objects.acknowledging(group))



class Group(models.Model):
    """
        This model is used to represent any kind of user's group (friends, coworkers, schools, etc...)
    """

    objects = GroupQuerySet.as_manager()

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#


    name = models.CharField(max_length=254, unique=True)
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
    #**                                      Methods                                            **#
    #*********************************************************************************************#
    def can_retrieve(self, user, *args, **kwargs):
        """
            Returns True if the given user can access the group.
            This can happen in the following cases :
            * The group visibility is set to `VISIBILITY_PUBLIC`
            * I'm a member of the group
            * The group visibility is set to `VISIBILITY_NORMAL` and I'm a member of an aknowledging group
        """

        if self.group_visibility == Group.VISIBILITY_PUBLIC or GroupMember.objects.is_member(self, user):
            return True

        elif self.group_visibility == Group.VISIBILITY_NORMAL:
            for parent in Group.objects.acknowledging(self):
                if GroupMember.objects.is_member(parent, user):
                    return True

        return False

    def can_print_invitations(self, user):
        return GroupMember.objects.is_member(group, user)

    #No can_member : already handled via the queryset
    #No can_print_invitations : same reason
    #No list : same reason
