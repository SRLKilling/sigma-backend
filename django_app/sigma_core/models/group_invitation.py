from django.db import models
from sigma_api.importer import load_ressource

GroupMember = load_ressource("GroupMember")

class GroupInvitationQuerySet(models.QuerySet):

    def get_user_invitations(self,user):
        """ Return a queryset containing the list of invitations where `user` is the invitee
            `user` can be a model instance, or a primary key """
        return self.filter(invitee = user).order_by("date")

    def get_group_invitations_qs(self, user, group):
        """ Return a queryset containing the list of invitations where `group` is the inviter group
            `group` can be a model instance, or a primary key """
        if GroupMember.objects.is_member(group,user):
            return self.filter(models.Q(group = group) & models.Q(issued_by_invitee=False))
        else:
            return self.none()

    def get_group_invitations_pending(self, user, group):
        """ Return a queryset containing the list of invitations where the user in the asker
            `group` can be a model instance, or a primary key """
        if GroupMember.objects.is_member(group,user):
            return self.filter(models.Q(group = group) & models.Q(issued_by_invitee=True))
        else:
            return self.none()

class GroupInvitation(models.Model):
    """
        Modelize an invitation to a group.
        Invitation can be issued both by the invitee and the inviter (depending on the group settings)
        Invitation have a short life-time.
        As soon as someone accepts or declines the invitation, the instance is destroyed.
    """

    objects = GroupInvitationQuerySet.as_manager()

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    class Meta:
        unique_together = (("invitee", "group"),)

    group = models.ForeignKey('Group', related_name='invitations')
    invitee = models.ForeignKey('User', related_name='invitations')

    """ Represents whether the invitation has been issued by the invitee or the inviter """
    issued_by_invitee = models.BooleanField(default=True)

    """ The date the invitation has been issued """
    date = models.DateTimeField(auto_now_add=True)


    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#


    def can_retrieve(self, user):
        """ Check whether `user` can retrieve the invitation.
            True in the following cases
            * You're the invitee.
            * You're member of the group, with the invite right.
        """
        if user == self.invitee:
            return True

        else:
            user_mb = GroupMember.objects.get_membership(user, self.group)
            return user_mb != None and user_mb.has_invite_right


    def can_create(self, user):
        """ Check whether `user` can create the invitation.
            * If the invitation is issued by the invitee, the group must allow users to ask for invitations.
            * Otherwise, the inviter must have the corresponding right.
        """
        if self.issued_by_invitee:
            return (self.invitee == user) and (self.group.can_anyone_ask)

        else:
            inviter_mb = GroupMember.objects.get_membership(user, self.group)
            return inviter_mb != None and inviter_mb.has_invite_right


    def can_accept(self, user):
        """ Check wheter `user` can accept the invitation.
            * If the invition is issued by invitee, `user` must be a member with invite right
            * Otherwise, `user` must be the invitee
        """
        if not self.issued_by_invitee:
            return user == self.invitee

        else:
            user_mb = GroupMember.objetcs.get_membership(user, self.group)
            return user_mb != None and user_mb.has_invite_right


    def can_destroy(self, user):
        """ Check whether `user` can destroy, i.e. decline, the invitation.
            Same as can_retrieve
            True in the following cases
            * You're the invitee.
            * You're member of the group, with the invite right.
        """
        if user == self.invitee:
            return True

        else:
            user_mb = GroupMember.objects.get_membership(user, self.group)
            return user_mb != None and user_mb.has_invite_right
