from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from taggit.models import Tag
from django.views import View


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


