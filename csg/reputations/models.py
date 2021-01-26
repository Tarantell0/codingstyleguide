from django.db import models
#from login.models import Login
from conventions.models import Convention, Comment

from django.contrib.auth.models import User

class Supporter(models.Model):
    login = models.ForeignKey(User)

    def __unicode__(self):
        return self.login

class ReputationManager(models.Manager):
    
    def total(self, login):
        reputations = self.get_query_set().filter(login=login)
        total = 0
        for reputation in reputations:
            total += reputation.points
        return total

class Reputation(models.Model):
    points = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    supporter = models.ForeignKey(User, related_name="login_supporter", blank=True, null=True)
    convention = models.ForeignKey(Convention, blank=True, null=True)
    #comment = models.ForeignKey(Comment, blank=True, null=True)
    login = models.ForeignKey(User)

    objects = ReputationManager()

    def __unicode__(self):
        return "%d points %s, %s" % (self.points, self.login, self.convention)

    def Meta(object):
        verbose_name_plural = "Reputation"
