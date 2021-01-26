from django import template
from conventions.models import Vote, Favorite, Convention, Edit, Comment
from reputations.models import Reputation

register = template.Library()

def base_standards(convention, reputation, votes, show_discussion_count=True, similars=True, display_date=True):
    return {'convention':convention,
            'reputation':reputation,
            'votes':votes, 
            'display_date': display_date,
            'show_discussion_count':show_discussion_count, 
            'similars':similars}


def convention_list(convention):
    is_edited = Edit.objects.is_edited(convention)
    edit = None
    edit_reputation = None
    if is_edited:
        edit = Edit.objects.get(latest=True, convention=convention)
        edit_reputation = Reputation.objects.total(edit.login)
        is_edited = True
    reputation = Reputation.objects.total(convention.login)
    return {
            'convention': convention, 
            'reputation': reputation,
            'edit': edit,
            'is_edited' : is_edited,
            'edit_reputation': edit_reputation
        }

def edited_convention(convention):
    
    is_edited = Edit.objects.is_edited(convention)
    edit = None
    editor_reputation = None
    if is_edited:
        edit = Edit.objects.get(latest=True, convention=convention)
        editor_reputation = Reputation.objects.total(edit.login)
        is_edited = True
    reputation = Reputation.objects.total(convention.login)
    return {
            'convention': convention, 
            'reputation': reputation,
            'edit': edit,
            'is_edited' : is_edited,
            'editor_reputation': editor_reputation
        }


def same_conventions(convention):
    same_conventions = Convention.objects.filter(title=convention.title, tag=convention.tag)
    convention = same_conventions
    return{ 'same_conventions': same_conventions, 'convention':convention, 'total': same_conventions.count()-1 }


def discussion_count(convention):
    total = Comment.objects.filter(convention=convention)
    return{ 'total':total.count() }


def delete_comment(context, comment):

    return { 'comment':comment }

def vote_comment(context, comment):
    
    return { 'comment':comment } 

def comment_list(context, convention):
    
    return { 'convention':convention }

def vote_list(context, convention, total_votes):
    
    vote = None
    if context['request'].user.is_authenticated():
        vote = Vote.objects.filter(convention=convention, login=context['request'].user, latest=True)
    if vote:
        vote = vote[0]
    
    active_user_reputation = None
    if context['request'].user.is_authenticated():
        active_user_reputation = Reputation.objects.total(context['request'].user)
    
    return { 'total_votes':total_votes, 'vote':vote, 'convention':convention, 'reputation':active_user_reputation }


def favorite_list(context, convention):
    
    favorite = None
    if context['request'].user.is_authenticated():
        try:
            login = context['request'].user
            favorite = Favorite.objects.is_favorite(convention, login)
        except IndexError:
            favorite = None

    return { 'favorite': favorite, 'convention': convention }
   
register.inclusion_tag("conventions/base_standards.html")(base_standards)
register.inclusion_tag("conventions/convention_info.html")(convention_list)
register.inclusion_tag("conventions/votes.html", takes_context=True)(vote_list)
register.inclusion_tag("conventions/favorite.html", takes_context=True)(favorite_list)
register.inclusion_tag("conventions/comment.html", takes_context=True)(comment_list)
register.inclusion_tag("conventions/same_conventions.html")(same_conventions)
register.inclusion_tag("conventions/discussion_count.html")(discussion_count)
register.inclusion_tag("conventions/edited_convention.html")(edited_convention)
register.inclusion_tag("conventions/vote_comment.html", takes_context=True)(vote_comment)
register.inclusion_tag("conventions/delete_comment.html", takes_context=True)(delete_comment)
