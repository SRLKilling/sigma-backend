from django.db import models
from sigma_api.importer import load_ressource

Group = load_ressource("Group")
User = load_ressource("User")

class GroupMemberQuerySet(models.QuerySet):

    def for_user(self, user):
        """ Return a queryset containing all of a user memberships """
        return self.filter(user=user)
        
    def for_group(self, group):
        """ Returns a queryset containing all members of a group. """
        return self.filter(group=group)
        
    def user_can_see(self, group, user):
        """
            Returns a queryset containing all members of the given group, a user can see.
            * If you're a member, you'll see everybody
            * If not, and the group is public, you'll see not-hidden members
            * If not, and the group is normal, you'll see not-hidden and connected to you members
        """
        if self.is_member(group, user):
            return self

        elif group.members_visibility == Group.model.VISIBILITY_PUBLIC:
            return self.filter(group = group, hidden = False)

        elif group.members_visibility == Group.model.VISIBILITY_NORMAL:
            # return self.filter(group = group, hidden = False, user__in = User.User.get_connected_qs(user))                                        # TODO !!
            pass

        return self.none()
        
        
    def get_membership(self, group, user):
        """ Tries to get the membership corresponding to the given `user` and `group` """
        return self.get(group=group, user=user)
    
    
    def is_member(self, group, user):
        """ Returns True if and only if `user` is a member of the given `group`. """
        return self.filter(group=group, user=user).exists()

    def are_related(self, user1, user2):
        """ Return a queryset containing user1 memberships where user2 is also a member of the same group """                                        # TODO !!
        # groups_user2 = self.member
        # return GroupMember.get_user_memberships_qs(user1).filter(group__in = GroupMember.get_user_memberships_qs(user2).values('group')).exists()
        return self




class GroupMember(models.Model):
    """
        Modelize a membership relation between an User and a Group.
        A user is a member of a group if and only if the corresponding GroupMember object exists
    """
    
    objects = GroupMemberQuerySet.as_manager()

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    class Meta:
        unique_together = (("user", "group"),)

    user = models.ForeignKey('User', related_name='memberships')
    group = models.ForeignKey('Group', related_name='memberships')



    """ The date the user has been accepting into the group """
    created = models.DateTimeField(auto_now_add=True)

    """ If sets to True, you can't be seen by non-members, regardless of the group's members_visibility setting """
    hidden = models.BooleanField(default=False)



    """ An administrator has all rights, and can change other's rights (including other admins).
        Admins also have the power to acknowledge or ask for acknowledgment. """
    is_administrator = models.BooleanField(default=False)

    """ The superadministrator must be unique.
        He is an admin whose rights can't be changed by other admins. """
    is_super_administrator = models.BooleanField(default=False)

    """ If True, the member can invite or accept inviation to enter the group. """
    has_invite_right = models.BooleanField(default=False)

    """ If True, the member will be able to chat when non-member users try to contact the group. """
    has_contact_right = models.BooleanField(default=False)

    """ If True, the member can publish on the official group page, and moderate/accept/decline others publications intentions. """
    has_publish_right = models.BooleanField(default=False)

    """ If True, the member can kick other members (except admins if he is not an admin) """
    has_kick_right = models.BooleanField(default=False)


    def __str__(self):
        return "User \"%s\" in Group \"%s\"" % (self.user.__str__(), self.group.__str__())


    #*********************************************************************************************#

    @staticmethod
    def create(user, group, sa = False):
        """
            Create a membership based on the given user an group.
            This static method is used by following views :
            * InvitationView create members once an invitation is accepted
            * GroupView create super admin right after creating a group
        """
        member = GroupMember(user=user, group=group)
        if sa:
            member.is_super_administrator = True
            member.is_administrator = True
        member.save()

        UserConnection.create_new_connections_gr(user, group)
        return member

    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#


    def can_retrieve(self, user):
        """ Check whether `user` can retrieve the membership.
            True in the following cases :
            * You're the member.
            * You're a member of the group.
            * The member is not hidden, and the group is not public
            * The member is not hidden, and I'm connected to the member
        """
        if user == self.user or GroupMember.objects.is_member(self.group, user):
            return True

        elif not self.hidden:
            if self.group.members_visibility == Group.model.VISIBILITY_PUBLIC:
                return True
            elif self.group.members_visibility == Group.model.VISIBILITY_NORMAL:
                return user.is_connected_to( self.user )

        return False

    def can_change_right(self, user):
        """
            Check whether `user` can change member's rights.
            `user` has to be an admin, or if the member is an admin, a super admin.
        """
        user_membership = GroupMember.get_membership(self.group, user)

        return (not self.is_super_administrator) and ( (self.is_administrator and user_membership.is_super_administrator) or user_membership.is_administrator )


    def can_destroy(self, user):
        """
            Check whether `user` can kick the member.
            `user` must be a member with kick right, or an admin.
            If `user` is trying to kick an admin, he must be a super admin himself
            We can never kick a super admin.
        """
        user_membership = GroupMember.get_membership(self.group, user)

        return (user_membership != None) and (user_membership.can_kick or user_membership.is_administrator or user_membership.is_super_administrator) and (not self.is_administrator or user_membership.is_super_administrator) and (not self.is_super_administrator)
