from django.db import models
from sigma_api.importer import load_ressource

GroupMember = load_ressource("GroupMember")
Publication = load_ressource("Publication")

class SharedPublicationQuerySet(models.QuerySet):

    def sort(self):
        return self.order_by('-date')

    def in_group(self, group):
        return self.filter(group=group).filter(approved=True)

    def visible_by_user(self, user):
        membersof = GroupMember.objects.for_user(user).values('group')
        return self.approved().filter(group__pk__in = membersof)

    def approved(self):
        return self.filter(approved = True)

    def to_approve(self):
        return self.filter(approved = False)

    def publication_which_group(self, publication):
        return self.filter(publication = publication)

class SharedPublication(models.Model):

    objects = SharedPublicationQuerySet.as_manager()

    publication = models.ForeignKey("Publication", related_name='shared')

    group = models.ForeignKey("Group", related_name='shared_publications')
    approved = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "SharedPublication(" + ", ".join[(self.publication.__str__(), self.group.__str__(), self.approved, self.date.__str__()]) + ")"
        return self.publication.title

    @staticmethod
    def post_internal(user, group, title, content, event = 0):
        pub = Publication.model(group = group, author = user, title = title, content = content)
        if event:
            pub.related_event = event
        pub.save()
        pub.share(group)
        return pub

    def can_retrieve(self, user):
        return True
