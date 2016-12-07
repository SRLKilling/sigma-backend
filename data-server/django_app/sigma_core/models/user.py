from django.db import models
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
        Modelize an sigma user.
        Invitation can be issued both by the invitee and the inviter (depending on the group settings)
        Invitation have a short life-time.
        As soon as someone accepts or declines the invitation, the instance is destroyed.
    """
    
    #*********************************************************************************************#
    #**                                       Fields                                            **#
    #*********************************************************************************************#
    
    email = models.EmailField(max_length=254, unique=True) # Users are identified by their email.
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True)

    
    # Required by Django to abstract the User interface
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['lastname', 'firstname']
    objects = UserManager()

    def get_full_name(self):
        return self.lastname + self.firstname

    def get_short_name(self):
        return self.email
    
    def __str__(self):
        return self.email
        
        
    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#
    
    
    def can_retrieve(self, user):
        """ Check whether `user` can retrieve information about the user
            True if you share a group with this user.
        """
        return GroupMember.has_common_memberships(self, user)
    
    def can_update(self, user):
        """ Check wheter `user` can update the user profile.
            A user can only edit its own profile """
        return self == user
        


    # Perms for admin site
    def has_perm(self, perm, obj=None): # pragma: no cover
        return True

    def has_module_perms(self, app_label): # pragma: no cover
        return True
