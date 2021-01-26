# coding=utf-8
"""
#GENERAL TODOs
UNVOTED IS SINCE 25th FEB REMOVED TO THE USER, BUT STILL ACCESSIBLE THROUGH .com/unvoted/
"""
from login.models import LoginInfo #, Login
from reputations.models import Reputation
from tags.models import Tag, Language #TagRelatedNames 
from notifications.models import Notification
from conventions.models import Convention, Vote, Favorite, Edit, Comment, Flag, Duplicate, VoteComment
from blog.models import Blog
from forms import AddConventionForm, EditConventionForm, SignupForm

from haystack.query import SearchQuerySet

from django.shortcuts import render, get_object_or_404 #, render_to_response 
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.utils.timezone import utc
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.sessions.models import Session
#from django.utils import simplejson
from django.core.cache import cache

from django.utils.http import urlquote

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime, timedelta
#import datetime
import re
import random
import string
import hashlib
import hmac
import json
import ghdiff
import markdown2
import json

PTS_WELCOME = 1
PTS_POST = 2
PTS_CONVENTION_POS = 5
PTS_CONVENTION_NEG = -2

MIN_PTS_TO_EDIT = 50
MIN_PTS_TO_VOTE_POS = 10
MIN_PTS_TO_VOTE_NEG = 40
MIN_PTS_TO_COMMENT = 0
MIN_PTS_TO_POST = 0
MIN_PTS_TO_ADD_NEW_LANG = 0
MIN_PTS_TO_FLAG = 0
MAX_ROWS_TO_DISPLAY = 50
MAX_POPULAR = 20
MAX_ROWS_TO_PAGE = 36 # Sandis (lovely girlfriend) age 15. Feb 2014
MAX_COMMUNITY_PROFILES = 50


def perma_blog(request, offset, slug=" "):
    
    #post = Blog.objects.all().filter(id=offset)
    post = Blog.objects.filter(id=offset)
    if not post:
        raise Http404
    
    if slug != post[0].slug:
        next = reverse('perma_blog', args=(post[0].id,post[0].slug,))
        return HttpResponseRedirect(next)

    return render(request, 'blog.html', {"posts":post})


def blog(request):
    posts = Blog.objects.all().order_by("-creation_date")
    return render(request, 'blog.html', {"posts":posts})


def show_404(request):
    return render(request, '404.html')


def welcome_view(request):
    if not request.user.is_authenticated():
        raise Http404

    text="""
> “You have to learn the rules of the game. And then you have to play better than anyone else.” - A. Einstein

Every single one of us wants their work to add up to something. We provide a platform for you to continuously improve your code. The kind of code that has your fingerprints all over it.

Simultaneously,  with your expertise you can give back to other developers, and together make a better coding world.

Play well with others and enjoy your stay! 

Thank you for helping Coding Style Guide be Coding Style Guide.
    """
    return render(request, 'welcome.html', {'text':text, 'hide_leftside_menu':True})


def about(request):
    """
    It displays the about page: 
        1. What I believe
        2. What are the goals
        3. How it works
        4. For whom is that page for
    """
    text="""

# ABOUT #

* * *

Coding Style Guide is a community-driven reference site. To make your code universally readable it collects and provides programming guidelines for lots of programming languages. We try hard to make it simple to use, so you can easily adapt your code to the guideline that is most convenient for you.

Coding Style Guide is currently in beta version. We are continously improving this site to provide you a great product.

Coding Style Guide is totally free and doesn't require any registration.

# GOAL #

* * *

The mission of our project is to help and support developers by creating an outright platform to find guidelines such as rules, techniques, standards, conventions and styles. For every matter with writing readable code, we want to provide a quick and applicable solution.

We strongly believe that writing and reading code should be simple for every developer. However, only if all of us apply similar guidelines and techniques. Nowadays, there are lots of polyglots programming for too many different platforms. This makes it  almost impossible to constantly remember the conventions for every single language. That's why we want to establish a quick and simple reference tool, enabling you to find the perfect guideline as quick as possible.

To fill this project with life and make it sustainable is not an easy task. This can only be accomplished if the community collaborates with sharing knowledge and experience. Being critical by voting what's hot and what's not will help us to filter the most convenient entries.

The result will be a tool for everyone who wants to improve their own coding styles. So feel free to stop by anytime, find everything you need for your code, post what you found most practicable in your coding life.

# HOW IT WORKS #

* * *

The cool thing is that you have reading access to all the guidelines without registration.

But... once you registered, this is what you can do after having collected enough reputation points:
"""

    table="""
<table>
    <tr><th>Powers</th><th>Min. points required</th></tr>
    <tr><td>add new guideline</td><td>0</td></tr>
    <tr><td>vote up</td><td>10</td></tr>
    <tr><td>vote down</td><td>40</td></tr>
    <tr><td>edit</td><td>0</td></tr>
    <tr><td>comment</td><td>0</td></tr>
    <tr><td>flag an entry</td><td>0</td></tr>
</table>
<br>
And this is how you get those reputation points:
<br>
<table>
    <tr><th>Earnings</th><th>Reputation points</th></tr>
    <tr><td>registration</td><td>+ 1</td></tr>
    <tr><td>add new guideline</td><td>+ 2</td></tr>
    <tr><td>receiving up vote</td><td>+ 5</td></tr>
    <tr><td>receiving down vote</td><td>- 2</td></tr>
</table>
<br>
"""

    second_part = """
# DEVELOPER API #

* * *

We are also working hard trying to make the internet suck less. We have implemented an API to allow your apps to communicate with Coding Style Guide. You just have to call an url ending with '.json'. These are the available urls: 

*  Homepage

    `http://codingstyleguide.com/.json`

*  Programming language

    `http://codingstyleguide.com/language/3/python.json`
    
    `#3 is an example for a language id`

*  Permalink

    `http://codingstyleguide.com/guideline/59/yoda-conditions.json`
    
    `#59 is an example for a guideline id`

*  Similar guidelines

    `http://codingstyleguide.com/guidelines/3/similar.json`
    
    `#3 is an example for a guideline id`

*  Hot
    
    `http://codingstyleguide.com/hot.json`

# FEEDBACK #

* * *

For any feedback, comments or suggestions... or just to say "Hi!", please drop us a line - we will appreciate it!
<diegoloop@me.com>

Code is read more than written - Made with passion in Bamberg, Germany

[@cstyleguide](http://twitter.com/cstyleguide)

"""
    return render(request, 'about.html', {'text':text, 'table':table, 'second_part':second_part, 'hide_leftside_menu':True}) 


