from django.db import models
from sigma_api.importer import load_ressource

Search = load_ressource("Search")
Group = load_ressource("Group")
User = load_ressource("User")
Event = load_ressource("Event")

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

    def levenshtein_distance(self, a, b):
        n = len(a)
        m = len(b)

        c_effacement = 1
        c_insertion = 1
        c_substitution = 1

        d = [[0 for k in range(m + 1)] for k in range(n + 1)]
        for i in range(n + 1):
            d[i][0] = i
        for j in range(m + 1):
            d[0][j] = j

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                c_substitution_local = c_substitution
                if a[i-1] == b[j-1]:
                    c_substitution_local = 0
                r = d[i-1][j] + c_effacement
                r = min(r, d[i][j-1] + c_insertion)
                r = min(r, d[i-1][j-1] + c_substitution_local)
                d[i][j] = r
        return d[n][m]

    def can_print_list(self, user):
        return True

    def user(self, s):
        if len(s) >= 2:
            words = s.split(" ")
            l = Group.objects
            for x in words:
                a = l.filter(firstname__contains(x))
                b = l.filter(lastname__contains(x))
                l = a | b
            return l
        else:
            return []
