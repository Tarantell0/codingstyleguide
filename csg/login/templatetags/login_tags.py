from django import template
from reputations.models import Reputation

from django.contrib.auth.models import User


register = template.Library()

def login_finder(context):

    user_logged = {}
    if context['request'].user.is_authenticated():
        user_logged['user'] = context['request'].user
        user_logged['reputation'] = Reputation.objects.total(context['request'].user)
    else:
        user_logged['user'] =  None
    user_logged['path'] = context['request'].path
    
 
    return user_logged

register.inclusion_tag("login/header.html", takes_context=True)(login_finder)