def notifications_user(request,offset):
    params = {}
    if not request.user.is_authenticated()  or (request.user.id != int(offset)):
        raise Http404  
    else:
        notifications = Notification.objects.filter(login=request.user).order_by("-creation_date")
        page = 1

        if request.method == "GET":
            page = request.GET.get('page')

        paginator = Paginator(notifications, MAX_ROWS_TO_PAGE)
        try:
            reduce_notifications = paginator.page(page)
        except (PageNotAnInteger, TypeError):
            reduce_notifications = paginator.page(1)
        except (EmptyPage, TypeError):
            reduce_notifications = paginator.page(paginator.num_pages)

        #notifications = Notification.objects.filter(login=request.user).order_by('-creation_date')[:20]
        for notification in reduce_notifications:
            notifications.convention = get_convention_if_edited(notification.convention) 
        params['notifications'] = reduce_notifications 

    params['up_pts'] = PTS_CONVENTION_POS
    params['down_pts'] = PTS_CONVENTION_NEG

    return render(request, 'notifications/user_notifications.html', params)


def search_machine(request):
    """ 
    Using Haystack this function returns the query matches in Convention Model
    """
    results = None
    text = ""
    if request.method == "GET":# and request.GET.get('text'):
        text = request.GET.get('text')
        if text and len(text.split() ) > 0:
            search = SearchQuerySet().all()
            results = search.filter(content=text)
        elif not text:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    return render(request, 'conventions/search.html', {'conventions': results, 'text': text})


def duplicate(request):
    if request.method == "POST":
        duplicate_id = request.POST['duplicate_guide']
        convention_id = request.POST['current_guide']
        
        response = ""
        try:
            to_duplicate = Convention.objects.get(id=duplicate_id)
            convention = Convention.objects.get(id=convention_id)
            if to_duplicate == convention:
                #response = "WRONG: You can't tag the same guideline as duplicate"
                response = "Sorry! But you can't tag the same guideline as duplicate."
            else:
                try:
                    duplicate = Duplicate.objects.get(duplicated=to_duplicate, convention=convention)
                    duplicate.login.add(request.user)
                    duplicate.save()
                    response = "Thank you! Your request has been received. It will be processed after at least 3 users tagged it as duplicate." 
                    #response = "RIGHT: Your request has been succeed" 
                except Duplicate.DoesNotExist:
                    duplicate = Duplicate.objects.create(duplicated=to_duplicate, convention=convention)
                    duplicate.login.add(request.user)
                    duplicate.save()
                    #response = "RIGHT: Your have created a new row for this guideline" 
                    response = "Thank you! Your request has been received. Please note at least 2 more users have to mark it as duplicate to validate it." 
        
        except Convention.DoesNotExist:
            #response = "WRONG: Please enter a valid guideline id"
            response = "Sorry! But we can't find the id you are tagging."
        
        data = json.dumps({'message':'%s' % response})
        return HttpResponse(data, content_type='application/json; charset=utf8')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def search_duplicate(request):
    
    results = None
    text = ""
    data = json.dumps({'':''});
    if request.method == "POST":
        perma_id = request.POST.get('perma_id')
        #if perma_id and len(perma_id.split()) > 0:
        if request.is_ajax():
            #founded_guide = "baam"
            style = ""
            if len(perma_id) > 0:
                style =Convention.objects.filter(id__iexact=perma_id)
            
            try:
                data = json.dumps({'style':'%s' % style[0].title,
                                  'tag': '%s' % style[0].tag.name,
                                  'date': '%s' % style[0].creation_date.strftime("%b %d '%Y, %H:%M"),
                                  'author': '%s' % style[0].login.username,
                                  'votes': '%s' % Vote.objects.total_votes(style[0]) })
            except (IndexError):
                pass

            return HttpResponse(data, content_type='application/json; charset=utf8')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def check_revision_match(a,b):
    
    if a != b:
        return True

    return False


def revision_convention(request, offset):
    """
    This function collects the modifications made, and lists all of them using ghdiff
    """
    convention = get_object_or_404(Convention, id=offset)
    latest_title = ""
    if Edit.objects.is_edited(convention=convention):
        edit = Edit.objects.filter(convention=convention).order_by('-creation_date')[0]
        latest_title = Edit.objects.get(convention=convention,latest=True).title
    else: 
        raise Http404
    versions = Edit.objects.filter(convention=edit.convention).order_by('-creation_date')
 
    descriptions = []
    titles = []
    index =  []
    total_versions = versions.count()
    
    if total_versions <= 1: # 1 will match with latest=True
        if check_revision_match(edit.convention.title, edit.title):
            titles.append(ghdiff.diff(edit.convention.title, edit.title))

        else:
            titles.append(False)

        if check_revision_match(edit.convention.description, edit.description):
            descriptions.append(ghdiff.diff(edit.convention.description, edit.description))
        else:
            descriptions.append(False)
    
    else: # assuming that at least are 2 edited versions
        
        for i in range(total_versions-1):
            index.append( (total_versions+1) - i)
            
            # Because the versions is order_by desc, therefore ghdiff( second_string, first_string )
            if check_revision_match(versions[i+1].title, versions[i].title):
                titles.append( ghdiff.diff(versions[i+1].title, versions[i].title) )
            else: 
                titles.append(False)
            
            if check_revision_match(versions[i+1].description,versions[i].description):
                descriptions.append( ghdiff.diff(versions[i+1].description,versions[i].description) )
            else:
                descriptions.append(False)

        if check_revision_match(edit.convention.description,versions[total_versions-1].description):
            descriptions.append( ghdiff.diff(edit.convention.description,versions[total_versions-1].description) )
        else:
            descriptions.append(False)
        
        if check_revision_match(edit.convention.title, versions[total_versions-1].title):
            titles.append( ghdiff.diff(edit.convention.title,versions[total_versions-1].title) )
        else:
            titles.append(False)
          

    index.append(2) # the count is desc so (2) will be always the last to display

    params={'edit': edit, 'latest_title':latest_title,'subversion': zip(versions,descriptions,titles,index)}

    return render(request, 'conventions/revision.html', params) 


