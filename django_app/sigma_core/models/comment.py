from django.db import models
from sigma_api.importer import load_ressource

Publication = load_ressource("Publication")

class CommentQuerySet(models.QuerySet):

    def sort(self):
        return self.order_by('-date')

    def by_user(self, user):
        return self.filter(user = user)

    def on_publication(self, publication):
        return self.filter(publication = publication)

class Comment(models.Model):

    objects = CommentQuerySet.as_manager()

    user = models.ForeignKey("User")
    publication = models.ForeignKey("Publication")
    comment = models.CharField(max_length=1500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Comment(" + ", ".join([self.user.__str__(), self.publication.__str__(), self.date.__str__()]) + ")"

    def can_retrieve(self, user):
        b = True
        b = b and Publication.objects.visible_by_user(user).filter(pk = self.pk).exists()
        return b

    def can_create(self, user):
        b = True
        b = b and user == self.user
        b = b and self.publication.can_retrieve(user)
        return b

    def can_destroy(self, user):
        b = True
        b = b and user == self.user
        return b
