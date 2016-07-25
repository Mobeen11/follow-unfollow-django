from django.contrib import admin
from .models import UserProfile
from .models import RelationShip
from .models import Post


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["author", "published_date", "text"]

class RelationshipAdmin(admin.ModelAdmin):
    list_display = ["following", "follow", "my_status"]

admin.site.register(UserProfile)
admin.site.register(RelationShip, RelationshipAdmin)
admin.site.register(Post, PostAdmin)
