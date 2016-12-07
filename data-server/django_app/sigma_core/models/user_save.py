from django.db import models
from django.db.models import Q

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# TODO : Add unique username for frontends URLs

# Basic user manager required by Django
class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset()

    def create_user(self, email, lastname, firstname, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model( email=self.normalize_email(email), lastname=lastname, firstname=firstname )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, lastname, firstname, password):
        user = self.create_user(email, lastname, firstname, password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    """
    User are identified by their email. Lastname and firstname are required.
    """
    email = models.EmailField(max_length=254, unique=True)
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=128)
    # username = models.CharField(max_length=128, unique=True) # TODO - Add unique username for frontend URLs
    phone = models.CharField(max_length=20, blank=True)
    photo = models.CharField(max_length=20, default = 'img/4.jpg')

    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)
    join_date = models.DateTimeField(auto_now_add=True)

    #difference between superuser and staff ?
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()

    #invited_to_groups is to delete, or we have to make a through="GroupInvitation" attribute
    invited_to_groups = models.ManyToManyField('Group', blank=True, related_name="invited_users");

    #what is the purpose of that line if "memberships" already exist ?
    groups = models.ManyToManyField('Group', through='GroupMember', related_name='users')

    # Related fields:
    #   - memberships (model GroupMember)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return "{} {}".format(self.lastname, self.firstname)

    def get_short_name(self):
        return self.email

    def is_sigma_admin(self):
        return self.is_staff or self.is_superuser

    def has_common_group(self, user):
        """
        Return True iff self has a group in common with user.
        Warning: non symmetric function! u1.has_common_group(u2) may be different of u2.has_common_group(u1)
        """
        # We are really in the same group if you ARE really in the group.
        # But, on the other hand, you can "see" pending request of other members.
        return len(set(self.memberships.values_list('group', flat=True)).intersection(user.memberships.all().values_list('group', flat=True))) > 0

    def get_group_membership(self, group):
        from sigma_core.models.group_member import GroupMember
        from sigma_core.models.group import Group
        try:
            return self.memberships.get(group=group)
        except GroupMember.DoesNotExist:
            return None

    def is_group_member(self, g):
        from sigma_core.models.group_member import GroupMember
        mem = self.get_group_membership(g)
        return mem is not None

    def can_invite(self, group):
        from sigma_core.models.group_member import GroupMember
        mem = self.get_group_membership(group)
        return mem is not None and mem.can_invite

    def can_accept_join_requests(self, group):
        # Considered that someone who can invite can also accept join requests
        from sigma_core.models.group_member import GroupMember
        if self.is_sigma_admin():
            return True
        mem = self.get_group_membership(group)
        return mem is not None and mem.can_invite

    def can_modify_group_infos(self, group):
        from sigma_core.models.group_member import GroupMember
        mem = self.get_group_membership(group)
        return mem is not None and mem.can_modify_group_infos

    def has_group_admin_perm(self, group):
        from sigma_core.models.group_member import GroupMember
        from sigma_core.models.group import Group
        if self.is_sigma_admin():
            return True
        mem = self.get_group_membership(group)
        return mem is not None and (mem.is_administrator or mem.is_superadministrator)

    def is_invited_to_group_id(self, groupId):
        return self.invited_to_groups.filter(pk=groupId).exists()

    def get_groups_with_confirmed_membership(self):
        from sigma_core.models.group_member import GroupMember
        return GroupMember.objects.filter(Q(user=self)).values_list('group', flat=True)


    # is_related_to(user, group)
    # Check if a user is related to a group by recursively checking if it is a member of the group, or related to the parent groups
    def is_related_to(group):
        already_checked = []
        def rec(group):
            try:
                GroupMember.objects.get(group=group.id, user=self.id)
                return True
            except GroupMember.DoesNotExist:
                parents = group.group_parents_list()
                for p in parents:
                    if not p.id in already_checked:
                        if rec(p):
                            return True
                already_checked.insert(group.id)
                return False

        if type(group) == int:
            group = Group.objects.get(id=group)
        return rec(group)



    ###############
    # Permissions #
    ###############

    # Perms for admin site
    def has_perm(self, perm, obj=None): # pragma: no cover
        return True

    def has_module_perms(self, app_label): # pragma: no cover
        return True
