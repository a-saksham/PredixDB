from django.contrib import admin
from .models import Movies, Notifications, Cast
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Movies)
admin.site.register(Notifications)
admin.site.register(Cast)