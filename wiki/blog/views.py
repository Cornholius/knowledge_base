from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, RegisterForm, LoginForm
from django.shortcuts import redirect
from taggit.models import Tag
from django.views import View
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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
        return render(request, 'blog/register.html', {'form': RegisterForm})

    def post(self, request):
        new_user = RegisterForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return render(request, 'blog/post_list.html', {'posts': posts})
        else:
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return render(request, 'blog/post_list.html', {'posts': posts})


class LoginView(View):

    def get(self, request):
        return render(request, 'blog/login.html', {'form': LoginForm})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return render(request, 'blog/post_list.html', {'posts': posts})


class LogoutView(View):

    def get(self, request):
        auth.logout(request)
        return redirect('../login')
