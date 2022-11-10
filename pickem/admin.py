from django.contrib import admin

# Register your models here.

from .models import Player, Knockout, Team, Question, Choice, UserGroup, UserKnockout

admin.site.register(Player)
admin.site.register(Knockout)
admin.site.register(Team)
admin.site.register(UserKnockout)
admin.site.register(UserGroup)
admin.site.register(Question)
admin.site.register(Choice)
