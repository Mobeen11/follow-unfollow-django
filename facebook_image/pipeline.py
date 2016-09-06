

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

from .models import *
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
from django.shortcuts import render, redirect, render_to_response
from requests import request, HTTPError
from urllib2 import urlopen, HTTPError
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from PIL import Image
from twython import Twython
twitter = Twython()
def save_profile(backend, user, response, *args, **kwargs):
    print "this is pipeline"
    print "user: ", user
    print "response: ", response
    print "args: ", args
    print "kargs: ", kwargs
    profile = Profile()
    twitter_obj = TwitterStatus()
    facebook_obj = FacebookStatus()


    if backend.name == 'twitter':
        twitter_profile = TwitterStatus.objects.filter(username=user)
        if twitter_profile:
            print "user already exist"
            # print "profile:", twitter.getProfileImage(user, size='bigger')
        else:
            # user = User.objects.get(username = response['access_token']['screen_name'])
            # user.set_password(response['oauth_token']['oauth_token_secret'])
            # user.save()

            image_url = response['profile_image_url_https']
            avatar = urlopen(image_url)

            twitter_obj.profile_image.save(slugify(user.username) + '.png',
                        ContentFile(avatar.read()))
            twitter_obj.link = image_url
            twitter_obj.username = user.username
            twitter_obj.fullname = kwargs['details']['fullname']
            print "image_url: ", image_url
            print "fullname: ", kwargs['details']['fullname']
            twitter_obj.save()
            print "that is twitter user"

    if backend.name == 'facebook':
        facebook_profile = FacebookStatus.objects.filter(username=user)
        if facebook_profile:
            print "user already exist"
        else:
            print "this is facebook"
            url = 'http://graph.facebook.com/{0}/picture?type='.format(response['id'])
            print "link_pipeline: ", url
            try:
                response = request('GET', url, params={'type': 'large'})
                response.raise_for_status()
                print "this is largeImage"
            except HTTPError:
                pass
            else:
                facebook_obj.link = url
                avatar = urlopen(url)
                # facebook_obj.profile_image.save(slugify(user.username) + '.png',
                #             ContentFile(avatar.read()))
                facebook_obj.profile_image.save('{0}_social.jpg'.format(user.username),
                                           ContentFile(response.content))
                print "fb_profile_image_url: ", facebook_obj.profile_image.url
                facebook_obj.username = user.username
                fb_username = kwargs['details']['username']
                facebook_obj.fullname = fb_username

                print "image_url: ", url
                print "username: ", fb_username
                facebook_obj.save()
                print "that is facebook user"

        # print "image main start"
        # background = Image.open('mubeenyousaf78952f92d6904ad3.png')
        # foreground = Image.open("new1.png")
        #
        # background.paste(foreground, (0, 0), foreground)
        # background.show()
        # print "this is image"

            # context = {
            #     'image': profile.profile_image,
            #     'user_name': fb_username,
            # }
    # return render('practice.html', context )