def edit_convention(request, offset):
    """
    This function create a wiki to edit a convention
    Note: Every user that has an account can change any convention and the
    changes will be displayed automatically without a filter. With that say
    we will trust in any logged in user.

    Note: 
        + A title's convention is possible edited if just exist once in the database,
        that means it doesn't have any similar convention jet.
    
    TODO: 
        + Maybe isn't a bad idea to implement a reputation system asking for a 
        minimum points before editing.
        - Following the Wikipedia principle where everyones can edit everything, asking
        for min reputation points is not correct
    """
    convention = get_object_or_404(Convention, id=offset)
    convention = get_convention_if_edited(convention)
    title_editable = True

    if not request.user.is_authenticated():
        url_red_path = '../../../login/?next=/guideline/%s/edit/' % offset
        return HttpResponseRedirect( url_red_path ) 
    
    for_edit = Convention.objects.filter(title=convention.title,tag=convention.tag)
    
    if len(for_edit) > 1:
        title_editable = False
    
    title_msg = ''

    if request.method == 'POST':
        form = EditConventionForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            title = cd['title']
            description = cd['rules_for_naming']

            if (description or title) and (description != convention.description or title != convention.title):
                have_errors = False 

                if title and (not title_editable):
                    have_errors = True
                    title_msg="Sorry! Similar guideline existing, editing this title isn't permitted."
                if not title:
                    title = convention.title

                if (description == convention.description) and (title == convention.title):
                    next = reverse('cv_perma', args=(convention.id,))
                    return HttpResponseRedirect(next)

                if title_editable:
                    if title or description:

                        if title and (title != convention.title):
                            valid_title,title_msg = is_valid_title(title)
                            if not valid_title:
                                have_errors = True
                        elif title and (title == convention.title):
                            title = convention.title

                        if description and (description == convention.description):
                            description = convention.description
                        elif description and (description != convention.description):
                            valid_description,title_msg = is_valid_title(description)
                            if not valid_description:
                                have_errors = True
                                title_msg = 'This guideline description is to short. Please add more information.'
                                
                    elif not title and not description:
                        next = reverse('cv_perma', args=(convention.id,))
                        return HttpResponseRedirect(next)

                if not title_editable:
                    if description and (description == convention.description):
                        description = convention.description
                    elif description and (description != convention.description):
                        valid_description,title_msg = is_valid_title(description)
                        if not valid_description:
                            have_errors = True
                            title_msg = 'This guideline description is to short. Please add more information.'

                if convention.description != description and description == '':
                    have_errors = True
                    title_msg = 'This guideline description is to short. Please add more information.'


                if not have_errors:
                    Edit.objects.create(
                        title=title,
                        convention=convention, 
                        login=request.user, 
                        description=description,
                        tag=convention.tag)
 
                    is_seen = True if request.user == convention.login else False

                    if request.user != convention.login:
                        notification = Notification.objects.create(
                            convention=convention,
                            supporter=request.user,
                            is_edit = True,
                            is_seen = is_seen,
                            extra_info = description[:200])

                        notification.login.add(convention.login)

                else:
                    return render(request, 'conventions/edit.html',{'error_min_char':title_msg,'convention':convention,'is_title_editable':title_editable,'form': form})

            next = reverse('cv_perma', args=(convention.id,))
            return HttpResponseRedirect(next)

    form = EditConventionForm( 
        initial = {'rules_for_naming':convention.description, 'title':convention.title}
    )
    
    return render(request, 'conventions/edit.html',{'convention':convention,'is_title_editable':title_editable,'form': form})


def perma_convention(request, offset, slug=" "):
    """
    This function show the perma convention and comments of a particular convention
    Note: reputation in comment deleted on 10. December 2013
    """
    convention = get_object_or_404(Convention, id=offset)

    if slug != convention.slug:
        next = reverse('cv_perma', args=(convention.id,convention.slug,))
        return HttpResponseRedirect(next)
    
    comments = Comment.objects.filter(convention=convention).order_by('creation_date')

    convention = get_convention_if_edited(convention)

    reputation = Reputation.objects.total(convention.login)
    
    t_votes = Vote.objects.total_votes(convention)
    vote = "+%d" % t_votes if t_votes > 0 else t_votes

    is_flag = False
    is_flag_duplicate = False
    vote_comment = []
    total_comment_votes = []

    if request.user.is_authenticated():
        try:
            is_flag=Flag.objects.get(login=request.user,convention=convention,flag=True, is_convention=True)
            is_flag=True
        except Flag.DoesNotExist:
            is_flag=False

        for comment in comments:
            try:
                VoteComment.objects.get(comment=comment,login=request.user)
                vote_comment.append(True)
                
            except VoteComment.DoesNotExist:
                vote_comment.append(False)
            total_comment_votes.append(VoteComment.objects.up_votes(comment))
    else:
        for c in comments:
            total_comment_votes.append(VoteComment.objects.up_votes(c))
            vote_comment.append(False)

    
    duplos = []
    is_duplicate = False
    duplicated_ids = []
    duplicated_flags = []
    try:
        duplicate = Duplicate.objects.all().filter(convention=convention)
        for d in duplicate:

            duplicated_ids.append(d.duplicated.id)
            for l in d.login.all():
                if request.user == l:
                    is_duplicate = True

            if d.login.count() >= 3:
                duplos.append(d)
            
            #raise Exception(d.duplicated.id)
            if request.user.is_authenticated():
                try:
                    is_flag_duplicate=Flag.objects.get(login=request.user, 
                                                       flag=True, 
                                                       is_duplicate=True,
                                                       convention_duplicate=d.duplicated)
                    duplicated_flags.append(True)
                except Flag.DoesNotExist:
                    duplicated_flags.append(False)


    except Duplicate.DoesNotExist:
        pass


    params = {"convention":convention,
              "total_votes":vote,
              "comments":zip(comments,vote_comment,total_comment_votes),
              "login":request.user,
              "reputation":reputation,
              "is_flag":is_flag, 
              "is_flag_duplicate":is_flag_duplicate, 
              "is_duplicate":is_duplicate, 
              "duplicated_id":",".join(str(x) for x in duplicated_ids), 
              "duplicate":zip(duplos,duplicated_flags)}

    if request.path_info.endswith('json'):
        # the idea to not call zip_wrapper is to not select twice in same models
        return jsonize(convention.title,zip([convention],[reputation],[vote]))
    else:
        return render(request, 'conventions/perma.html', params)


def edit_user(request, offset):
    """
    It shows an editable page for own user information
    """

    login_info = get_object_or_404(LoginInfo, login=offset)
    if not request.user.is_authenticated() or login_info.login != request.user:
        raise Http404
    
    if request.method == "POST":
        user_press_edit = request.POST.get("edit")
        user_press_edit_mail = request.POST.get("edit_mail")
        user_press_edit_log = request.POST.get("edit_log")
        user_press_delete = request.POST.get("delete")

        if user_press_edit:
            return user_pressed_edit(request,login_info)

        if user_press_delete:
            return user_pressed_delete(request)
        
        if user_press_edit_mail:
            return user_pressed_edit_mail(request,login_info)

        if user_press_edit_log:
            return user_pressed_edit_log(request,login_info)

    return render(request, 'login/edit.html', {'login_info':login_info})
    

