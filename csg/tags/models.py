# Tags could be anything that hast to be with reference.
# for example: Language, Frameworks 

from django.db import models
#from login.models import Login

from django.contrib.auth.models import User

from datetime import datetime, timedelta
from django.template.defaultfilters import slugify

def today():
    now = datetime.now()
    start = datetime.min.replace(year=now.year, month=now.month, day=now.day)
    end = (start + timedelta(days=1)) - timedelta.resolution
    return start, end


class CommonTagInfo(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    login = models.ForeignKey(User)

    class Meta:
        abstract = True


class Tag(CommonTagInfo):
    slug = models.SlugField(max_length=80, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
       if not self.id:
           self.slug = slugify(self.name)
       super(Tag, self).save(*args, **kwargs)
   

#class TagRelatedNames(models.Model):
#    tag = models.ForeignKey(Tag)
#    name = models.CharField(max_length=254)

#    def __unicode__(self):
#        return self.name


class EditedTagManager(models.Manager):
    def is_edited(self, tag):
        edit = EditedTag.objects.filter(tag=tag)
        if edit:
            return True
        return False

# To the first version, edit a tag is not allowed, this class must be deleted
class EditedTag(CommonTagInfo):
    tag = models.ForeignKey(Tag)
    latest = models.BooleanField(default=True)
    objects = EditedTagManager()

    def __unicode__(self):
        return "tag %s latest %d" % (self.tag, self.latest)

    def save(self, **kwargs):
        start, end = today()
        EditedTag.objects.filter(latest=True, tag=self.tag).filter(
            creation_date__range=(start, end)).update(latest=False)
        super(EditedTag, self).save(**kwargs)


class Language(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
