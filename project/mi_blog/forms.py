from django import forms
from .models import User, Comment, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['bio', 'image_profile', 'city', 'preferences']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_profile'].required = False  # No obligatorio

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'image_profile']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class CommentsForm(forms.ModelForm):

    class Meta():

        model = Comment 
        fields = ['content']

class SearchForm(forms.Form):
    query = forms.CharField()

