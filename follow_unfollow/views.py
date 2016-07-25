from django.shortcuts import render

# others redirect or http imorts
from django.shortcuts import render, Http404, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.utils import timezone

# models & forms import
from django.contrib.auth.models import User
from .models import UserProfile
from .models import RelationShip
from .models import Post
from follow_unfollow.form import RegisterForm
from follow_unfollow.form import LoginForm
from django.db.models import Q
from .form import PostForm
from tinymce.widgets import TinyMCE
from tinymce.views import render_to_link_list
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
# Create your views here.

def register_view(request):
    register_form = RegisterForm()
    print "sign up form"
    form = RegisterForm(request.POST or None)
    print form
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            print "form is register"
            email = register_form.cleaned_data.get("email")
            username = register_form.cleaned_data.get("username")
            password = register_form.cleaned_data.get("password")
            user = User.objects.create_user(username,email, password)
            print user
            user.save()
            print "register is success"

        else:
            print "form is not valid"
            raise Http404
    else:
        print "error in post"
    return render(request, 'signup.html', {'form':register_form})


def login_view(request):
    user = None
    form = LoginForm(request.POST or None)
    print "start"
    print form
    if request.method == "POST":
        user = LoginForm(request.POST)
        print "this is the post request"
        if form.is_valid():
            print "form is valid"
            l_username = form.cleaned_data.get("username")
            l_password = form.cleaned_data.get("password")
            user_login = authenticate(username=l_username, password=l_password)
            if user_login is not None:
                auth_login(request, user_login)
                user = request.user
                #return HttpResponseRedirect(reverse('all'))
                return redirect('postlist_view')
                #return render(request, 'profile.html', {'username': l_username })
            else:
                print "error"
    else:
        print "this is error in validation"
    return render(request, 'login.html', {'form': form, 'userobj':user} )


def logout_view(request):
    logout(request)
    print "you are logout"
    return HttpResponseRedirect(reverse('login_view'))



def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    #u = User.objects.get(username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    relation = RelationShip.objects.filter(follow=user).values_list('following',flat=True)
        #.exclude(follow = request.user)    # this query goes wrong because you have inserted the wrong data in the get_or_create
    #relation = RelationShip.objects.filter(following=u)
    print "profile",profile
    print  "relation", relation

    form = PostForm()
    print "request.method", request.method
    if request.method == "POST":
        print "this is request"
        form = PostForm(request.POST or None)
        if form.is_valid():
            print "this form is valid"
            post = form.save(commit=False)      #don't know why commit is false
            post.author = request.user
            text = form.cleaned_data.get("text")
            print "t:", text
            post.published_date = timezone.now()
            post.save()
            return redirect('postlist_view')
        else:
            print form.error


    return render(request, 'user_profile.html', {"relations": relation, "form":form })


#@login_required
def all_view(request):
    u = User.objects.get(email__iexact=request.user.email)
    print "u:",u
    user = User.objects.all().exclude(email=request.user.email)
    relation = RelationShip.objects.filter(follow=u).values_list('following_id',flat=True)      #the following is list of users we are getting the ids by _id
    print "relation:", relation
    return render(request, 'profile.html', {"user": user, "relation":relation})


def follow_view(request, username):
    user = User.objects.all().exclude(email=request.user.email)
    follow_user = User.objects.get(username=username)
    print follow_user
    print request.user
    relation, created = RelationShip.objects.get_or_create(follow=request.user, following=follow_user)

    if created:
        print "created", created

    elif relation:
        relation.delete()
        print "relation delete"

    return HttpResponseRedirect('/all/')

def newpost_view(request):
    #post = Post()
    #print post
    #if request.POST:
    #post.author = request.user     #form is also not getting post in here
    ##if request.method == "POST":
    #text = request.POST.get("mytextarea")
    #post.text = text
    #print "this is text",text
    #post.save()
    #return redirect('/all/')
    #post.objects.create(author=post.author, text=text)
    form = PostForm()
    print "request.method", request.method
    if request.method == "POST":
        print "this is request"
        form = PostForm(request.POST or None)
        if form.is_valid():
            print "this form is valid"
            post = form.save(commit=False)      #don't know why commit is false
            post.author = request.user
            text = form.cleaned_data.get("text")
            print "t:", text
            post.published_date = timezone.now()
            post.save()
            return redirect('postlist_view')
        else:
            print form.error


    return render(request,'user_profile.html',{'form':form})


def postlist_view(request):
    post = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
    #print post
    return render(request, 'post_list.html',{'posts':post})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    return render(request, 'post_detail.html', {'post':post})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            print "this is the post edit"
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        print "this is the post edit else"
    return render(request, 'post_edit.html', {'form': form})

def following_userspost_view(request):

   pass


def follow_users_view(request, username):
    user = get_object_or_404(User, username=username)
    relation = RelationShip.objects.filter(following=user).values_list('follow_id', flat=True)
    posts = Post.objects.filter(author__in = relation)
        #.values_list('follow_id', flat=True)
    print "user",user
    print "relation",relation
    print "post", posts


    return render(request, 'followuser.html', {'user':user, 'relation': relation, 'post':posts})


def relationship_status_view(request, username):
    user = get_object_or_404(User, username=username)
    relation = RelationShip.objects.filter(following=user).values_list('follow_id', flat=True)
    mutual_relation = RelationShip.objects.filter(follow=user).values_list('following_id', flat=True)
    test_relation = RelationShip.objects.filter(following__in=relation).values_list('following_id', flat=True)

        #.values_list('following_id', flat=True)
    print "relation status", relation
    print "mutual relation", mutual_relation
    print "test relation", test_relation



    return render(request, 'relationstatus.html',{'relation':relation, 'mutualrelation':mutual_relation})