def front_user(request, offset):
    """
    This function returns the user front page.
    Topics to display:
        1. User Information
        2. Convention posted
        3. Favorite conventions

    Note: 
    Showing Tags that a user has created is removed
    """
    #user_info = get_object_or_404(User, id=offset)
    try: 
        user_info = LoginInfo.objects.get(login=offset)
    except LoginInfo.DoesNotExist:
        raise Http404
    
    #user_info = get_object_or_404(LoginInfo, id=offset)

    if not user_info.login.is_active:
        raise Http404   
    
    is_same_user = request.user == user_info.login

    total_convention_votes = []
    try: 
        conventions = Convention.objects.filter(login=user_info.pk)#user_info.id)
        for c in conventions: 
            c = get_convention_if_edited(c)
            
            t_votes = Vote.objects.total_votes(c)
            vote = "+%d" % t_votes if t_votes > 0 else t_votes
            total_convention_votes.append( vote )
    
    except Convention.DoesNotExist:
        pass 
   
     
    total_fav_votes = []
    try: 
        favorites = Favorite.objects.filter(login=user_info.pk)#user_info)
        for f in favorites: 
            f.convention = get_convention_if_edited(f.convention)

            t_votes = Vote.objects.total_votes(f.convention)
            vote = "+%d" % t_votes if t_votes > 0 else t_votes
            total_fav_votes.append(vote)
    except Favorite.DoesNotExist:
        pass
   
    user_reputation = Reputation.objects.total(user_info.pk)#user_info)

    vote_up_sum = MIN_PTS_TO_VOTE_POS - user_reputation
    vote_up = True if vote_up_sum <= 0 else False #"still %d points to go" %vote_up_sum

    vote_down_sum = MIN_PTS_TO_VOTE_NEG - user_reputation
    vote_down = True if vote_down_sum <= 0 else False# "still %d points to go" %vote_down_sum

    up = miss_up = ""
    if vote_up: 
        up = ', vote up'
    else:
        miss_up = '%d reputation pts. needed to vote up and' % vote_up_sum

    down = miss_down = ""
    if vote_down:
        down = ' and down'
    else:
        miss_down = '%d reputation pts. needed to vote down' % vote_down_sum

    abilities = "Add%s%s, edit, comment and flag on guidelines" % (up, down)
    miss_powers = "%s %s" % (miss_up, miss_down)

    params = {
        'user_info': user_info,
        'is_same_user': is_same_user,
        'reputation' : user_reputation,
        'conventions': zip(conventions, total_convention_votes),
        'favorites': zip(favorites, total_fav_votes),
        'abilities': abilities,
        'miss_powers': miss_powers
    }
    
    return render(request, 'login/info.html', params)


def age_set(key, val):
    save_time = datetime.utcnow()
    cache.set(key, (val,save_time))


def age_get(key):
    r = cache.get(key)
    
    if r:
        val, save_time = r
        age = (datetime.utcnow() - save_time).total_seconds()
    
    else:
        val, age = None, 0

    return val, age


def get_conventions(update = False):
    mc_key = 'CONVENTIONS'

    convention, age = age_get(mc_key)
    
    if update or convention is None:
        #raise Exception('update: ', update, ' convention: ', convention, ' age: ', age)
        q = Convention.objects.all().order_by("-creation_date")[:30]
        convention = list(q)
        age_set(mc_key, convention)

    return convention, age


def frontpage(request):
    """
    This function returns a list of the latest 100 conventions sorted by creation_date desc
    """
    if request.GET.get('message'):
        next = reverse('frontpage')
        return HttpResponseRedirect(next)

    #conventions, age = get_conventions()
    conventions = Convention.objects.all().order_by("-creation_date")[:MAX_ROWS_TO_DISPLAY ]

    zip_conventions = wrapper_finder(conventions)

    if request.path_info.endswith('json'):
        return jsonize('homepage', zip_conventions)
    
    else:
        return render(request, 'frontpage.html', {'conventions' : zip_conventions })


def post_convention(request):
    """
    Through this function will be add a new CodingCovention
    TODO:
        1. Add minimum required reputation to create a new tag
        2. Delete model TagReletadeNames
    """
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect( '../../login/?next=/post/guideline/')

    if request.method == 'POST':
        form = AddConventionForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data 
            title = cd['identifier_type']
            description = cd['rules_for_naming']
            tag = cd['language_tag']

            valid_title,title_msg = is_valid_title(title)
            if valid_title:
                tag_lan = None
                try:
                    tag_lan = Tag.objects.get(name=tag)
                except Tag.DoesNotExist:
                    
                    try:
                        lan = Language.objects.get(name=tag)
                        tag_lan = Tag.objects.create(name=lan, login=request.user)
                    except Language.DoesNotExist:
                        wrn_lang = True 
                        return render(request, 'conventions/post.html', {'form':form, 'wrn_lang':wrn_lang})

                convention = Convention.objects.create(title=title,
                    description=description,
                    login=request.user, 
                    tag= tag_lan)
                
                Reputation.objects.create(points=PTS_POST,convention=convention,login=request.user)
            
            else:
                return render(request, 'conventions/post.html', {'form':form, 'error_min_char':title_msg})

#            mc_key = 'CONVENTIONS'
#            post, age = age_get(mc_key)
            next = reverse('cv_perma', args=(convention.id,))
            return HttpResponseRedirect(next)

    else: 
       form = AddConventionForm()
    
    return render(request, 'conventions/post.html', {'form':form})


def similar_convention(request, offset):
    """
    Displays a list of similar conventions
    Requeriments to be a "similar convention"
        1. Same Tag (Language)
        2. Same Title
    """
    similar_convention = get_object_or_404(Convention, id=offset)
    conventions = Convention.objects.filter(title=similar_convention.title, tag=similar_convention.tag)

    params = {}
    if conventions.count() <= 1: 
        params['no_similars_msg'] = 'This guideline has no similars.' 

    vote_conventions = {}
    for convention in conventions:
        vote = Vote.objects.total_votes(convention)
        vote_conventions[convention] = vote

    sort_conventions = list(sorted(vote_conventions, key=vote_conventions.__getitem__, reverse=True))
    zip_conventions = wrapper_finder(sort_conventions)

    params['conventions']= zip_conventions 
    

    if request.path_info.endswith('json'):
        return jsonize( ''.join(['Similar: ',conventions[0].title]), zip_conventions) 
    
    else:
        return render(request, 'conventions/similar.html', params)


def users(request):
    """
    This function return a Leaderboards of all active users
    """
    users = []
#    sort = None
    sorting = Sorting(User.objects.filter(is_active=True)) 
    page = 1
    
    if request.method == "GET": 
        sort = request.GET.get('sort')
        page = request.GET.get('page')
        
        if sort == "date":
            users = sorting.user_attr('-date_joined')
        
        elif sort == "title":
            users = sorting.user_attr('username')
        
        elif sort == "reputation":
            users = sorting.user_reputation()
        
        else:
            sort = 'reputation'
            users = sorting.user_reputation()


    paginator = Paginator(users, MAX_COMMUNITY_PROFILES)
    try:
        page_users = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        page_users = paginator.page(1)
    except (EmptyPage, TypeError):
        page_users = paginator.page(paginator.num_pages)

    reputation = []
    userinfo = []
    for user in page_users:
        reputation.append(Reputation.objects.total(login=user))
        try:
            log_info = LoginInfo.objects.get(login=user)
            userinfo.append(log_info)
        except LoginInfo.DoesNotExist:
            pass

    tabs = ['reputation','newest','a - z']
    sort_key = ['reputation','date','title']
    params = {'users': zip(page_users,reputation,userinfo), 'sort':sort, 'tabs':zip(tabs,sort_key), 'pagin':page_users }
    return render(request, 'users.html', params) 


