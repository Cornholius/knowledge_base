from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'tags')


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')