from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(FacebookStatus)
admin.site.register(TwitterStatus)
admin.site.register(ImagesList)

