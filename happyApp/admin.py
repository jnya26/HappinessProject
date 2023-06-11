from django.contrib import admin
from django.db import models

from .models import TeamsModel, UserModel


class TeamsModelAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'logo']
    exclude = ['team_mood_rate']


class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'team']
    exclude = ['avarage_mood_mark', 'token']
    formfield_overrides = {
        models.ForeignKey: {'required': False},
    }


admin.site.register(TeamsModel, TeamsModelAdmin)
admin.site.register(UserModel, UserModelAdmin)

# Register your models here.
