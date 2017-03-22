from django.db import models
from sigma_api.importer import load_ressource

Search = load_ressource("Search")

class SearchQuerySet(models.QuerySet):
    pass


class Search(models.Model):
    """
        fantom
    """
    objects = SearchQuerySet.as_manager()
    
    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#

    def can_print_list(self, user):
        return True
