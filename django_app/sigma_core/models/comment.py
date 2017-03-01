from django.db import models
from sigma_api.importer import load_ressource

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
        return True
