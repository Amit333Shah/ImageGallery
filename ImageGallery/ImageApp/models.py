from django.db import models
from taggit.managers import TaggableManager

# Create your models here.


class ImageUpload(models.Model):
    title = models.CharField(max_length=200, blank=False)
    desc = models.TextField()
    images = models.FileField(null=True, blank=True, upload_to='images/')
    slug = models.SlugField(unique=True, max_length=100, default="uuid.uuid1")
    tags = TaggableManager()

    def __str__(self):
        return self.title