def most_popular(request):
    sorting = Sorting( Convention.objects.all() )
    conventions = sorting.votes(up=True)[:MAX_POPULAR]

    zip_conventions = wrapper_finder(conventions)
    
    if request.path_info.endswith('json'):
        return jsonize('Top', zip_conventions)
    
    else:
        return render(request, 'conventions/hot.html', { 'conventions' : zip_conventions, 'title_site':'Most Polular', 'title': 'Most Popular Guidelines' })


def hot_conventions(request):
    """
    Returns a list of hot conventions base on hot_math(a,b) function
    """
    sorting = Sorting( Convention.objects.all().order_by('-creation_date')[:MAX_ROWS_TO_DISPLAY] )
    conventions = sorting.hot()[:MAX_ROWS_TO_DISPLAY ]

    zip_conventions = wrapper_finder(conventions)
    
    if request.path_info.endswith('json'):
        return jsonize('Hot', zip_conventions)
    
    else:
        return render(request, 'conventions/hot.html', { 'conventions' : zip_conventions, 'title_site':'Hot', 'title': 'Hot Guidelines' })


def unvoted(request):
    sorting = Sorting( Convention.objects.all().order_by('-creation_date')[:MAX_ROWS_TO_DISPLAY] )
    
    conventions = sorting.unvoted('creation_date',newest=True)
    #conventions = Convention.objects.all().order_by('-creation_date')[:5]

    zip_conventions = wrapper_finder(conventions)

    if request.path_info.endswith('json'):
        return jsonize('Unvoted', zip_conventions)
    
    else:
        return render(request, 'conventions/unvoted.html', {'conventions': zip_conventions})


def favorites(request):
    """
     this views shows the favorites of every user
    """
    
    if not request.user.is_authenticated():
        raise Http404   

    convention_list = Favorite.objects.filter(login=request.user)
    
    paginator = Paginator(convention_list, MAX_ROWS_TO_DISPLAY)
    page = 1
    if request.method == "GET" and request.GET.get('page'):
        page = request.GET.get('page')

    try:
        conventions = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        conventions = paginator.page(1)
    except (EmptyPage, TypeError):
        conventions = paginator.page(paginator.num_pages)

    all_conventions = []
    reputations = []
    votes = []
    
    for convention in conventions:
        convention = get_convention_if_edited(convention)
        all_conventions.append(convention)
        reputations.append( Reputation.objects.total(convention.convention.login) )
        t_votes = Vote.objects.total_votes(convention.convention)
        res_votes = "+%d" % t_votes if t_votes > 0 else t_votes
        votes.append( res_votes )
    
    zip_conventions = zip(all_conventions,reputations,votes)

    return render(request, 'conventions/user_favorite_list.html', {'conventions': zip_conventions, 'pagin':conventions })


def front_conventions_tagged(request, offset=0, slug=" "):
    """
    Show all conventions for individual Tag (Language). 
    This function also looks at similar* conventions and it displays (compare)
    the hottest of them.
    The conventions to display are sorted by hottets.
    
    *Requeriments to be a "similar convention"
        1. Same Tag (Language)
        2. Same Title
    """
    #tag = get_object_or_404(Tag, id=offset)

    try:
        tag = Tag.objects.get(id=offset)
        
        if slug != tag.slug:
            next = reverse("cv_tagged", args=(tag.id, tag.slug,))
            return HttpResponseRedirect(next)

    except Tag.DoesNotExist:
        try:
            tag = Tag.objects.get(slug=slug)
            if offset != tag.id:
                next = reverse("cv_tagged", args=(tag.id, tag.slug,))
                return HttpResponseRedirect(next)

        except Tag.DoesNotExist:
            raise Http404


    conventions = []
    sorting = Sorting( Convention.objects.filter(tag=tag) )
    page = 1
    sort = "up_votes"
    
    if request.method == "GET": 
        sort = request.GET.get('sort')
        page = request.GET.get('page')
        
        if sort == "date":
            conventions = sorting.attr("creation_date", True) 
        
        elif sort == "title":
            conventions = sorting.attr("title", False) 
        
        elif sort == "hot":
            conventions = sorting.hot()
        
        elif sort == "up_votes":
            conventions = sorting.votes(up=True)
        
        elif sort == "down_votes":
            conventions = sorting.votes(up=False)
        
        elif request.user.is_authenticated() and sort == "favorites":
            conventions = sorting.favorites(request.user,offset)
       
        else:
            sort = 'up_votes'
            conventions = sorting.votes(up=True)
        #    raise Http404
    
    #else:
    
    paginator = Paginator(conventions, MAX_ROWS_TO_PAGE)
    try:
        reduce_conventions = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        reduce_conventions = paginator.page(1)
    except (EmptyPage, TypeError):
        reduce_conventions = paginator.page(paginator.num_pages)
    
#    raise Exception(reduce_conventions.paginator.num_pages)       
    zip_conventions = wrapper_finder(reduce_conventions,find_edited_versions=False)
    
    if request.path_info.endswith('json'):
        return jsonize(conventions[0].tag.name, zip_conventions)

    else:
        tabs =     ['up votes','down votes']
        sort_key = ['up_votes','down_votes']

        if request.user.is_authenticated():
            tabs.append('favorites')
            sort_key.append('favorites')

        tabs.extend(['hot','a - z','newest'])
        sort_key.extend(['hot','title','date'])

        params = {'conventions':zip_conventions, 'pagin':reduce_conventions, 'language':tag.name,'offset':offset,'sort':sort, 'tabs': zip(tabs,sort_key)}
        return render(request, 'conventions/tagged.html', params)


""" LOG IN, SIGN UP """
def logout_view(request):
    """
    Logout users function
    """
    next = reverse('frontpage')
    if request.user.is_authenticated():
        logout(request)

    response = HttpResponseRedirect(next)
    return response

