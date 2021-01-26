from django.contrib import admin
from conventions.models import Convention, Vote, Favorite, Edit, Comment, Flag, Duplicate, VoteComment

admin.site.register(Convention)
admin.site.register(Edit)
admin.site.register(Vote)
admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(Flag)
admin.site.register(Duplicate)
admin.site.register(VoteComment)
