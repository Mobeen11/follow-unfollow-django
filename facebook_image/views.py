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
    # profile = Profile.objects.all()
    # profile_image = profile.profile_image
    # context = {'profile_img': profile_image}
    print "this is view"
    user  = request.user
    if user.is_authenticated():
        print "user: ", user
        profile = Profile.objects.get(username=user)
        print "profile: ", profile.profile_image

        context = {
            # 'image': profile.profile_image,
            # 'username': profile.username,
            'profile': profile,
            'image': profile.profile_image,
        }

    else:
        print "user doesn't exist"
        context = {}
    return render(request, 'facebook_image/practice.html', context)


def save(request):
    user = request.user
    profile = Profile.objects.get(username=user)
    print "image is start"
    # had to change the path dynamically
    background = Image.open('static/test/mubeenyousaf78952f92d6904ad3-social.png')
    # change the file name accordingly
    foreground = Image.open("static/img/new1.png")
    foreground = foreground.resize((50, 50))

    background.paste(foreground, (0, 0), foreground)
    background.show()
    background.save('new_img.png',"PNG")

    profile.new_profile_image.save("background"+ '.png', File(open('new_img.png')))
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




