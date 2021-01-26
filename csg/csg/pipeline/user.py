from login.models import LoginInfo
from reputations.models import Reputation
from notifications.models import Notification
from csg.views import PTS_WELCOME

def user_details(strategy, details, response, user=None, *args, **kwargs):
    if kwargs['is_new']:

        if strategy.backend.__class__.__name__ == 'FacebookOAuth2' or strategy.backend.__class__.__name__ == 'TwitterOAuth' or strategy.backend.__class__.__name__ == 'GithubOAuth2': 

            login_info = LoginInfo.objects.create(
                login=user,
                website='',
                location='')
            login_info.save()
            Reputation.objects.create(login=user, points=PTS_WELCOME)

            notification = Notification.objects.create(
                supporter=user,
                extra_info = "Thanks for joining us...")
            notification.login.add(user)


#    else:
#        pass

