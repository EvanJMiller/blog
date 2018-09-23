from django.contrib import admin

# Register your models here.
from .models import Article, Profile
#from django.contrib.auth.models import User

admin.site.register(Article)
admin.site.register(Profile)





