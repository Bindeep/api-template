from django.db import models

from apps.core.utils.slugify import unique_slugify


class BaseModel(models.Model):
    """Base model for this project."""
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugModel(models.Model):
    """
    Abstract model to insert slug field in model

    Takes reference from fields `name` or `title` and create
    slug for that instance before saving.
    """
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        abstract = True

    def get_slug_text(self):
        slug_text = None
        if hasattr(self, 'name'):
            slug_text = self.name.lower()
        elif hasattr(self, 'title'):
            slug_text = self.title.lower()
        assert slug_text is not None,\
            "There must be a field named `name` or `title` or `alt name`"
        return slug_text

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_text = self.get_slug_text()
            unique_slugify(self, slug_text)
        if self.slug and self.slug.startswith("copy-of"):
            slug_text = self.get_slug_text()
            unique_slugify(self, slug_text)
        return super().save(*args, **kwargs)
