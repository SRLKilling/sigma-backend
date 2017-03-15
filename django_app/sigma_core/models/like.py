from django.db import models
from sigma_api.importer import load_ressource

class LikeQuerySet(models.QuerySet):

    def by_user(self, user):
        return self.filter(user = user)

    def on_publication(self, publication):
        return self.filter(publication = publication)

class Like(models.Model):

    objects = LikeQuerySet.as_manager()

    user = models.ForeignKey("User")
    publication = models.ForeignKey("Publication")

    def __str__(self):
        return "Like(" + ", ".join([self.user.__str__(), self.publication.__str__()]) + ")"

    def can_retrieve(self, user):
        b = True
        b = b and self.publication.can_retrieve(user)
        return b

    def can_create(self, user):
        b = True
        b = b and self.publication.can_retrieve(user)
        b = b and self.user == user
        return b

    def can_destroy(self, user):
        b = True
        b = b and self.user == user
        return b
