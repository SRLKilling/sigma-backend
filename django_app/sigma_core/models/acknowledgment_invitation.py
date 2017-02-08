from django.db import models
from sigma_api.importer import load_ressource

GroupMember = load_ressource("GroupMember")

class AcknowledgmentInvitation(models.Model):
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
        unique_together = (("acknowledged", "acknowledged_by"),)

    acknowledged = models.ForeignKey('Group', related_name='invitation_to_be_acknowledged')
    acknowledged_by = models.ForeignKey('Group', related_name='invitation_to_acknowledge')
    
    """ Represents whether the invitation has been issued by the invitee or the inviter """
    issued_by_invitee = models.BooleanField(default=True)
    
    """ The date the invitation has been issued """
    date = models.DateTimeField(auto_now_add=True)
    
    
    #*********************************************************************************************#
    #**                                       Getters                                           **#
    #*********************************************************************************************#
            
            
    @staticmethod
    def get_invitations_qs(user, group):
        """ Return a queryset containing the list of invitations related to the given group.
            The given group can be the inviter or the invitee. """
        return AcknowledgmentInvitation.objects.filter( models.Q(acknowledged = group) | models.Q(acknowledged_by = group) )
        
    @staticmethod
    def is_invited(sub, parent):
        """ Return true if the first group argument is invited to be acknowledged by the second group argument.
            False otherwise.
        """
        return AcknowledgmentInvitation.objects.filter(acknowledged = sub, acknowledged_by = parent).exists()
    
    
    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#
    
    def is_admin_of_invited(self, user):
        mb = GroupMember.model.get_membership(self.acknowledged, user)
        return mb != None and (mb.is_administrator or mb.is_super_administrator)
        
    def is_admin_of_inviter(self, user):
        mb = GroupMember.model.get_membership(self.acknowledged_by, user)
        return mb != None and (mb.is_administrator or mb.is_super_administrator)
        
        
    
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
    
