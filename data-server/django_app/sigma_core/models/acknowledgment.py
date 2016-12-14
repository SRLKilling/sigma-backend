from django.db import models

class Acknowledgment(models.Model):
    """
        This model is used to represent the fact that a group acknowledge the existance of another group.
        All members of the acknowledging group will be able to see the acknowledged group.
    """

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#
    
    class Meta:
        unique_together = (("acknowledged", "acknowledged_by"),)
    
    acknowledged = models.ForeignKey('Group', related_name='acknowledged_by')
    acknowledged_by = models.ForeignKey('Group', related_name='acknowledged')
    
    date = models.DateTimeField(auto_now_add=True)
    
    # delegate_admin = models.BooleanField(default=True)

    def __str__(self):
        return "'%s' acknowledged by '%s'" % (self.acknowledged.__str__(), self.acknowledged_by.__str__())

    
    #*********************************************************************************************#
    #**                                       Getters                                           **#
    #*********************************************************************************************#
    
            
    @staticmethod
    def get_acknowledged_by_qs(user, group):
        """ Return a queryset containing the list of groups that are aknowledged by the given group. """
        return Acknowledgment.objects.filter(acknowledged_by = group).values("acknowledged")
        
    @staticmethod
    def get_acknowledging_qs(user, group):
        """ Return a queryset containing the list of groups that aknowledge the given group. """
        return Acknowledgment.objects.filter(acknowledged = group).values("acknowledged_by")
        
        
    @staticmethod
    def is_acknowledged_by(sub, parent):
        """ Return true if the first group argument is acknowledged by the second group argument.
            False otherwise.
        """
        return Acknowledgment.objects.filter(acknowledged = sub, acknowledged_by = parent).exists()
    