def login_view(request):
    """
    Login user function
    """
    if request.user.is_authenticated():
        next = reverse("frontpage")
        return HttpResponseRedirect(next)

    redirect_to = request.REQUEST.get('next', '')
    if not redirect_to or redirect_to == '/login/' or redirect_to == '/signup/' or redirect_to == '/join/':
        redirect_to = '/'
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        params = {}
        
        if user is not None:
            
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_to)

            else:
                # Return a 'disabled account' error message
                params['error_username'] = "This user doesn't exist anymore."
                params['username'] = username
                return render(request, 'login/login.html', params)

        else:
            # Return an 'invalid login' error message.
            params['error_message'] = "Username or password incorrect."
            params['username'] = username
            return render(request, 'login/login.html', params)

    return render(request,'login/login.html')


def signup(request): 
    
    if request.user.is_authenticated():
        next = reverse("frontpage")
        return HttpResponseRedirect(next)

    params = {}
    if request.method == 'POST':
        form =  SignupForm(request.POST)
        params['form'] = form
        
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            email = cd['email']
            password = cd['password']
            password_verify = cd['password_verify']
            
            have_error = False
            
            if email:
                
                if not valid_email(email):
                    have_error = True

            if not valid_username(username):
                have_error = True
                params['error_username'] = "Invalid username, use at least 4 and not more than 12 characters."

            if not valid_password(password):
                have_error = True
                params['error_password'] = "Invalid password, use at least 5 characters."

            if password != password_verify:
                have_error = True
                params['error_password_verify'] = "Your password doesn't match."

            user_found = User.objects.filter(username=username)
            
            if user_found:
                have_error = True
                params['error_username'] = 'Username already taken.'

            if have_error:
                params['have_error'] = True
                return render(request, 'login/signup.html', params, context_instance=RequestContext(request) )

            user = User.objects.create_user(username=username,email=email,password=password)
            user.is_staff=False
            user.save()

            if user:
                LoginInfo.objects.create(login=user,website='',location='')

                Reputation.objects.create(login=user, points=PTS_WELCOME)
                
                user = authenticate(username=username, password=password)
                login(request, user)

                notification = Notification.objects.create(
                    supporter=user,
                    extra_info = "Thanks for joining us...")
                notification.login.add(user)
                
                
                #next = reverse('frontpage', kwargs={ 'show_welcome_banner':True })
                request.session['show_welcome_banner'] = True
                next = reverse('frontpage')
                return HttpResponseRedirect(next)
        
        else:
            params['have_error'] = True
            
            return render(request, 'login/signup.html', params,context_instance=RequestContext(request) )
    
    else:
        form = SignupForm()
    
    return render(request,'login/signup.html', {'form':form}, context_instance=RequestContext(request))
           

