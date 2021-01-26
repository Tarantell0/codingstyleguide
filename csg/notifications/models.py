from django.db import models
from django.contrib.auth.models import User
from conventions.models import Convention

# Create your models here.

class Notification(models.Model):
    login = models.ManyToManyField(User)
    supporter = models.ForeignKey(User, related_name="notification_supporter", blank=True, null=True)
    convention = models.ForeignKey(Convention, blank=True, null=True)
    extra_info = models.CharField(max_length=255, blank=True, null=True)
    is_seen = models.NullBooleanField(default=False, blank=True, null=True)
    is_comment = models.NullBooleanField(default=False, blank=True, null=True)
    is_vote_up = models.NullBooleanField(default=False, blank=True, null=True)
    is_remove_up = models.NullBooleanField(default=False, blank=True, null=True)
    is_vote_down = models.NullBooleanField(default=False, blank=True, null=True)
    is_remove_down = models.NullBooleanField(default=False, blank=True, null=True)
    is_edit = models.NullBooleanField(default=False, blank=True, null=True)
    is_other = models.NullBooleanField(default=False, blank=True, null=True)
    header_for_other = models.CharField(max_length=255, blank=True, null=True)
    url_for_other = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "to %s by %s" % (self.login, self.supporter)

