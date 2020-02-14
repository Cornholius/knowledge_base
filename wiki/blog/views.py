from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, RegisterForm
from django.shortcuts import redirect
from taggit.models import Tag
from django.views import View
from django.http import HttpResponseRedirect

class PostListView(View):

    def get(self, request, tag_slug=None):
        post_with_tags = Post.objects.all()
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            post_with_tags = post_with_tags.filter(tags__in=[tag])
            return render(request, 'blog/post_list.html', {'posts': post_with_tags, 'tag': tag})
        else:
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return render(request, 'blog/post_list.html', {'posts': posts})


class PostDetailView(View):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})


class PostNewView(View):

    def get(self, request):
        if request.method == "POST":
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
        return render(request, 'blog/register.html', {'register_form': RegisterForm})

    def post(self, request):
        new_user = RegisterForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            return render(request, 'blog/post_list.html', {'posts': posts})
        else:
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            print('222222222222222222222222222222222222222')
            return render(request, 'blog/post_list.html', {'posts': posts})