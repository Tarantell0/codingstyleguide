from django.contrib import admin
from tags.models import Tag,  Language #, EditedTag,TagRelatedNames,

admin.site.register(Tag)
admin.site.register(Language)

