from django.template.defaultfilters import slugify
from taggit.models import Tag, TaggedItem
from .transliterator import slugify as literator


class RuTag(Tag):

    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        return slugify(literator(self.name))[:128]


class RuTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return RuTag
