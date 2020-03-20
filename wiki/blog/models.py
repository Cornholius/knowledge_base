from django.conf import settings
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from .slug_ru_patch import RuTaggedItem


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author_first_name = ''
    author_last_name = ''
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager(through=RuTaggedItem)
    document = models.FileField(blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Media(models.Model):
    document = models.FileField(blank=True)
    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
