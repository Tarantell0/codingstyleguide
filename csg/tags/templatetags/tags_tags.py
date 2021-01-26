from django import template
from tags.models import Tag

def nav_taglist():
    tags = Tag.objects.all().order_by('name')
    return {'tags' : tags}


register = template.Library()
register.inclusion_tag('tags/sidebar_tags.html')(nav_taglist)

