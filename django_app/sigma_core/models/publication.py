from django.db import models
from sigma_api.importer import load_ressource

SharedPublication = load_ressource("SharedPublication")

class PublicationQuerySet(models.QuerySet):

    def sort(self):
        return self.order_by('-last_commented')

    def created_by(self, user):
        return self.filter(author = user)

    def visible_by_user(self, user):
        ids = SharedPublication.objects.visible_by_user(user).values('publication').distinct()
        return self.filter(pk__in = ids)

    def with_event(self):
        return self.exclude(related_event__isnull=True)

    def without_event(self):
        return self.filter(related_event__isnull=True)

    def in_group(self, group):
        ids = SharedPublication.objects.in_group(group).values('publication').distinct()
        return self.filter(pk__in = ids)

class Publication(models.Model):
    """
        An abstract publication
    """

    objects = PublicationQuerySet.as_manager()

    group = models.ForeignKey("Group", related_name='publications')
    author = models.ForeignKey("User")
    date = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=144, blank=True)
    content = models.CharField(max_length=1500)

    related_event = models.ForeignKey("Event", blank=True, null=True)
    internal = models.BooleanField(default=True)
    last_commented = models.DateTimeField(auto_now_add=True)
    # last_commented : also when shared

    def __str__(self):
        return "Publication(" + ", ".join([self.title, self.group.__str__(), self.author.__str__(), str(self.internal)]) + ")"

    def share(self, group):
        s = SharedPublication.model(publication = self, group = group)
        s.save()
        return s

    def can_retrieve(self, user):
        return True
