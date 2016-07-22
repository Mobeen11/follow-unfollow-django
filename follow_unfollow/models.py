from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce import models as tinymce_models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    followers = models.CharField(max_length=120, null=True, blank=True)
    #picture = models.ImageField(upload_to="/pics", null=True, blank=True)   #this will give error of media etc etc

    def __str__(self):
        return self.user.username

status = (
    ('single', 'single'),
    ('mutual', 'mutual'),
)


class RelationShip(models.Model):
    follow = models.ForeignKey(User, related_name='follow')
    following = models.ForeignKey(User, related_name='following')
    my_status = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return str(self.follow)


class Post(models.Model):
    author = models.ForeignKey('auth.User', related_name='post_author')
    text = tinymce_models.HTMLField()
    created_date =  models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
