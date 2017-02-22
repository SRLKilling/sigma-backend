from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from sigma_api.importer import load_ressource

UserConnection = load_ressource("UserConnection")

# TODO : Add unique username for frontends URLs


# Basic user manager required by Django
class UserManager(BaseUserManager):
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
        user.is_staff = True
        user.save()
        return user



class UserQuerySet(models.QuerySet):

    def get_visible_users(self, user):

        #without user_connection
        #groups_qs = Group.user_can_see(user)
        #return User.filter(groupMember__group__in = group_qs)

        user_connections_qs = UserConnection.objects.connections_to(user)
        return self.filter(userconnection__in = user_connections_qs)


class User(AbstractBaseUser):
    """
        Modelize an sigma user.
        Invitation can be issued both by the invitee and the inviter (depending on the group settings)
        Invitation have a short life-time.
        As soon as someone accepts or declines the invitation, the instance is destroyed.
    """

    objects = BaseUserManager.from_queryset(UserQuerySet)

    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#

    email = models.EmailField(max_length=254, unique=True) # Users are identified by their email.
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=128)

    join_date = models.DateTimeField(auto_now_add=True)

    school = models.ForeignKey('Group', related_name='school')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)


    # Required by Django to abstract the User interface

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['lastname', 'firstname']
    objects = UserManager()

    def get_full_name(self):
        return self.lastname + self.firstname

    def get_short_name(self):
        return self.email

    # A modifier !
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email


    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#


    def can_retrieve(self, user):
        """ Check whether `user` can retrieve information about the user
            True if you share a group with this user.
        """
        return True
        #return UserConnection.model.are_users_connected(self, user) or GroupMember.has_common_memberships(self, user)

    def can_update(self, user):
        """ Check wheter `user` can update the user profile.
            A user can only edit its own profile """
        return self == user
