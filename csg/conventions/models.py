from django.db import models
#from login.models import Login
from datetime import datetime, timedelta
#from languages.models import Language
from tags.models import Tag
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


def today():
    """
    Just relevant for checking updates in one day. So isn't functional for the web
    """
    now = datetime.now()
    start = datetime.min.replace(year=now.year, month=now.month, day=now.day)
    end = (start + timedelta(days=1)) - timedelta.resolution
    return start, end


class CommonConventionInfo(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    login = models.ForeignKey(User)
    tag = models.ForeignKey(Tag)

    class Meta:
        abstract = True

class Convention(CommonConventionInfo):
    slug = models.SlugField(max_length=80, blank=True)

    def __unicode__(self):
        return "%d %s by %s" % (self.id, self.creation_date, self.login)

    def save(self, *args, **kwargs):
        if not self.id:
            #url_path = "%s/%s" % (self.id, self.slug)
            url = "%s %s" % (self.tag.name, self.title)
            self.slug = slugify(url)
        super(Convention, self).save(*args, **kwargs)


class Comment(models.Model):
    login = models.ForeignKey(User)
    convention = models.ForeignKey(Convention)
    comment = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "comment by %s in convention id %d " % (self.login, self.convention.pk )


class EditManager(models.Manager):

    def is_edited(self, convention):
        edit = Edit.objects.filter(convention=convention)
        if edit:
            return True
        return False


class Edit(CommonConventionInfo):
    convention = models.ForeignKey(Convention)
    latest = models.BooleanField(default=True)
    objects = EditManager()

    def __unicode__(self):
        return "%d edited by %s" % (self.convention.id, self.login.username)

    def save(self, **kwargs):
        #start, end = today()
        #Edit.objects.filter(latest=True, convention=self.convention.id).filter(
        #    creation_date__range=(start, end)).update(latest=False)
        
        Edit.objects.filter(latest=True, convention=self.convention.id).update(latest=False)

        super(Edit, self).save(**kwargs)


class FlagManager(models.Manager):
    def is_flag(self, convention, login):
        return self.get_query_set().filter(convention=convention, login=login)[0].flag


class Flag(models.Model):
    flag = models.BooleanField(default=False)
    is_convention = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    convention = models.ForeignKey(Convention)
    convention_duplicate = models.ForeignKey(Convention, related_name="flag_convention_duplicate", blank=True, null=True)
    login = models.ForeignKey(User)

    objects = FlagManager()

    def __unicode__(self):
        return "Flag: %d %s" % (self.flag, self.creation_date)


class Duplicate(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    convention = models.ForeignKey(Convention)
    duplicated = models.ForeignKey(Convention, related_name="duplicate_duplicated")
    login = models.ManyToManyField(User)

    def __unicode__(self):
        return "Duplicate: %d date: %s" % (self.convention.id, self.creation_date)


class FavoriteManager(models.Manager):
    def is_favorite(self, convention, login):
        return self.get_query_set().filter(convention=convention, login=login)[0].favorite


class Favorite(models.Model):
    favorite = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    convention = models.ForeignKey(Convention)
    login = models.ForeignKey(User)

    objects = FavoriteManager()

    def __unicode__(self):
        return "Favorite: %d %s" % (self.favorite, self.creation_date)


class VoteCommentManager(models.Manager):
    def up_votes(self, comment):
        return self.get_query_set().filter(comment=comment, up=True).count()
    
    def total_votes(self, comment):
        return self.up_votes(comment)


class VoteComment(models.Model):
    up = models.BooleanField(default=False)
    down = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, blank=True, null=True)
    login = models.ForeignKey(User)
    latest = models.BooleanField(default=True)
    
    objects = VoteCommentManager()

    def save(self, **kwargs):
        VoteComment.objects.filter(latest=True, comment=self.comment, login=self.login).update(latest=False)
        super(VoteComment, self).save(**kwargs)
    
    def __unicode__(self):
        return "%s, up: %d latest: %d" % (
            self.login.username, 
            self.up, 
            self.latest
        )


class VoteManager(models.Manager):
    def up_votes(self, convention):
        return self.get_query_set().filter(convention=convention, up=True).count()

    def down_votes(self, convention):
        return self.get_query_set().filter(convention=convention, down=True).count()
    
    def total_votes(self, convention):
        return self.up_votes(convention) - self.down_votes(convention)


class Vote(models.Model):
    up = models.BooleanField(default=False)
    down = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    convention = models.ForeignKey(Convention, blank=True, null=True)
#    edit = models.ForeignKey(Edit, blank=True, null=True)
#    favorite = models.ForeignKey(Favorite, blank=True, null=True)
#    comment = models.ForeignKey(Comment, blank=True, null=True)

    login = models.ForeignKey(User)
    latest = models.BooleanField(default=True)

    objects = VoteManager()

    def save(self, **kwargs):
        Vote.objects.filter(latest=True, convention=self.convention, login=self.login).update(latest=False)
        super(Vote, self).save(**kwargs)
    
    def __unicode__(self):
        return "%s, up: %d down: %d latest: %d" % (
            self.login.username, 
            self.up, 
            self.down,
            self.latest
        )
