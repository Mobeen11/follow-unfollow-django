from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth.views import logout
from .models import *
from PIL import Image
from urllib2 import urlopen, HTTPError
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.core.files import File
import datetime
import facebook
import urllib
from urlparse import urlparse
from twitter import *
from twython import Twython

# from twython_django_oauth.models import TwitterProfile

from django.template import Context, RequestContext


def home(request):

    if request.user.is_authenticated():
        return redirect('done')
    return render(request, 'facebook_image/home.html')


@login_required
def done(request):
    return render(request, "facebook_image/done.html", {})


def logout_view(request):
    logout(request)
    return redirect('test')


def test(request):
    context = {}
    images = ImagesList.objects.all()
    print "images: ", images
    # for i in images:
    #     print "i: ", i.image.url

    print "this is view"
    user = request.user
    if user.is_authenticated():
        print "user: ", user
        twitter_profile = TwitterStatus.objects.filter(username=user)
        facebook_profile = FacebookStatus.objects.filter(username=user)
        if twitter_profile:
            print "user is from twitter"
            for tw in twitter_profile:
                fullname = tw.fullname
                profile_image = tw.profile_image
                print "profile: ", tw.profile_image.url
                context = {
                    'fullname': fullname,
                    # 'profile': twitter_profile,
                    'image': tw.profile_image,
                    'images_display': images,
                    'user': user
                }

        if facebook_profile:
            print "user is from facebook"
            for fb in facebook_profile:

                fullname = fb.fullname
                profile_image = fb.profile_image
                print "profile: ", fb.profile_image.url
                context = {
                    'fullname': fullname,
                    # 'profile': twitter_profile,
                    'image': fb.profile_image,
                    'images_display': images,
                    'user': user
                }

    else:
        print "user doesn't exist"
        context = {'images_display': images, 'user':user }
    return render(request, 'facebook_image/practice.html', context)


# not applied
def save(request):
    user = request.user
    profile = Profile.objects.get(username=user)
    print "image is start", profile.profile_image
    # had to change the path dynamically
    # background = Image.open('static/test/mubeenyousaf78952f92d6904ad3-social.png')
    # background = Image.open(profile.profile_image)
    # change the file name accordingl
    # background = Image.open('static/test/mubeenyousaf78952f92d6904ad3-social.png')


    images = ImagesList.objects.all()
    for i in images:
        facebook_img = FacebookStatus()
        background = Image.open(profile.profile_image)
        background = background.resize((255, 230))
        # change the file name accordingly
        foreground = Image.open(i.image)
        foreground = foreground.resize((250, 230))

        background.paste(foreground, (0, 0), foreground)

        # image_url = 'http://localhost:9090/media/'+background.url
        background.save('static/test/background.png', "PNG")
        facebook_img.new_image.save("background" + '.png', File(open('static/test/background.png')))
        facebook_img.STATUS = "Approved"
        facebook_img.author = request.user
        facebook_img.message = "this is message post"
        facebook_img.link = "http://localhost:9090" + facebook_img.new_image.url
        facebook_img.save()
        print "image is saved: ", facebook_img.new_image.url

        # facebook_img.objects.create(STATUS="Approved", author=request.user, message="this is image", link= , new_image=)

    background.save('new_img.png',"PNG")

    # profile.new_profile_image.save("background"+ '.png', File(open('new_img.png')))
    print "image is done"

    get_images = FacebookStatus.objects.filter(author=request.user)
    print "get_image", get_images
    for im in get_images:
        print "im: ", im.new_image

    context = {
        'user_images': get_images,
        'image': profile.profile_image,
    }
    return render(request, 'facebook_image/practice.html', context)


