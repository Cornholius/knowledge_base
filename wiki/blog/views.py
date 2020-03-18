from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, RegisterForm, LoginForm
from taggit.models import Tag
from django.views import View
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse


class PostListView(View):

    def get(self, request, tag_slug=None):
        post_with_tags = Post.objects.all()
        user = str(request.user)
        anon = 'AnonymousUser'
        all_tags = Tag.objects.all()
        if user is anon:
            return redirect('../login')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            post_with_tags = post_with_tags.filter(tags__in=[tag])
            return render(request, 'blog/post_list.html', {'posts': post_with_tags, 'tag': tag, 'all_tags': all_tags})
        else:
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return render(request, 'blog/post_list.html', {'posts': posts, 'all_tags': all_tags})

    def post(self, request):
        search_text = request.POST.get('Search')
        posts = Post.objects.filter(Q(title__contains=search_text) | Q(text__contains=search_text))
        return render(request, 'blog/post_list.html', {'posts': posts})


class FileView(View):

    def get(self,request):
        print('###########################################')
        return HttpResponse(request)


class PostDetailView(View):

    def get(self, request, pk=None, file=None):
        id = pk
        post = get_object_or_404(Post, pk=pk)

        if file:
            print('OLOLOLOLO')


        qwe = Post.objects.get(id=id).document
        print('!!!!!!!!!!', request)
        print('@@@@@', request, '@@@@@', qwe)




        return render(request, 'blog/post_detail.html', {'post': post})


class PostNewView(View):

    def get(self, request):
        user = str(request.user)
        anon = 'AnonymousUser'
        if user is anon:
            return redirect('../login')
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            for tag in form.cleaned_data['tags']:
                post.tags.add(tag)
            return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
            return render(request, 'blog/post_edit.html', {'form': form})


class RegisterView(View):

    def __init__(self):
        self.text_button = 'Зарегистрироваться и войти'


    def get(self, request):
        return render(request, 'blog/login_or_register.html', {'form': RegisterForm,
                                                               'button': self.text_button})

    def post(self, request):
        new_user = RegisterForm(request.POST)
        if User.objects.filter(username=request.POST.get('username')).exists():
            error_text = 'Пользователь с таким логином уже существует'
            return render(request, 'blog/login_or_register.html', {'form': RegisterForm,
                                                                   'button': self.text_button,
                                                                   'error': error_text})
        if new_user.is_valid():
            print(User.objects.filter(username=request.POST.get('username')))
            new_user.save()
            username = new_user.cleaned_data.get('username')
            password = new_user.cleaned_data.get('password2')
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return render(request, 'blog/post_list.html', {'posts': posts})
        else:
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return render(request, 'blog/post_list.html', {'posts': posts})


class LoginView(View):

    def __init__(self):
        self.text_button = 'Войти'
        self.error_text = 'Неверный логин или пароль'

    def get(self, request):
        return render(request, 'blog/login_or_register.html', {'form': LoginForm, 'button': self.text_button})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return render(request, 'blog/post_list.html', {'posts': posts})
        else:
            return render(request, 'blog/login_or_register.html', {'error': self.error_text,
                                                                   'form': LoginForm,
                                                                   'button': self.text_button})


class LogoutView(View):

    def get(self, request):
        auth.logout(request)
        return redirect('../login')
