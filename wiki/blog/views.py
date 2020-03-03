from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, RegisterForm, LoginForm
from django.shortcuts import redirect
from taggit.models import Tag
from django.views import View
from django.contrib import auth


class PostListView(View):

    def get(self, request, tag_slug=None):
        post_with_tags = Post.objects.all()
        user = str(request.user)
        anon = 'AnonymousUser'
        if user is anon:
            return redirect('../login')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            post_with_tags = post_with_tags.filter(tags__in=[tag])
            return render(request, 'blog/post_list.html', {'posts': post_with_tags, 'tag': tag})
        else:
            print(user)
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return render(request, 'blog/post_list.html', {'posts': posts})


class PostDetailView(View):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
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
        form = PostForm(request.POST)
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

    def get(self, request):
        text_button = 'Зарегистрироваться и войти'
        return render(request, 'blog/login_or_register.html', {'form': RegisterForm, 'button': text_button})

    def post(self, request):
        new_user = RegisterForm(request.POST)
        if new_user.is_valid():
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
