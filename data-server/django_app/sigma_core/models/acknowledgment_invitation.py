from django.db import models

class AcknowledgementInvitation(models.Model):
    """
        Modelize an invitation to acknowledge a group.
        Invitation can be issued both by the invitee and the inviter.
        Invitation have a short life-time.
        As soon as someone accepts or declines the invitation, the instance is destroyed.
    """
    
    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    class Meta:
        unique_together = (("invitee", "group"),)

    acknowledged = models.ForeignKey('Group', related_name='acknowledged_by')
    acknowledged_by = models.ForeignKey('Group', related_name='acknowledged')
    
    """ Represents whether the invitation has been issued by the invitee or the inviter """
    issued_by_invitee = models.BooleanField(default=True)
    
    """ The date the invitation has been issued """
    date = models.DateTimeField(auto_now_add=True)
    
    
    #*********************************************************************************************#
    #**                                       Getters                                           **#
    #*********************************************************************************************#
            
            
    @staticmethod
    def get_group_acknowledge_invitations_qs(user):
        """ Return a queryset containing the list of invitations where `user` is the invitee
            `user` can be a model instance, or a primary key. """
        return AcknowledgementInvitation.objects.filter(acknowledged = group)
        
    @staticmethod
    def is_invited(sub, parent):
        """ Return true if the first group argument is invited to be acknowledged by the second group argument.
            False otherwise.
        """
        return AcknowledgementInvitation.objects.filter(acknowledged = sub, acknowledged_by = parent).exists()
    
    
    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#
    
    def is_admin_of_invited(self, group):
        mb = GroupMember.get_membership(user, self.acknowledged)
        return (mb.is_admin or mb.is_super_administrator)
        
    def is_admin_of_inviter(self, group):
        mb = GroupMember.get_membership(user, self.acknowledged_by)
        return (mb.is_admin or mb.is_super_administrator)
    
    def can_retrieve(self, user):
        """ Check whether `user` can retrieve the invitation.
            Must be an admin of one of the group.
        """
        return self.is_admin_of_invited(user) or self.is_admin_of_inviter(user)
            
    
    def can_create(self, user):
        """ Check whether `user` can create the invitation.
            User must be an admin of the issuer group
        """
        if self.issued_by_invitee:
            return self.is_admin_of_invited(user)
        else:
            return self.is_admin_of_inviter(user)
            
            
    def can_accept(self, user):
        """ Check wheter `user` can accept the invitation.
            User must be an admin of the validating group
        """
        if self.issued_by_invitee:
            return self.is_admin_of_inviter(user)
        else:
            return self.is_admin_of_invited(user)
            
            
    def can_destroy(self, user):
        """ Check whether `user` can destroy, i.e. decline, the invitation.
            Must be an admin of one of the groups.
        """
        return self.is_admin_of_invited(user) or self.is_admin_of_inviter(user)
    
