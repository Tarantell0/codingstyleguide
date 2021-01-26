from django.conf.urls import patterns, include, url
from csg.views import signup, login_view, logout_view, front_user, edit_user, welcome_view
from csg.views import perma_convention, post_convention
from csg.views import edit_convention, revision_convention
from csg.views import frontpage, front_conventions_tagged
from csg.views import toggle_vote, toggle_favorite, toggle_comment, toggle_comment_vote 
from csg.views import toggle_delete_comment, toggle_update_comment
from csg.views import search_machine, search_duplicate
from csg.views import hot_conventions, unvoted
from csg.views import about, users, favorites, flag, duplicate
from csg.views import similar_convention 
from csg.views import notifications_user
from csg.views import toggle_rm_welcome
from csg.views import show_404
from csg.views import blog, perma_blog
from csg.views import most_popular

from forms import AddConventionForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^/?(?:.json)?$', frontpage, name='frontpage'),

    url(r'^404/$', show_404, name="show_404"),

    url(r'^blog/$',blog, name='blog'),
    url(r'^article/(?P<offset>\d+)/(?P<slug>[-\w]+)/?(?:.json)?$', perma_blog, name='perma_blog'),
    url(r'^article/(\d+)/?(?:.json)?$', perma_blog, name='perma_blog'),

    url(r'^join/$',signup, name='lg_signup'),
    url(r'^login/$',login_view, name='lg_login'),
    url(r'^logout/$',logout_view, name='lg_logout'),
    url(r'^welcome/$',welcome_view, name='welcome'),

    url(r'^user/(\d+)/$', front_user, name="lg_info"),
    url(r'^user/edit/(\d+)/$', edit_user, name="lg_edit"),
    url(r'^user/notifications/(\d+)/$', notifications_user, name="lg_notifications"),
    url(r'^post/guideline/$', post_convention, name='cv_post'),
    #url(r'^language/(?P<offset>\d+)/(?P<slug>[-\w]+)/?(?:.json)?$', front_conventions_tagged, name='cv_tagged'),
    #url(r'^language/(\d+)/?(?:.json)?$', front_conventions_tagged, name='cv_tagged'),
    #url(r'^l/(\d+)/?(?:.json)?$', front_conventions_tagged, name='cv_tagged_shortener'),

    url(r'^lang/(?P<offset>\d+)/(?P<slug>[-\w]+)/?(?:.json)?$', front_conventions_tagged, name='cv_tagged'),
    url(r'^lang/(\d+)/?(?:.json)?$', front_conventions_tagged, name='cv_tagged'),
    url(r'^lang/(?P<slug>[-\w]+)$', front_conventions_tagged, name='cv_tagged'),    
    url(r'^language/(?P<offset>\d+)/(?P<slug>[-\w]+)/?(?:.json)?$', front_conventions_tagged),
    url(r'^language/(\d+)/?(?:.json)?$', front_conventions_tagged),
    url(r'^language/(?P<slug>[-\w]+)$', front_conventions_tagged),
    #url(r'^(?P<slug>[-\w]+)/(?P<offset>\d+)/?(?:.json)?$', front_conventions_tagged, name='cv_tagged'),
    #url(r'^(\d+)/?(?:.json)?$', front_conventions_tagged, name='cv_tagged_shortener'),

    url(r'^guideline/(?P<offset>\d+)/(?P<slug>[-\w]+)/?(?:.json)?$', perma_convention, name="cv_perma"),
    url(r'^guideline/(\d+)/?(?:.json)?$', perma_convention, name="cv_perma"),
    url(r'^g/(\d+)/?(?:.json)?$', perma_convention, name="cv_perma_shortener"),
    url(r'^style/(?P<offset>\d+)/(?P<slug>[-\w]+)/?(?:.json)?$', perma_convention, name="cv_perma"),
    url(r'^style/(\d+)/?(?:.json)?$', perma_convention, name="cv_perma"),
    url(r'^s/(\d+)/?(?:.json)?$', perma_convention, name="cv_perma_shortener"),
    #url(r'^g/(\d+)/?(?:.json)?$', perma_convention, name="cv_perma_shortener"),
    
    #url(r'^guideline/(?P<id>\d+)/(?P<slug>[-\w]+)/$', perma_convention, name="cv_perma"),
    url(r'^guideline/edit/(\d+)$', edit_convention, name="cv_edit"),
    url(r'^guideline/revision/(\d+)$', revision_convention, name="cv_revision"),
    url(r'^guidelines/(\d+)/similar/?(?:.json)?$', similar_convention, name="cv_similar"),
    
    url(r'^toggle_vote/$', toggle_vote, name="cv_toggle_vote"),
    url(r'^toggle_comment_vote/$', toggle_comment_vote, name="cv_toggle_comment_vote"),
    url(r'^toggle_favorite/$', toggle_favorite, name="cv_toggle_favorite"),
    url(r'^toggle_comment/$', toggle_comment, name="cv_toggle_comment"),
    url(r'^toggle_delete_comment/$', toggle_delete_comment, name="cv_toggle_delete_comment"),
    url(r'^toggle_update_comment/$', toggle_update_comment, name="cv_toggle_update_comment"),
    url(r'^toggle_rm_welcome', toggle_rm_welcome, name="rm_welcome"),

    url(r'^search/', search_machine),
    url(r'^search_duplicate/', search_duplicate, name="search_duplicate"),

    url(r'^hot/?(?:.json)?$', hot_conventions, name="cv_hot"),
    url(r'^top/?(?:.json)?$', most_popular, name="most_popular"),
    url(r'^unvoted/?(?:.json)?$', unvoted, name="cv_unvoted"),
    url(r'^favorites', favorites, name="favorites"),
    url(r'^flag/', flag, name="flag"),
    url(r'^duplicate/', duplicate, name="duplicate"),
    url(r'^users', users, name="users"),

    url(r'^about', about, name="about"),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^user/password/reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/user/password/reset/done/'}, 
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/user/password/done/'}),
    url(r'^user/password/done/$', 
        'django.contrib.auth.views.password_reset_complete'),
)
