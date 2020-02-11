from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
        # labels = {'title': '', 'text': ''}
        # widgets = {'title': forms.TextInput(attrs={'placeholder': 'Название поста'}),
        #            'text': forms.Textarea(attrs={'placeholder': 'Текст поста'})
        #            }