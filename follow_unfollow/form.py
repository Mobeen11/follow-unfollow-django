from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .models import RelationShip
from .models import Post
from tinymce.widgets import TinyMCE



class RegisterForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
            'password': forms.PasswordInput(),
        }
    class Meta:
        Model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
            'password': forms.PasswordInput(),
        }

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=12)
    followers = forms.CharField(max_length=120)
    class Meta:
        Model = UserProfile
        fields = ['username', 'followers']

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Post
        fields = ['text']

