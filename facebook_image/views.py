from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth.views import logout
from .models import *
from PIL import Image
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.core.files import File
import datetime
import facebook
from twitter import *


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

    images = ImagesList.objects.all()
    print "images: ", images
    for i in images:
        print "i: ", i.image.url

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
                }

    else:
        print "user doesn't exist"
        context = {'images_display': images, }
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

        facebook_img.new_image.save("background" + '.png', File(open('new_img.png')))
        facebook_img.STATUS = "Approved"
        facebook_img.author = request.user
        facebook_img.message = "this is message post"
        facebook_img.link = "https://followunfollow.herokuapp.com"+facebook_img.new_image.url
        facebook_img.save()
        background.show()

        # facebook_img.objects.create(STATUS="Approved", author=request.user, message="this is image", link= , new_image=)


    background.save('new_img.png',"PNG")

    # profile.new_profile_image.save("background"+ '.png', File(open('new_img.png')))
    print "image is done"
    profile.save()
    print "this is image: ",  profile.new_profile_image

    get_pic_profile = Profile.objects.get(username=user)
    print get_pic_profile.new_profile_image
    context = {
        'image': get_pic_profile.new_profile_image,
    }
    return render(request, 'facebook_image/practice.html', context)

#share image on facebook
def share_post(request):
    user = User.objects.get(username=request.user.username)
    print "user: ", user
    statuses = FacebookStatus.objects.filter(author=user)[:1]  # We only need one status for this test

    print "statuses: ", statuses
    status = statuses[0]
    auth = user.social_auth.first()
    print "auth: ", auth.extra_data['access_token']
    graph = facebook.GraphAPI(auth.extra_data['access_token'])
    graph.put_object('me', 'feed', link=status.link)
    status.publish_timestamp = datetime.datetime.now()
    status.save()

    return redirect('test')



def tweet(request):
    t = Twitter(
        auth=OAuth('HISKYRsVumzfw29OsuO6uemJY',
                   '2sUI8VMPSaYpma1wQeQn6GSKP9o08uQAbtYQH5JAhIufWPT4Xv',
                   'HISKYRsVumzfw29OsuO6uemJY',
                   '2sUI8VMPSaYpma1wQeQn6GSKP9o08uQAbtYQH5JAhIufWPT4Xv')
        )
    examples = {}
    examples["twurl"] = "twurl -H upload.twitter.com \"/1.1/media/upload.json\" -f /path/to/file -F media -X POST"
    examples["python"] = """
        import twitter
    api = twitter.Api(
        base_url='https://api.twitter.com/1.1',
        consumer_key='YOUR_CONSUMER_KEY',
        consumer_secret='YOUR_CONSUMER_SECRET',
        access_token_key='YOUR_ACCESS_KEY',
        access_token_secret='YOUR_ACCESS_SECRET')

    url = '%s/media/upload.json' % api.upload_url
    data = {}
    data['media'] = open(str("/path/to/file"), 'rb').read()
    response = api._RequestUrl(url, 'POST', data=data)
    """

    examples["nodejs"] = """
    var Twit = require('twit')
    var fs = require('fs')
    var T = new Twit({
        consumer_key:         'YOUR_CONSUMER_KEY'
      , consumer_secret:      'YOUR_CONSUMER_SECRET'
      , access_token:         'YOUR_ACCESS_KEY'
      , access_token_secret:  'YOUR_ACCESS_SECRET'
    })
    var b64content = fs.readFileSync('/path/to/img', { encoding: 'base64' })
    // first we must post the media to Twitter
    T.post('media/upload', { media_data: b64content }, function (err, data, response) {
      // now we can reference the media and post a tweet (media will attach to the tweet)
      var mediaIdStr = data.media_id_string
      var params = { status: 'Tweet with a photo!', media_ids: [mediaIdStr] }
      T.post('statuses/update', params, function (err, data, response) {
        console.log(data)
      })
    })
    """

    return redirect('/test/')

    # pass





