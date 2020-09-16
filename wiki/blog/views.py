from django.utils import timezone
from .models import Post, Media
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, RegisterForm, LoginForm, MediaForm
from taggit.models import Tag, TaggedItem
from django.views import View
from django.contrib import auth
from django.db.models import Q
from django.core.files.base import ContentFile
from django.contrib.auth.models import User


class MediaFiles:

    def delete_media(self, request):
        if request.POST['delete'] is not None:
            Media.objects.filter(document=request.POST['delete']).delete()


class PostListView(View):

    def tags(self):
        tags_cloud = Tag.objects.in_bulk()  # выгребаем словарь со всеми существующими тегами (id и пост+теги)
        dead_tags_id = []
        for i in tags_cloud.keys():  # Перебираем все теги и ищем пустые
            maybe_dead_tags = TaggedItem.objects.filter(tag_id=i)
            if maybe_dead_tags.exists() is False:  # Если к тегу не привязан пост он едет в список мёртвых
                dead_tags_id.append(i)
        for i in dead_tags_id:
            Tag.objects.filter(id=i).delete()

    def get(self, request, tag_slug=None):
        self.tags()
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
            # author = User.objects.get(id=posts.author_id)
            return render(request, 'blog/post_list.html', {'posts': posts, 'all_tags': all_tags})

    def post(self, request):
        search_text = request.POST.get('Search')
        posts = Post.objects.filter(Q(title__contains=search_text) | Q(text__contains=search_text))
        return render(request, 'blog/post_list.html', {'posts': posts})


class PostDetailView(View):

    def get(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        author = User.objects.get(username=post.author)
        media = Media.objects.filter(post_id=pk)
        return render(request, 'blog/post_detail.html', {'post': post, 'media': media, 'author': author})

    def post(self, request, pk=None):
        MediaFiles.delete_media(self, request)
        return redirect('post_detail', pk=pk)


class EditPostView(View):

    def edit_tags(self, pk=None):  # получаем имена привязаных тегов, удаляем все привязанные теги к посту, отправляем их в форму
        tag_id = []
        tag_name = []
        tags_in_post = TaggedItem.objects.filter(object_id=pk).values()
        for i in tags_in_post:  # получаем по id поста все привязанные теги
            tag_id.append(i['tag_id'])
        for i in tag_id:  # получаем имена всех привязаных тегов и складываем в список
            tag_names = Tag.objects.filter(id=i).values()
            for names in tag_names:
                tag_name.append(names['name'])
        for i in tag_id:  # удаляем связи тегов с постом по id тегов
            TaggedItem.objects.filter(tag_id=i).delete()
        tag_string = ', '.join(tag_name)
        return tag_string

    def get(self, request, pk=None):
        edit_user = Post.objects.filter(id=pk)
        media_files = Media.objects.filter(post_id=pk)
        form = PostForm(edit_user.values()[0])
        media = MediaForm()
        form.data['tags'] = self.edit_tags(pk)
        return render(request, 'blog/post_edit.html', {'form': form, 'media': media, 'media_files': media_files})

    def post(self, request, pk=None):
        form = PostForm(request.POST, request.FILES)
        if 'delete' in request.POST:
            MediaFiles.delete_media(self, request)
            return redirect('post_edit', pk=pk)
        if request.POST['save']:
            if form.is_valid():
                post = Post.objects.get(id=pk)
                post.title = form.data['title']
                post.text = form.data['text']
                if request.FILES.getlist('media') is not None:
                    for _ in request.FILES.getlist('media'):
                        data = _.read()  # Если файл целиком умещается в памяти
                        media = Media(post=post)
                        media.document.save(_.name, ContentFile(data))
                        media.save()
                for tag in form.cleaned_data['tags']:
                    post.tags.add(tag)
                post.save()
                return redirect('post_detail', pk=pk)
            else:
                return redirect('post_edit', pk=pk)


class DeletePostView(View):

    def get(self, request, pk):
        Post.objects.filter(id=pk).delete()
        Media.objects.filter(post_id=pk).delete()
        return redirect('/')


class PostNewView(View):

    def get(self, request):
        user = str(request.user)
        anon = 'AnonymousUser'
        if user is anon:
            return redirect('../login')
        form = PostForm()
        media = MediaForm()
        return render(request, 'blog/post_edit.html', {'form': form, 'media': media})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            print('##########################', post.author)
            post.save()
            for _ in request.FILES.getlist('media'):
                data = _.read()  # Если файл целиком умещается в памяти
                media = Media(post=post)
                media.document.save(_.name, ContentFile(data))
                media.save()
            for tag in form.cleaned_data['tags']:
                post.tags.add(tag)
            return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
            return render(request, 'blog/post_edit.html', {'form': form})


class RegisterView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
            return redirect('../')
        else:
            return render(request, 'blog/login_or_register.html', {'error': self.error_text,
                                                                   'form': LoginForm,
                                                                   'button': self.text_button})


class LogoutView(View):

    def get(self, request):
        auth.logout(request)
        return redirect('../login')
