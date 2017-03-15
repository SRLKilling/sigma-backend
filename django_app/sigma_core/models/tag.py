from django.db import models
from sigma_api.importer import load_ressource

class TagQuerySet(models.QuerySet):

    def tag_by(self, user):
        return self.filter(user = user)

    def tag_of(self, user):
        return self.filter(tagged = user)

    def on_publication(self, publication):
        return self.filter(publication = publication)

class Tag(models.Model):

    objects = TagQuerySet.as_manager()

    user = models.ForeignKey("User", related_name="user")
    publication = models.ForeignKey("Publication")
    tagged = models.ForeignKey("User", related_name="tagged")

    def __str__(self):
        return "Tag(" + ", ".join([self.user.__str__()  +  self.tagged.__str__() + self.publication.__str__()]) + ")"

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