# # share image on facebook
# def share_post(request, pk):
#     user = request.user
#     user = User.objects.get(username=user.username)
#share image on facebook
import requests
@login_required
def share_post(request, pk):
    print "this is error"
    user = request.user
    user = User.objects.get(username=request.user.username)
    print "user: ", user
    fb_profile = FacebookStatus.objects.filter(username=user)
    print "fb_profile: ", fb_profile
    if request.method == "GET":
        print "request is get"
        message = request.GET.get("message")
        print "message: ", message
    images = ImagesList.objects.filter(pk=pk)
    for i in images:
        facebook_img = FacebookStatus()
        for fb in fb_profile:
            print "this is fb profile"
            background = Image.open(fb.profile_image)
            background = background.resize((255, 230))
            # change the file name accordingly
            foreground = Image.open(i.image)
            foreground = foreground.resize((250, 230))
            background.paste(foreground, (0, 0), foreground)
            background.save('static/test/background.png', "PNG")
            # avatar = background.save('static/test/background.png', "PNG")
            # fb.new_image.save(slugify(user.username) + '.png',
            #                                 ContentFile(avatar.read()))
            # x = (fb.new_image.url).split('facebookstatus_images/')
            # y = "".join(x)
            # print "link: ", y
            #
            # fb.link = 'http://followunfollow.herokuapp.com' + y
            fb.new_image.save("background" + '.png', File(open('static/test/background.png')))
            fb.link = 'http://followunfollow.herokuapp.com'+fb.new_image.url
            fb.message = message
            fb.save()
            background.show()


    statuses = FacebookStatus.objects.filter(username=user)[:1]  # We only need one status for this test

    print "statuses: ", statuses
    status = statuses[0]
    auth = user.social_auth.first()
    print "auth: ", auth.extra_data['access_token']
    graph = facebook.GraphAPI(auth.extra_data['access_token'])
    file = open('static/test/background.png', 'rb')
    if file:
        print "file found"
    data = file.read()
    # graph.put_object('me', 'photos', message="You can put a caption here", source=file.read())
    albumid = ''
    for s in statuses:
        print "s.image: ", s.new_image.url
        # with open("static/test/background.png", "rb") as image:
        parameters = {
                      'name': 'FollowunFollow',
                      'link': 'http://followunfollow.herokuapp.com/test',
                      'message': s.message,
                      'description': 'Place Image Over your Profile',
                      'picture': s.link,
                      'access_token': auth.extra_data['access_token']
                      }
        r = requests.post('https://graph.facebook.com/me/feed', params=parameters)
        print "facebook user feed", r.status_code
        posted_image_id = graph.put_wall_post(parameters)

    file.close()
    print "link:", status.link
    # status.publish_timestamp = datetime.datetime.now()
    status.save()

    return redirect('test')


CONSUMER_KEY = 'HISKYRsVumzfw29OsuO6uemJY'
CONSUMER_SECRET = '2sUI8VMPSaYpma1wQeQn6GSKP9o08uQAbtYQH5JAhIufWPT4Xv'
ACCESS_TOKEN_KEY = '587179393-0WzjoaIUP8hg45wmabvebNLErFHcTOTquh4HJyeQ'
ACCESS_TOKEN_SECRET = 'uu0uZiv3p1jkiFWcXBUrZh4fIpwkKbHeZHPRjcZia7dNA'
from TwitterAPI import TwitterAPI
@login_required
def tweet(request, pk):
    c = RequestContext(request)
    user = request.user
    print "user: ", user.social_auth


    if request.method == "GET":
        print "request is get"
        message = request.GET.get("message")
        print "message: ", message

    tw_profile = TwitterStatus.objects.filter(username=user)
    images = ImagesList.objects.filter(pk=pk)
    for i in images:
        for tw in tw_profile:
            print "this is tw profile"
            background = Image.open(tw.profile_image)
            background = background.resize((255, 230))
            # change the file name accordingly
            foreground = Image.open(i.image)
            foreground = foreground.resize((250, 230))
            background.paste(foreground, (0, 0), foreground)
            background.save('static/test/background.png', "PNG")
            tw.new_image.save("background" + '.png', File(open('static/test/background.png')))
            tw.link = "https://followunfollow.herokuapp.com" + tw.new_image.url
            tw.message = message
            tw.save()

            background.show()

    statuses = TwitterStatus.objects.filter(username=user)[:1]
    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

    status = statuses
    print "status: ", status
    for s in status:
        print "in the loop"
        file = open('static/test/background.png', 'rb')
        data = file.read()
        r = api.request('statuses/update_with_media', {'status': 'http://followunfollow.herokuapp.com/test/'}, {'media[]': data})
    return redirect('test')



