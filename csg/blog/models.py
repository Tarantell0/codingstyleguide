from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Blog(models.Model):
    login = models.ForeignKey(User)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=80)
    slogan = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return "article %s by %s" % (self.title, self.login)

    def save(self, *args, **kwargs):
        if not self.id:
            #url_path = "%s/%s" % (self.id, self.slug)
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)
