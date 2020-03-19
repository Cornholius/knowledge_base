from django import forms
from .models import Post, Media
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class LocationForm(forms.Form):
    name = forms.CharField(label=u'Локация')
    photos = forms.ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}))


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
        self.fields['username'].widget.attrs.update({'class': 'input100', 'placeholder': 'Логин'})
        self.fields['password1'].widget.attrs.update({'class': 'input100', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'input100', 'placeholder': 'Повторите пароль'})
        self.fields['first_name'].widget.attrs.update({'class': 'input100', 'placeholder': 'Ваше имя'})
        self.fields['last_name'].widget.attrs.update({'class': 'input100', 'placeholder': 'Ваша фамилия'})
        for _ in self.fields:
            self.fields[_].label = ''
            self.fields[_].help_text = ''


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {'username': ('Writer')}

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input100', 'placeholder': 'Имя пользователя'})
        self.fields['password'].widget.attrs.update({'class': 'input100', 'placeholder': 'Пароль'})
        self.fields['username'].label = ""
        self.fields['password'].label = ""
