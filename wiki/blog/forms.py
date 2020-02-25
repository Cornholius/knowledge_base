from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'tags')


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input100'})
        self.fields['password1'].widget.attrs.update({'class': 'input100'})
        self.fields['password2'].widget.attrs.update({'class': 'input100'})
        self.fields['first_name'].widget.attrs.update({'class': 'input100'})
        self.fields['last_name'].widget.attrs.update({'class': 'input100'})


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input100'})
        self.fields['password'].widget.attrs.update({'class': 'input100'})