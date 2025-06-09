from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

# Create your models here.

class SinglePage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = RichTextUploadingField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bài viết đơn lẻ"
        verbose_name_plural = "Bài viết đơn lẻ"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_page', args=[self.slug])