""" TOGGLE FUNCTIONS """
def toggle_delete_comment(request):
    """
    Just the writter of the comment has the rights to delete their 
    own comment
    """
    
    if request.method == "POST":
        comment_id = request.POST["comment_id"]
        comment_request = get_object_or_404(Comment, id=comment_id)
        
        if not request.user.is_authenticated():
            url_red_path = ''.join(['../login/?next=/guideline/',str(comment_request.convention.id),'/'])
            return HttpResponseRedirect( url_red_path )
        
        Notification.objects.filter(is_comment=True,convention=comment_request.convention,creation_date=comment_request.creation_date,supporter=comment_request.login).delete()
        comment_request.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def toggle_update_comment(request):
    if request.method == "POST":
        comment_id = request.POST["comment_id"]
        comment_text = request.POST["comment_text"]
        comment_request = get_object_or_404(Comment, id=comment_id)

        if not request.user.is_authenticated():
            url_red_path = ''.join(['../login/?next=/guideline/',str(comment_request.convention.id),'/'])
            return HttpResponseRedirect( url_red_path )
        
        if comment_request.comment != comment_text:
            comment_request.comment=comment_text
            comment_request.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def toggle_comment(request):
    """
    Add comments to perma conventions (just for logged users)
    """
    if request.method == "POST":
        convention_id = request.POST['convention_id']
        comment = request.POST.get('comment')
        convention = get_object_or_404(Convention, id=convention_id)

        if not request.user.is_authenticated():
            url_red_path = ''.join(['../login/?next=/guideline/',convention_id,'/'])
            return HttpResponseRedirect( url_red_path ) 
        
        if comment:
            Comment.objects.create(login=request.user,convention=convention,comment=comment) 

            notification = Notification.objects.create(is_comment=True,supporter=request.user,convention=convention,extra_info=comment[:200])
            replies = Comment.objects.filter(convention=convention)
            to_reply = {}
            for replay in replies:
                if replay.login != request.user:
                    to_reply[replay.login] = replay.login

            if convention.login != request.user: 
                to_reply[convention.login]=convention.login

            if not to_reply:
                notification.delete()
            else:
                notification.login.add(*to_reply) # * means iterate through a list
        else:
            next = reverse('cv_perma', args=(convention_id,))
            return HttpResponseRedirect(next)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def flag(request):
    
    if request.method == "POST":
        flag_convention_id = request.POST['convention_id']
        is_convention = request.POST['is_convention']
        is_duplicate = request.POST['is_duplicate']
        duplicate_convention_id = request.POST['duplicate_convention_id']
        
        convention = get_object_or_404(Convention, id=flag_convention_id)
        
        if not request.user.is_authenticated():
            url_red_path = ''.join(['../../login/?next=/guideline/',flag_convention_id,'/'])
            return HttpResponseRedirect( url_red_path ) 

        is_convention = True if is_convention == "true" else False
        is_duplicate = True if is_duplicate == "true" else False

        convention_duplicated = None if duplicate_convention_id == "None" else duplicate_convention_id
        if convention_duplicated:
            convention_duplicated = get_object_or_404(Convention, id=duplicate_convention_id)
        
        try:
            sel_flag = Flag.objects.get(login=request.user,convention=convention,flag=True, is_convention=is_convention, is_duplicate=is_duplicate, convention_duplicate=convention_duplicated)
            sel_flag.delete()
        except Flag.DoesNotExist:
            Flag.objects.create(login=request.user,convention=convention,flag=True, is_convention=is_convention, is_duplicate=is_duplicate, convention_duplicate=convention_duplicated)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def toggle_rm_welcome(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            request.session['show_welcome_banner'] = False 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def toggle_favorite(request):
    """
    Tag a convention as a Favorite
    """
    
    if not request.user.is_authenticated():
        if request.is_ajax():
            data = json.dumps({'redirect':'login'})
            return HttpResponse(data, content_type='application/json; charset=utf8')
        else:
            next = reverse('frontpage')
            return HttpResponseRedirect(next)
    
    login = request.user
    
    if request.method == "POST":
        convention_id = request.POST['convention_id']
        favorite = request.POST['favorite']
        convention = get_object_or_404(Convention, id=convention_id)
        #favorite = True if favorite == 'true' else False

        if favorite:
            all_favs = Favorite.objects.all().filter(convention=convention,login=login)
            if all_favs.count() < 2:
                favorite, created = Favorite.objects.get_or_create(convention=convention,login=login,favorite=True)
                if not created:
                    favorite.delete()
                data = json.dumps({"redirect":False})
                return HttpResponse(data, content_type='application/json; charset=utf8');

            else:
                all_favs.delete()
                data = json.dumps({"redirect":False})
                return HttpResponse(data, content_type='application/json; charset=utf8');
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def toggle_comment_vote(request):
    
    if not request.user.is_authenticated():
        if request.is_ajax():
            data = json.dumps({"redirect":"login"})
            return HttpResponse( data, content_type='application/json; charset=utf8')
        else:
            next = reverse('frontpage')
            return HttpResponseRedirect(next)

    login = request.user

    if request.method == "POST":
        comment_id = request.POST['comment_id']

        comment = get_object_or_404(Comment, id=comment_id)
        if comment.login == request.user:
            if request.is_ajax():
                return HttpResponse( json.dumps({"invalid_user":True}),
                    content_type='application/json; charset=utf8')

        try:
            VoteComment.objects.get(comment=comment,login=login,up=True,down=False,latest=True).delete()           
        except VoteComment.DoesNotExist:
            VoteComment.objects.create(comment=comment,login=login,up=True,down=False)

        if request.is_ajax():
            data = json.dumps({"text":"%s" % comment})
            return HttpResponse(data, content_type='application/json; charset=utf8');

    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def toggle_vote(request):
    """
    Implent the vote system in conventions using AJAX
    """

    if not request.user.is_authenticated():
        
        if request.is_ajax():
            data = json.dumps({"redirect":"login"})
            return HttpResponse( data, content_type='application/json; charset=utf8')
        else:
            next = reverse('frontpage')
            return HttpResponseRedirect(next)   

    login = request.user

    if request.method == "POST":
        convention_id = request.POST['convention_id']
        up_vote = request.POST['up_vote']
        down_vote = request.POST['down_vote']

        convention = get_object_or_404(Convention, id=convention_id)
        
        if convention.login == request.user:
            if request.is_ajax():
                return HttpResponse( json.dumps({"invalid_user":True}), 
                    content_type='application/json; charset=utf8')
            else:
                next = reverse('frontpage')
                return HttpResponseRedirect(next)   

        down_vote = True if down_vote == "true" else False
        up_vote = True if up_vote == "true" else False

        points = PTS_CONVENTION_POS if up_vote == True else PTS_CONVENTION_NEG
        
        if up_vote:
            if Reputation.objects.total(request.user) < MIN_PTS_TO_VOTE_POS:
                next = reverse('cv_perma', args=(convention.id,))
                return HttpResponseRedirect(next)
        if down_vote:
            if Reputation.objects.total(request.user) < MIN_PTS_TO_VOTE_NEG:
                next = reverse('cv_perma', args=(convention.id,))
                return HttpResponseRedirect(next)

        notification = None

        Notification.objects.all().filter(supporter=login,convention=convention,is_vote_up=True).delete()
        Notification.objects.all().filter(supporter=login,convention=convention,is_vote_down=True).delete()
        Notification.objects.all().filter(supporter=login,convention=convention,is_remove_up=True).delete()
        Notification.objects.all().filter(supporter=login,convention=convention,is_remove_down=True).delete()

        try:
            Vote.objects.get(convention=convention,login=login,up=up_vote,down=down_vote,latest=True).delete()
            
            


            notification = Notification.objects.create(is_remove_up=up_vote,is_remove_down=down_vote,supporter=login,convention=convention,extra_info=convention.description[:200])
            notification.login.add(convention.login)

            delete_reputation(convention,login,points)
            delete_zero_reputation(convention,login,0)
        except Vote.DoesNotExist:
            mirror_points = PTS_CONVENTION_NEG if up_vote == True else PTS_CONVENTION_POS

            notification = Notification.objects.create(is_vote_up=up_vote,is_vote_down=down_vote,supporter=login,convention=convention,extra_info=convention.description[:200])
            notification.login.add(convention.login)
                

            re = delete_reputation(convention,login,mirror_points)
            re_zero = delete_zero_reputation(convention,login,0)

            
            if re or re_zero: # if any reputation is deleted
                Vote.objects.get(convention=convention,login=login,up=(not up_vote),down=(not down_vote),latest=True).delete()
            
            Vote.objects.create(convention=convention,login=login,up=up_vote,down=down_vote)

            if Reputation.objects.total(convention.login) <= 1 and points <= 0:
                points = 0
            
            Reputation.objects.create(points=points,supporter=login,convention=convention,login=convention.login)


        
        data = json.dumps({"redirect":False})
        
        return HttpResponse(data, content_type='application/json; charset=utf8');
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


class ReputationReq(object):
    
    def __init__(self, usr):
        self.usr = usr

    @property
    def total_pts(self):
        return Reputation.objects.total(self.usr)

    def abilities():
        return {
            'edit':MIN_PTS_TO_EDIT,
            'vote_pos':MIN_PTS_TO_VOTE_POS,
            'vote_neg':MIN_PTS_TO_VOTE_NEG,
            'comment':MIN_PTS_TO_COMMENT,
            'post':MIN_PTS_TO_POST,
            'add_lang':MIN_PTS_TO_ADD_NEW_LANG,
            'flag':MIN_PTS_TO_FLAG
            }

    def check(self,ability):
        pts = self.total_pts
        sum = self.abilities - pts
        if sum < 0:
            return True, sum
        return False, sum


""" INTERNAL HELPFULL FUNCTIONS/CLASSES """
class Sorting(object):
     
    def __init__(self, collections):
        self.collections = collections


    @property
    def hide_similar(self):
        c_votes={}
        
        for convention in self.collections:
            c_votes[convention] = Vote.objects.total_votes(convention)

        by_votes = list(sorted(c_votes, key=c_votes.__getitem__, reverse=False)) # False display the best voted

        reduce_duplicates = {}
        
        for convention in by_votes:
            convention = get_convention_if_edited(convention)
            reduce_duplicates[convention.title] = [convention,c_votes[convention]]

        return reduce_duplicates.values()


    def votes(self,up):
        by_votes = {}
        
        for c in self.hide_similar:
            by_votes[c[0]] = c[1]
        
        return list(sorted(by_votes, key=by_votes.__getitem__, reverse=up))


    def attr(self, attr,reverse=False):
        sorting = {}
        
        for c in self.hide_similar:
            sorting[c[0]]=getattr(c[0], attr)
        
        return list(sorted(sorting,key=sorting.__getitem__,reverse=reverse))


    def favorites(self,user,offset):
        sorting = []
        all_favs = Favorite.objects.filter(login=user, convention__tag=offset)
        
        if all_favs.count > 0:
            
            for c in all_favs:
                sorting.append( Convention.objects.get(id=c.convention.id) )
            
            return sorting
        
        else:
            
            return []


    def hot(self, reverse=True):
        hots = {}
        
        for c in self.hide_similar:
            hots[c[0]] = hot_math(c[1],c[0])
        
        return list(sorted(hots, key=hots.__getitem__, reverse=reverse))


    def unvoted(self,attr,newest=True):
        unvo={}
        
        for c in self.hide_similar:
            
            if c[1] == 0:
                unvo[c[0]] = getattr(c[0], attr)
        
        return list(sorted(unvo, key=unvo.__getitem__, reverse=newest))

    
    def user_attr(self,attr,reverse=True):
        
        return self.collections.order_by(attr)

    
    def user_reputation(self,best=True):
        rep={}
        
        for user in self.collections:
            rep[user] = Reputation.objects.total(login=user)
        
        return list(sorted(rep,key=rep.__getitem__,reverse=best))


def user_pressed_edit(request, user_info):
    user_info.birthday = request.POST.get("birthday")
    user_info.location = request.POST.get("location")
    website = request.POST.get("website")
    
    if website:
        http = 'http'
        https = 'https'
        if ( website.find(http) == -1 or website.find(http) != 0 ) and ( website.find(https) == -1 or website.find(https) != 0 ):
            user_info.website = ''.join(['http://',website])
        else:
            user_info.website = website
    else:
        user_info.website = ''

    if user_info.birthday:
        try:
            datetime.strptime(user_info.birthday, '%Y-%m-%d')
            user_info.save()
        except ValueError:
            error_birthday = 'Ex. yyyy-mm-dd'
            return render(request, 'login/edit.html', {'login_info':user_info, 'error_birthday':error_birthday})

    else:
        user_info.birthday = None
        user_info.save()
    
    next = reverse('lg_info', args=(request.user.id,))
    return HttpResponseRedirect(next)   


def user_pressed_delete(request):
    request.user.is_active = False
    request.user.save()
    
    return HttpResponseRedirect(reverse('lg_logout'))


def user_pressed_edit_mail(request, user_info):
    email =  request.POST.get("email")
    if email:
        if valid_email(email):
            request.user.email = email
            request.user.save()
            next = reverse('lg_info', args=(request.user.id,))
            return HttpResponseRedirect(next)   
        
        else:
            error_mail = 'Insert a valid email.'
            return render(request, 'login/edit.html', {'login_info':user_info, 'error_mail':error_mail})
    else:
        request.user.email = ''
        request.user.save()
        next = reverse('lg_info', args=(request.user.id,))
        return HttpResponseRedirect(next)   



def user_pressed_edit_log(request,user_info):
    current_pw = request.POST.get('current_pw')
    password = request.POST.get('new_pw')
    verify = request.POST.get('confirm_pw')
    
    have_error = True
    error_pw = ''
    error_current_pw = ''
    if current_pw and password and verify:
        user = authenticate(username=request.user.username, password=current_pw)
        
        if user and (password == verify):
            if not valid_password(password):
                have_error = True
                error_pw = "Password must at least 5 chars long."
            else:
                have_error = False
                request.user.set_password(verify)
                request.user.save()
        
        elif password and password != verify:
            have_error = True
            error_pw = "Password doesn't match."
        
        elif not user:
            have_error = True
            error_current_pw = 'Invalid password.'
        
        else:
            have_error = True
            error_pw = "This user is not authenticated."
            
    else:
        have_error = True
        error_current_pw = 'All password inputs are required.'

    if have_error:
        return render(request, 'login/edit.html', {'login_info':user_info,'error_current_pw':error_current_pw,'error_pw':error_pw})
    
    else:
        next = reverse('lg_info', args=(request.user.id,))
        return HttpResponseRedirect(next)


""" EXTRA FUNCTIONS """

PASS_RE = re.compile(r"^.{5,100}$")
def valid_password(password):
    return password and PASS_RE.match(password)


USR_RE = re.compile(r"^.{4,12}$")
def valid_username(username):
    return username and USR_RE.match(username)


EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return email and EMAIL_RE.match(email)


def make_salt():
    return ''.join(random.choice(string.letters) for x in range(5))


def make_password_hash(username, password, salt=None):
    
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(username + password + salt ).hexdigest()
    
    return '%s,%s' % (salt, h)


def find_dynamicurl(request):
    next = request.POST.get('next', '')
    
    if not next:
        next = reverse('frontpage')
    
    return HttpResponseRedirect(next)


def get_convention_if_edited(convention):
    is_edited = Edit.objects.is_edited(convention)
    
    if is_edited:
        edited = Edit.objects.get(latest=True, convention=convention)
        convention.description = edited.description
        convention.title = edited.title
    
    return convention


def delete_zero_reputation(convention, login, points):
    try:
        rep = Reputation.objects.get(convention=convention, 
            supporter=login, login=convention.login, points=points)
        rep.delete()
        return True
    except Reputation.DoesNotExist:
        return False


def delete_reputation(convention, login, points):
    try:
        rep = Reputation.objects.get(convention=convention, 
            supporter=login, login=convention.login, points=points)
        rep.delete()
        return True
    except Reputation.DoesNotExist:
        return False



def hot_math(votes, convention):
    ######## Find hottest math ########
    # hot = votes + 1 / time + 1.5
    ##################################
    now = datetime.utcnow().replace(tzinfo=utc)
    timediff = now - convention.creation_date
    sec = timediff.seconds

    # H = (Vo + 1) * (Vi + 1) / T
    return (votes + 1) / (sec + 1.5)


def is_valid_title(title):
    
    if len(title.split() ) > 0 and len(title) > 4:
        return True, None
    
    error_min_char = "This title is too short."
    
    return False, error_min_char


def wrapper_finder(conventions,find_edited_versions=True):
    all_conventions = []
    reputations = []
    votes = []
    
    for convention in conventions:
        
        if find_edited_versions:
            convention = get_convention_if_edited(convention)
        all_conventions.append(convention)
        reputations.append( Reputation.objects.total(convention.login) )
        t_votes = Vote.objects.total_votes(convention)
        res_votes = "+%d" % t_votes if t_votes > 0 else t_votes
        votes.append( res_votes )
    
    return zip(all_conventions,reputations,votes)


def jsonize(site_title, conventions_pack):
    # TODO handle inactive users
    json_render = json.dumps({'results':[{'site':site_title, 
                                    'guidelines': [{'id':std.id,
                                                    'title':std.title,
                                                    'votes':vote,
                                                    'language':std.tag.name,
                                                    'description':markdown2.markdown(std.description),
                                                    'posted':str(std.creation_date),
                                                    'user':[{'username':std.login.username if std.login.is_active else 'community',
                                                             'reputation':rep}]} 
                                    for std,rep,vote in conventions_pack] }] }, indent=4 )
    
    return HttpResponse(json_render, content_type='application/json; charset=UTF-8')



