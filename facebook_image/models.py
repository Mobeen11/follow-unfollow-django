from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('approved', 'Approved'),
    )
    status = models.CharField(max_length=255,
                              choices=STATUS, default=STATUS[0][0])
    author = models.OneToOneField(User, null=True, blank=True, related_name="user_profile")
    # author = models.ForeignKey(User, null=True, blank=True, related_name="user_profile")
    username = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    profile_image = models.ImageField()
    new_profile_image = models.ImageField(blank=True, upload_to='profile_images')

    def __str__(self):
        return self.name


# class FacebookStatus(models.Model):
#
#     publish_timestamp = models.DateTimeField(null=True, blank=True)
#     # author = models.ForeignKey(User)
#     author = models.ForeignKey(User, null=True, blank=True, related_name="user_profile_facebook")
#     message = models.TextField(max_length=255)
#     link = models.URLField(null=True, blank=True)
#     profile_image = models.ImageField(blank=True, upload_to='facebookstatus_images/profile_images')
#     new_image = models.ImageField(blank=True, upload_to='facebookstatus_images/new_profiles')
#
#     def __str__(self):
#         return self.message

class FacebookStatus(models.Model):
    username = models.CharField(max_length=255, blank=True)
    fullname = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey(User, null=True, blank=True, related_name="user_profile_facebook")
    link = models.URLField(null=True, blank=True)
    publish_timestamp = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(blank=True, upload_to='facebookstatus_images/profile_images')
    new_image = models.ImageField(blank=True, upload_to='facebookstatus_images/new_profiles')
    message = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.fullname

class TwitterStatus(models.Model):
    username = models.CharField(max_length=255, blank=True)
    fullname = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey(User, null=True, blank=True, related_name="user_profile_twitter")
    link = models.URLField(null=True, blank=True)
    publish_timestamp = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(blank=True, upload_to='twitterstatus_images/profile_images')
    new_image = models.ImageField(blank=True, upload_to='twitterstatus_images/new_profiles')
    message = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.fullname

class ImagesList(models.Model):
    image = models.ImageField(blank=True,  upload_to='imageslist')

    def __str__(self):
        return str(self.image)


class Group(models.Model):
    alias = models.CharField(max_length=255, unique=True,  blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    followers_count = models.IntegerField(null=True, blank=True)
    total_donations_count = models.IntegerField(null=True, blank=True)
    donations = models.IntegerField(null=True, blank=True)
    @property
    def total_score(self):
        score = self.followers_count *1 + (self.total_donations_count*10 + self.donations*10)
        return score