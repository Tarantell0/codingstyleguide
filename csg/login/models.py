from django.db import models
from datetime import date

from django.contrib.auth.models import User

class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        return self.model._default_manager.create(username=username)

class Login(models.Model):

    username = models.CharField(max_length=30, unique=True, db_index=True)
    password = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    def is_authenticated(self):
        return True 

    def inactive_username(self):
        return "user%d%d%d" % (self.id, self.creation_date.year, self.creation_date.month)
    
    def __unicode__(self):
        return u'%s %s %s' % (self.username, self.email, self.creation_date)

    class Meta(object):
        verbose_name_plural = "Login"


class LoginInfo(models.Model):
    #real_name = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    #twitter = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    #about_me = models.TextField(null=True, blank=True)
    login = models.OneToOneField(User, primary_key=True)

    def __unicode__(self):
        return self.login.username

    def age(self):
        if not self.birthday:
            return None

        today = date.today() 
        try: 
            birthday = self.birthday.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.birthday.replace(year=today.year, day=self.birthday.day-1)

        if birthday > today:
            return today.year - self.birthday.year - 1
        else:
            return today.year - self.birthday.year
