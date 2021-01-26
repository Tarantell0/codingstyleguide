from django import template
from notifications.models import Notification

register = template.Library()

def user_notification(context):
    if context['request'].user.is_authenticated():
        notifications = Notification.objects.filter(
            login=context['request'].user,
            is_seen=False,
            )
        user_id = context['request'].user.id
        return {'notifications':notifications, 'user_id':user_id}
    else: 
        return None


def update_as_seen(context, notification):
#    ns = notifications.filter(is_seen=False)[:10]
#
#    for n in ns:
#        n.is_seen = True 
#        n.save()
    if not notification.is_seen:
        notification.is_seen = True
        notification.save()

    return ""
    
    #raise Exception(ns)

register.inclusion_tag('notifications/notification_header.html',takes_context=True)(user_notification)
register.simple_tag(takes_context=True)(update_as_seen)

