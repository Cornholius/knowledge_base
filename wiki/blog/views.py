from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from taggit.models import Tag


def post_list(request, tag_slug=None):
    post_with_tags = Post.objects.all()
    # tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_with_tags = post_with_tags.filter(tags__in=[tag])
        return render(request, 'blog/post_list.html', {'posts': post_with_tags, 'tag': tag})
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', form.cleaned_data)
            for tag in form.cleaned_data['tags']:
                post.tags.add(tag)
                print(post.tags.all())
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})


def post_list_test(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/test.html', {'posts': posts})
