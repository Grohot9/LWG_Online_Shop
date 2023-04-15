from django.contrib import admin
from django.contrib.auth import get_user_model

from account.models import Role, UserProfile

admin.site.register([get_user_model(), UserProfile, Role])
