from typing import Iterable
from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.
class Image(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="images_created",
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    Image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)

    # Add many-to-many relationship between users likes and images.
    user_likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name="images_liked",
                                        blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self) -> str:
        return self.title
    
    # Override save method of models.Model class to add slug automatically.
    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(force_insert, force_update, using, update_fields)