#
# # this is attemptt 2
# from django import template
# from django.contrib.sites.models import Site
# from django.db.models import Model
# from django.template.defaultfilters import urlencode
# try:
#     from django_bitly.templatetags.bitly import bitlify
#     DJANGO_BITLY = True
# except ImportError:
#     DJANGO_BITLY = False
#
# register = template.Library()
#
# TWITTER_ENDPOINT = 'http://twitter.com/intent/tweet?text=%s'
# FACEBOOK_ENDPOINT = 'http://www.facebook.com/sharer/sharer.php?u=%s'
#
# class MockRequest(object):
#     @staticmethod
#     def build_absolute_uri(relative_url):
#         if relative_url.startswith('http'):
#             return relative_url
#         current_site = Site.objects.get_current()
#         return '%s%s' % (current_site.domain, relative_url)
#
# def _build_url(request, obj_or_url):
#     if obj_or_url is not None:
#         if isinstance(obj_or_url, Model):
#             if DJANGO_BITLY:
#                 return bitlify(obj_or_url)
#             else:
#                 return request.build_absolute_uri(obj_or_url.get_absolute_url())
#         else:
#             return request.build_absolute_uri(obj_or_url)
#     return ''
#
# @register.simple_tag(takes_context=True)
# def post_to_facebook_url(context, obj_or_url=None):
#     request = context.get('request', MockRequest())
#     url = _build_url(request, obj_or_url)
#     context['facebook_url'] = FACEBOOK_ENDPOINT % urlencode(url)
#     return context


# def tweet(request):
#     c = RequestContext(request)
#     # print "request: ", request.session
#     # print "c: ", c
#     user = request.user
#     print "user: ", user
#     auth=OAuth('HISKYRsVumzfw29OsuO6uemJY',
#                    '2sUI8VMPSaYpma1wQeQn6GSKP9o08uQAbtYQH5JAhIufWPT4Xv',
#                    'HISKYRsVumzfw29OsuO6uemJY',
#                    '2sUI8VMPSaYpma1wQeQn6GSKP9o08uQAbtYQH5JAhIufWPT4Xv')
#
#     twitter = Twython(
#         twitter_token='HISKYRsVumzfw29OsuO6uemJY',
#         twitter_secret='2sUI8VMPSaYpma1wQeQn6GSKP9o08uQAbtYQH5JAhIufWPT4Xv',
#         oauth_token=user.oauth_token,
#         oauth_token_secret=user.oauth_secret
#     )
#     twitter.updateStatus(status="See how easy this was?")
#     return redirect('test')

# def tweet(request):
#     t = Twitter(
#         auth=OAuth('HISKYRsVumzfw29OsuO6uemJY',
#                    '2sUI8VMPSaYpma1wQeQn6GSKP9o08uQAbtYQH5JAhIufWPT4Xv',
#                    'HISKYRsVumzfw29OsuO6uemJY',
#                    '2sUI8VMPSaYpma1wQeQn6GSKP9o08uQAbtYQH5JAhIufWPT4Xv')
#         )
#     examples = {}
#     examples["twurl"] = "twurl -H upload.twitter.com \"/1.1/media/upload.json\" -f /path/to/file -F media -X POST"
#     examples["python"] = """
#         import twitter
#     api = twitter.Api(
#         base_url='https://api.twitter.com/1.1',
#         consumer_key='YOUR_CONSUMER_KEY',
#         consumer_secret='YOUR_CONSUMER_SECRET',
#         access_token_key='YOUR_ACCESS_KEY',
#         access_token_secret='YOUR_ACCESS_SECRET')
#
#     url = '%s/media/upload.json' % api.upload_url
#     data = {}
#     data['media'] = open(str("/path/to/file"), 'rb').read()
#     response = api._RequestUrl(url, 'POST', data=data)
#     """
#
#     examples["nodejs"] = """
#     var Twit = require('twit')
#     var fs = require('fs')
#     var T = new Twit({
#         consumer_key:         'YOUR_CONSUMER_KEY'
#       , consumer_secret:      'YOUR_CONSUMER_SECRET'
#       , access_token:         'YOUR_ACCESS_KEY'
#       , access_token_secret:  'YOUR_ACCESS_SECRET'
#     })
#     var b64content = fs.readFileSync('/path/to/img', { encoding: 'base64' })
#     // first we must post the media to Twitter
#     T.post('media/upload', { media_data: b64content }, function (err, data, response) {
#       // now we can reference the media and post a tweet (media will attach to the tweet)
#       var mediaIdStr = data.media_id_string
#       var params = { status: 'Tweet with a photo!', media_ids: [mediaIdStr] }
#       T.post('statuses/update', params, function (err, data, response) {
#         console.log(data)
#       })
#     })
#     """
#
#     return redirect('/test/')

    # pass


#change the profile picture twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
#avatar = open('myImage.png', 'rb')
#twitter.update_profile_image(image=avatar)





