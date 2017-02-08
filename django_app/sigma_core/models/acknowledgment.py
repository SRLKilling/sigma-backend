from django.db import models
from sigma_api.importer import load_ressource

class AcknowledgmentQuerySet(models.QuerySet):
    
    def acknowledged_by(self, group):
        """ Filter acknowledgment relation, where the given group(s) is the acknowledging one """
        return self.filter(acknowledged_by = group)
        
    def acknowledging(self, group):
        """ Filter acknowledgment relation, where the given group(s) is the acknowledged one """
        return self.filter(acknowledged__in = group) if isinstance(group, models.QuerySet) else self.filter(acknowledged = group)
        
    def is_acknowledged_by(self, parent_group, group):
        """ Returns true if group is acknowledged by parent_group """
        return self.acknowledged_by(parent_group).acknowledging(group).exists()


class Acknowledgment(models.Model):
    """
        This model is used to represent the fact that a group acknowledge the existance of another group.
        All members of the acknowledging group will be able to see the acknowledged group.
    """
    
    objects = AcknowledgmentQuerySet.as_manager()
    class Meta:
        unique_together = (("acknowledged", "acknowledged_by"),)
    
    acknowledged = models.ForeignKey('Group', related_name='acknowledged_by')
    acknowledged_by = models.ForeignKey('Group', related_name='acknowledging')
    date = models.DateTimeField(auto_now_add=True)
    
    # delegate_admin = models.BooleanField(default=True)

    def __str__(self):
        return "'%s' acknowledged by '%s'" % (self.acknowledged.__str__(), self.acknowledged_by.__str__())