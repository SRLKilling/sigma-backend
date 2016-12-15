from django.db import models

from sigma_core.models import group_member as GroupMember

class GroupInvitation(models.Model):
    """
        Modelize an invitation to a group.
        Invitation can be issued both by the invitee and the inviter (depending on the group settings)
        Invitation have a short life-time.
        As soon as someone accepts or declines the invitation, the instance is destroyed.
    """
    
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
    #**                                       Getters                                           **#
    #*********************************************************************************************#
            
            
    @staticmethod
    def get_user_invitations_qs(user):
        """ Return a queryset containing the list of invitations where `user` is the invitee
            `user` can be a model instance, or a primary key """
        if type(user) != int:
            user = user.pk
        return GroupInvitation.objects.filter(invitee = user)
            
    @staticmethod
    def get_group_invitations_qs(group):
        """ Return a queryset containing the list of invitations where `group` is the inviter group
            `group` can be a model instance, or a primary key """
        if type(group) != int:
            group = group.pk
        return GroupInvitation.objects.filter(group = group)
        
    
    
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
            user_mb = GroupMember.GroupMember.get_membership(user, self.group)
            return user_mb != None and user_mb.has_invite_right
            
    
    def can_create(self, user):
        """ Check whether `user` can create the invitation.
            * If the invitation is issued by the invitee, the group must allow users to ask for invitations.
            * Otherwise, the inviter must have the corresponding right.
        """            
        if self.issued_by_invitee:
            return (self.inviteee == user) and (self.group.can_anyone_ask)
            
        else:
            inviter_mb = GroupMember.GroupMember.get_membership(user, self.group)
            return inviter_mb != None and inviter_mb.has_invite_right
            
            
    def can_accept(self, user):
        """ Check wheter `user` can accept the invitation.
            * If the invition is issued by invitee, `user` must be a member with invite right
            * Otherwise, `user` must be the invitee
        """
        if not self.issued_by_invitee:
            return user == self.invitee
            
        else:
            user_mb = GroupMember.GroupMember.get_membership(user, self.group)
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
            user_mb = GroupMember.GroupMember.get_membership(user, self.group)
            return user_mb != None and user_mb.has_invite_right
    
