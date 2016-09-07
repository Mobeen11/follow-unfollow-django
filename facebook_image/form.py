from django import forms
from django.contrib.auth.models import User
from .models import *



class FacebookStatusForm(forms.Form):
    message = forms.CharField(max_length=255)



class TwitterStatusForm(forms.Form):
    message = forms.CharField(max_length=255)




