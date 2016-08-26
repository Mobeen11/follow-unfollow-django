

# def get_profile_image(strategy, details, response, uid, user, social, *args, **kwargs):
#     """Attempt to get a profile image for the User"""
#
#     if user is None:
#         return
#
#     image_url = None
#     if strategy.backend.name == "facebook":
#         image_url = "https://graph.facebook.com/{0}/picture?type=large".format(uid)
#     elif strategy.backend.name == "twitter":
#         if response['profile_image_url'] != '':
#             image_url = response['profile_image_url']
#
#     if image_url:
#         try:
#             result = urllib.urlretrieve(image_url)
#             user.original_photo.save("{0}.jpg".format(uid), File(open(result[0])))
#             user.save(update_fields=['original_photo'])
#         except URLError:
#             pass


#
# def save_profile(backend, user, response, *args, **kwargs):
#     if backend.name == 'facebook':
#         profile = user.get_profile()
#         print "profile: ", profile
#         if profile is None:
#             profile = Profile(user_id=user.id)
#             print "IF profile: ", profile
#         profile.gender = response.get('gender')
#         profile.link = response.get('link')
#         profile.timezone = response.get('timezone')
#         profile.save()
#

from .models import *
from django.shortcuts import render, redirect, render_to_response
def save_profile(backend, user, response, *args, **kwargs):
    print "this is pipeline"
    print "user: ", user
    print "response: ", response
    print "args: ", args
    print "kargs: ", kwargs
    profile = Profile()


    if backend.name == 'twitter':
        profile1 = Profile.objects.filter(username=user)
        if profile1:
            print "user already exist"
        else:
            image_url = response['profile_image_url_https']
            profile.profile_image = image_url
            profile.username = user
            print "image_url: ", image_url
            profile.save()
    if backend.name == 'facebook':
        profile1 = Profile.objects.filter(username=user)
        if profile1:
            print "user already exist"
        else:
            print "this is facebook"
            user_profile = User.objects.filter(username=user)
            print "user_profile: ", user_profile



            profile.author = user_profile
            print " profile.author",  profile.author
            url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
            profile.profile_image = url
            profile.username = user
            fb_username = kwargs['details']['username']
            profile.name = fb_username

            print "image_url: ", url
            print "username: ", fb_username
            profile.save()
            context = {
                'image': profile.profile_image,
                'user_name': fb_username,
            }
    # return render('practice.html', context )