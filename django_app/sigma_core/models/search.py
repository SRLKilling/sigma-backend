from django.db import models
from sigma_api.importer import load_ressource
import time

Search = load_ressource("Search")
Group = load_ressource("Group")
User = load_ressource("User")
Event = load_ressource("Event")

class Search(models.Model):

    #*********************************************************************************************#
    #**                                    Permissions                                          **#
    #*********************************************************************************************#

    def levenshtein_distance(self, a, b):
        n = len(a)
        m = len(b)

        c_effacement = 1
        c_insertion = 1
        c_substitution = 2

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

    def minimal_distance(self, s, object_name):
        #s : words written in the search bar
        #object_name : one of the possibility

        words = s.split()
        words_object = object_name.split()

        score = 0 #sum
        for w in words:
            mini = levenshtein_distance(w,words_object[0])
            best_word = words_object[0]
            for o in words_object:
                if levenshtein_distance(w, o)<mini:
                    best_word=o
                    mini = levenshtein_distance(w, o)
            score+=mini
        return score


    def can_print_list(self, user):
        return True

    # def users(user, s):
    #     t=time.time()
    #     words = s.split(" ")
    #     l = User.objects.get_visible_users(user)
    #     for x in words:
    #         a = l.filter(firstname__contains = x)
    #         b = l.filter(lastname__contains = x)
    #         l = a | b
    #     print(time.time()-t)
    #     return l

    #Pre-filter :  eliminate absurd candidates
    def users(user, s):
        words = s.split(" ")
        l = User.objects.get_visible_users(user)
        for x in words:
            if len(x)>=3:
                    a = l.filter(firstname__contains = x[0:3])
                    b = l.filter(lastname__contains = x[0:3])
                    l = a | b
        return l

    #Pre-filter : eliminate absurd candidates
    def groups(user, s):
        words = s.split(" ")
        l = Group.objects.user_can_see(user)
        for x in words:
            if len(x)>=3:
                    l=l.filter(name__contains = x[0:3])
        return l

    # def groups(user, s):
    #     words = s.split(" ")
    #     l = Group.objects.user_can_see(user)
    #     for x in words:
    #         a = l.filter(name__contains = x)
    #         b = l.filter(description__contains = x)
    #         l = a | b
    #     return l

    # def events(user, s):
    #     words = s.split(" ")
    #     l = Event.objects.visible_by_user(user)
    #     for x in words:
    #         a = l.filter(name__contains = x)
    #         b = l.filter(description__contains = x)
    #         c = l.filter(place_name__contains = x)
    #         l = a | b | c
    #     return l

    def events(user, s):
        words = s.split(" ")
        l = Event.objects.visible_by_user(user)
        for x in words:
            if len(x)>=3:
                a = l.filter(name__contains = x[0:3])
                b = l.filter(place_name__contains = x[0:3])
                l = a | b
        return l
