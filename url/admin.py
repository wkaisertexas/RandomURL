from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager

from .models import *

admin.site.register(User)
admin.site.register(Destination)
admin.site.register(URL)
